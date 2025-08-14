# ==================================================
# БЛОК 1: Установка пакетов и инициализация
# ==================================================

# Установка необходимых библиотек
!pip install mediapipe torch torchvision opencv-python pillow qdrant-client

import cv2
import numpy as np
import mediapipe as mp
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image
import base64
from io import BytesIO
import uuid
from datetime import datetime
import os
import glob
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

# Инициализация MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Инициализация модели ResNet
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Используется устройство: {device}")

# Загружаем предобученную ResNet-50
resnet_model = resnet50(pretrained=True)
# Убираем последний слой классификации, оставляем feature extractor
resnet_model = nn.Sequential(*list(resnet_model.children())[:-1])
resnet_model.eval()
resnet_model = resnet_model.to(device)

# Трансформации для ResNet
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                       std=[0.229, 0.224, 0.225])
])

# Инициализация Qdrant клиента и создание коллекции
qdrant_client = QdrantClient(location=":memory:")

# Создание коллекции для губ
collection_name = "lips_vectors"
vector_size = 2048  # Размер вектора ResNet-50

try:
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )
    print(f"✓ Коллекция '{collection_name}' создана успешно")
except Exception as e:
    print(f"⚠️ Коллекция уже существует или ошибка создания: {e}")

# Индексы точек губ в MediaPipe Face Mesh
LIPS_INDICES = [
    # Внешний контур губ
    61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318,
    # Внутренний контур губ
    78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 415,
    # Дополнительные точки для лучшего выделения
    13, 82, 81, 80, 78, 191, 80, 81, 82, 13, 312, 311, 310, 415
]

def extract_lips_vector(image_path):
    """
    Извлекает вектор губ из изображения

    Args:
        image_path (str): путь к изображению

    Returns:
        dict: {
            'success': bool,
            'vector': list,
            'lips_image_b64': str,
            'landmarks': list,
            'error': str
        }
    """

    try:
        # 1. Загрузка изображения
        image = cv2.imread(image_path)
        if image is None:
            return {
                'success': False,
                'vector': None,
                'lips_image_b64': None,
                'landmarks': None,
                'error': f'Не удалось загрузить изображение: {image_path}'
            }

        # Конвертируем BGR в RGB для MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = rgb_image.shape[:2]

        # 2. Детекция лица и ключевых точек
        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        ) as face_mesh:

            results = face_mesh.process(rgb_image)

            if not results.multi_face_landmarks:
                return {
                    'success': False,
                    'vector': None,
                    'lips_image_b64': None,
                    'landmarks': None,
                    'error': 'Лицо не обнаружено на изображении'
                }

            # Получаем первое найденное лицо
            face_landmarks = results.multi_face_landmarks[0]

            # 3. Извлечение координат губ
            lips_points = []
            for idx in LIPS_INDICES:
                if idx < len(face_landmarks.landmark):
                    landmark = face_landmarks.landmark[idx]
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    lips_points.append([x, y])

            if not lips_points:
                return {
                    'success': False,
                    'vector': None,
                    'lips_image_b64': None,
                    'landmarks': None,
                    'error': 'Не удалось извлечь точки губ'
                }

            # 4. Определение области губ
            lips_points = np.array(lips_points)
            x_min, y_min = np.min(lips_points, axis=0)
            x_max, y_max = np.max(lips_points, axis=0)

            # Добавляем отступы (20% от размера)
            margin_x = int((x_max - x_min) * 0.2)
            margin_y = int((y_max - y_min) * 0.2)

            x_min = max(0, x_min - margin_x)
            y_min = max(0, y_min - margin_y)
            x_max = min(width, x_max + margin_x)
            y_max = min(height, y_max + margin_y)

            # 5. Обрезка области губ
            lips_region = rgb_image[y_min:y_max, x_min:x_max]

            if lips_region.size == 0:
                return {
                    'success': False,
                    'vector': None,
                    'lips_image_b64': None,
                    'landmarks': None,
                    'error': 'Пустая область губ'
                }

            # 6. Преобразование в PIL для ResNet
            lips_pil = Image.fromarray(lips_region)
            lips_tensor = transform(lips_pil).unsqueeze(0).to(device)

            # 7. Векторизация через ResNet
            with torch.no_grad():
                features = resnet_model(lips_tensor)
                # Преобразуем в одномерный вектор
                vector = features.squeeze().cpu().numpy().flatten().tolist()

            # 8. Конвертация изображения губ в base64
            lips_pil_resized = lips_pil.resize((100, 100))  # Миниатюра
            buffer = BytesIO()
            lips_pil_resized.save(buffer, format='JPEG')
            lips_image_b64 = base64.b64encode(buffer.getvalue()).decode()

            # 9. Подготовка landmarks для сохранения
            landmarks_normalized = []
            for point in lips_points:
                landmarks_normalized.append([
                    float(point[0] - x_min) / (x_max - x_min),  # Нормализованная x
                    float(point[1] - y_min) / (y_max - y_min)   # Нормализованная y
                ])

            return {
                'success': True,
                'vector': vector,
                'lips_image_b64': lips_image_b64,
                'landmarks': landmarks_normalized,
                'error': None,
                'lips_bbox': [int(x_min), int(y_min), int(x_max), int(y_max)],
                'vector_size': len(vector)
            }

    except Exception as e:
        return {
            'success': False,
            'vector': None,
            'lips_image_b64': None,
            'landmarks': None,
            'error': f'Ошибка при обработке: {str(e)}'
        }

