FROM migrate/migrate:latest

WORKDIR /migrations

COPY . .

# Создаем entrypoint скрипт
RUN echo '#!/bin/sh' > /entrypoint.sh && \
    echo 'sleep 10' >> /entrypoint.sh && \
    echo 'migrate -path /migrations -database "postgres://postgres:Superdb777@main_db:5432/assistant?sslmode=disable" up' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]