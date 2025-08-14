# flutter/Dockerfile

FROM debian:stable-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    xz-utils \
    libglu1-mesa \
    && rm -rf /var/lib/apt/lists/*

# Установка Flutter
RUN git clone https://github.com/flutter/flutter.git /flutter
ENV PATH="/flutter/bin:${PATH}"

# Предварительная настройка Flutter для веб
RUN flutter doctor && \
    flutter config --enable-web

# Создание рабочей директории
WORKDIR /app

# Копирование проекта
COPY . /app/

# Установка сервера для раздачи статики
RUN apt-get update && apt-get install -y \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Запуск на порту 7000
EXPOSE 7000
CMD ["sh", "-c", "flutter pub get && flutter build web && cd build/web && python3 -m http.server 7000"] 