def clear_collection():
    """
    Очищает коллекцию губ в Qdrant

    Returns:
        dict: результат операции
    """
    try:
        # Получаем информацию о коллекции
        collection_info = qdrant_client.get_collection(collection_name)
        points_count = collection_info.points_count

        if points_count == 0:
            print("✓ Коллекция уже пуста")
            return {'success': True, 'deleted_count': 0}

        # Удаляем коллекцию
        qdrant_client.delete_collection(collection_name)

        # Создаем заново
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

        print(f"✓ Коллекция очищена. Удалено {points_count} точек")
        return {'success': True, 'deleted_count': points_count}

    except Exception as e:
        print(f"❌ Ошибка при очистке коллекции: {str(e)}")
        return {'success': False, 'error': str(e)}

def load_base_lips_to_qdrant(base_dir="/content/base_lips"):
    """
    Загружает все изображения из директории base_lips в Qdrant

    Args:
        base_dir (str): путь к директории с базовыми изображениями губ

    Returns:
        dict: статистика загрузки
    """

    start_time = datetime.now()
    print(f"🔄 Начинаю загрузку изображений из {base_dir}...")
    print(f"⏰ Время начала: {start_time.strftime('%H:%M:%S')}")

    # Проверяем существование директории
    if not os.path.exists(base_dir):
        print(f"❌ Директория {base_dir} не существует")
        return {'success': False, 'error': f'Директория {base_dir} не найдена'}

    # Поддерживаемые форматы изображений
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp']
    image_files = []

    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(base_dir, ext)))
        image_files.extend(glob.glob(os.path.join(base_dir, ext.upper())))

    if not image_files:
        print(f"❌ В директории {base_dir} не найдено изображений")
        return {'success': False, 'error': 'Изображения не найдены'}

    print(f"📁 Найдено {len(image_files)} изображений")

    successful_uploads = 0
    failed_uploads = 0
    upload_results = []

    for i, image_path in enumerate(image_files, 1):
        # Получаем имя файла без расширения
        filename = os.path.basename(image_path)
        name_without_ext = os.path.splitext(filename)[0]

        print(f"🔄 [{i}/{len(image_files)}] Обрабатываю: {filename}")

        # Векторизуем изображение
        lips_data = extract_lips_vector(image_path)

        if lips_data['success']:
            # Подготавливаем payload для сохранения в Qdrant
            point_id = str(uuid.uuid4())

            payload = {
                'name': name_without_ext,
                'filename': filename,
                'source_path': image_path,
                'lips_image_b64': lips_data['lips_image_b64'],
                'landmarks': lips_data['landmarks'],
                'lips_bbox': [int(coord) for coord in lips_data.get('lips_bbox', [])],
                'vector_size': int(lips_data['vector_size']),
                'upload_date': datetime.now().isoformat()
            }

            # Создаем точку для Qdrant
            point = PointStruct(
                id=point_id,
                vector=lips_data['vector'],
                payload=payload
            )

            try:
                # Сохраняем точку
                operation_info = qdrant_client.upsert(
                    collection_name=collection_name,
                    points=[point]
                )

                successful_uploads += 1
                print(f"   ✓ Успешно загружено (ID: {point_id[:8]}...)")
                upload_results.append({
                    'filename': filename,
                    'name': name_without_ext,
                    'point_id': point_id,
                    'status': 'success'
                })

            except Exception as e:
                failed_uploads += 1
                print(f"   ❌ Ошибка сохранения: {str(e)}")
                upload_results.append({
                    'filename': filename,
                    'name': name_without_ext,
                    'error': str(e),
                    'status': 'failed'
                })
        else:
            failed_uploads += 1
            print(f"   ❌ Ошибка векторизации: {lips_data['error']}")
            upload_results.append({
                'filename': filename,
                'name': name_without_ext,
                'error': lips_data['error'],
                'status': 'failed'
            })

    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\n📊 Статистика загрузки:")
    print(f"   ✓ Успешно: {successful_uploads}")
    print(f"   ❌ Ошибок: {failed_uploads}")
    print(f"   📁 Всего файлов: {len(image_files)}")
    print(f"   ⏱️ Время выполнения: {duration}")
    print(f"   🚀 Скорость: {len(image_files)/duration.total_seconds():.2f} изображений/сек")

    return {
        'success': True,
        'total_files': len(image_files),
        'successful_uploads': successful_uploads,
        'failed_uploads': failed_uploads,
        'upload_results': upload_results,
        'duration': duration,
        'speed': len(image_files)/duration.total_seconds()
    }

