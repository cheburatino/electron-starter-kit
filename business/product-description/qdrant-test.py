# Ниже предоставляю 2 блока кода, которые есть на текущий момент в ноутбуке. Напиши третий блок кода, который будет принимать поисковый запрос, преобразовывать его в вектор с помощью той же модели (из первого блока) и искать похожие векторы в коллекции.

# Блок 1:
# Получение эмбеддингов 

from transformers import AutoTokenizer, AutoModel
import torch
import os
import numpy as np

# Проверяем наличие директории
input_dir = '/content/rk_products'
if not os.path.exists(input_dir):
    raise FileNotFoundError(f"Директория {input_dir} не найдена!")

# Инициализация модели
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_name = 'DeepPavlov/rubert-base-cased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)
model.eval()

vector_list = []

# Обработка каждого файла
for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):  # Работаем только с txt-файлами
        file_path = os.path.join(input_dir, filename)

        # Чтение файла
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()

        # Получение вектора
        with torch.no_grad():
            inputs = tokenizer(
                text,
                return_tensors='pt',
                truncation=True,
                padding='max_length',
                max_length=512
            ).to(device)
            outputs = model(**inputs)
            vector = outputs.last_hidden_state[:, 0, :].cpu().numpy().tolist()[0]  # Берем [CLS] токен

        # Формируем запись
        doc_name = os.path.splitext(filename)[0]
        vector_list.append({
            'doc_name': doc_name,
            'text': text,
            'vector': vector,
            'url': ''  # Пустая строка для последующего заполнения
        })

# Убедимся, что векторы представлены как списки чисел (не torch.Tensor/numpy)
for item in vector_list:
    # Если вектор еще не список - конвертируем
    if isinstance(item['vector'], torch.Tensor):
        item['vector'] = item['vector'].cpu().numpy().tolist()
    elif isinstance(item['vector'], np.ndarray):
        item['vector'] = item['vector'].tolist()
    
    # Добавим text_size в payload
    item['text_size'] = len(item['text'])

# Вывод результатов
for item in vector_list:
    print(f"doc_name: {item['doc_name']}")
    print(f"Длина текста: {len(item['text'])} символов")
    print(f"Вектор присутствует: {bool(item['vector'])}")
    print("-" * 50)

print(f"\nОбработано файлов: {len(vector_list)}")

# Блок 2:
!pip install qdrant-client  # Установим клиент если нужно

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
import uuid

# Создаем клиент в оперативной памяти
client = QdrantClient(":memory:")

# Параметры коллекции
COLLECTION_NAME = "rk_products"
VECTOR_SIZE = 768  # Размерность векторов rubert

# Создаем коллекцию
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE  # Косинусное расстояние для семантического поиска
    )
)

# Подготовим точки для загрузки
points = []
for item in vector_list:
    points.append(PointStruct(
        id=str(uuid.uuid4()),  # Генерируем уникальный ID
        vector=item['vector'],
        payload={
            "doc_name": item['doc_name'],
            "text": item['text'],
            "text_size": item['text_size'],
            "url": item['url']
        }
    ))

# Загружаем данные в коллекцию
operation_info = client.upsert(
    collection_name=COLLECTION_NAME,
    wait=True,
    points=points
)

print(f"\nСтатус загрузки: {operation_info.status}")
print(f"Загружено точек: {len(points)}")

# Проверяем коллекцию
collection_info = client.get_collection(COLLECTION_NAME)
print(f"\nИнформация о коллекции:")
print(f"Количество точек: {collection_info.points_count}")
print(f"Размерность векторов: {collection_info.config.params.vectors.size}")
print(f"Метрика расстояния: {collection_info.config.params.vectors.distance}")