def search_from_test_directory(test_dir="/content/test_lips", top_k=5, threshold=0.3):
    """
    Ищет похожие губы для изображения из тестовой директории

    Args:
        test_dir (str): путь к директории с тестовым изображением
        top_k (int): количество результатов поиска
        threshold (float): минимальный порог схожести

    Returns:
        dict: результаты поиска
    """

    start_time = datetime.now()
    print(f"🔍 Поиск в тестовой директории {test_dir}...")
    print(f"⏰ Время начала: {start_time.strftime('%H:%M:%S')}")

    # Проверяем существование директории
    if not os.path.exists(test_dir):
        print(f"❌ Директория {test_dir} не существует")
        return {'success': False, 'error': f'Директория {test_dir} не найдена'}

    # Находим все изображения в директории
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp']
    image_files = []

    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(test_dir, ext)))
        image_files.extend(glob.glob(os.path.join(test_dir, ext.upper())))

    if not image_files:
        print(f"❌ В директории {test_dir} не найдено изображений")
        return {'success': False, 'error': 'Изображения не найдены'}

    if len(image_files) != 1:
        print(f"❌ В директории {test_dir} должен быть только один файл, найдено: {len(image_files)}")
        print("Найденные файлы:")
        for f in image_files:
            print(f"   - {os.path.basename(f)}")
        return {'success': False, 'error': f'Найдено {len(image_files)} файлов, ожидался 1'}

    test_image_path = image_files[0]
    test_filename = os.path.basename(test_image_path)

    print(f"📸 Тестовое изображение: {test_filename}")

    # Векторизуем тестовое изображение
    vectorization_start = datetime.now()
    query_lips_data = extract_lips_vector(test_image_path)
    vectorization_time = datetime.now() - vectorization_start

    if not query_lips_data['success']:
        print(f"❌ Ошибка векторизации тестового изображения: {query_lips_data['error']}")
        return {
            'success': False,
            'error': f'Векторизация не удалась: {query_lips_data["error"]}',
            'test_filename': test_filename
        }

    print(f"✓ Тестовое изображение векторизовано за {vectorization_time}")
    print(f"📐 Размер вектора: {query_lips_data['vector_size']}")

    # Выполняем поиск в Qdrant
    search_start = datetime.now()

    try:
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_lips_data['vector'],
            limit=top_k,
            score_threshold=threshold,
            with_payload=True,
            with_vectors=False
        )

        search_time = datetime.now() - search_start

        results = []

        if not search_results:
            print("❌ Похожие губы не найдены")
        else:
            print(f"✓ Найдено {len(search_results)} похожих результатов:\n")

            for i, result in enumerate(search_results, 1):
                result_dict = {
                    'rank': i,
                    'id': result.id,
                    'score': result.score,
                    'payload': result.payload,
                    'lips_image_b64': result.payload.get('lips_image_b64', ''),
                    'landmarks': result.payload.get('landmarks', [])
                }

                results.append(result_dict)

                print(f"{i}. ID: {result.id}")
                print(f"   Схожесть: {result.score:.4f}")
                print(f"   Имя файла: {result.payload.get('name', 'не указано')}")
                print(f"   Дата загрузки: {result.payload.get('upload_date', 'неизвестно')}")
                print()

        end_time = datetime.now()
        total_time = end_time - start_time

        print(f"\n⏱️ Временная статистика:")
        print(f"   🧠 Векторизация: {vectorization_time}")
        print(f"   🔍 Поиск: {search_time}")
        print(f"   ⏱️ Общее время: {total_time}")

        return {
            'success': True,
            'test_filename': test_filename,
            'test_image_path': test_image_path,
            'query_lips_data': query_lips_data,
            'search_results': results,
            'total_found': len(results),
            'vectorization_time': vectorization_time,
            'search_time': search_time,
            'total_time': total_time
        }

    except Exception as e:
        print(f"❌ Ошибка при поиске: {str(e)}")
        return {
            'success': False,
            'error': f'Ошибка поиска: {str(e)}',
            'test_filename': test_filename
        }

def get_collection_info():
    """
    Получает информацию о коллекции

    Returns:
        dict: информация о коллекции
    """
    try:
        collection_info = qdrant_client.get_collection(collection_name)

        info = {
            'name': collection_name,
            'points_count': collection_info.points_count,
            'vector_size': collection_info.config.params.vectors.size,
            'distance': collection_info.config.params.vectors.distance,
            'status': collection_info.status
        }

        print(f"📊 Информация о коллекции '{collection_name}':")
        print(f"   📈 Количество точек: {info['points_count']}")
        print(f"   📐 Размер вектора: {info['vector_size']}")
        print(f"   📏 Метрика расстояния: {info['distance']}")
        print(f"   🟢 Статус: {info['status']}")

        return info

    except Exception as e:
        print(f"❌ Ошибка получения информации: {str(e)}")
        return {'error': str(e)}

print("🎯 Система инициализирована успешно!")
print(f"📊 Устройство: {device}")
print(f"🗄️ Коллекция: {collection_name}")
print(f"📐 Размер вектора: {vector_size}")
print("\n🛠️ Доступные функции:")
print("   - clear_collection() - очистка коллекции")
print("   - load_base_lips_to_qdrant() - загрузка базовых изображений")
print("   - search_from_test_directory() - поиск похожих губ")
print("   - get_collection_info() - информация о коллекции")