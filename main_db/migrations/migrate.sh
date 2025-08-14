#!/bin/bash

# Поскольку скрипт находится в директории migrations, используем текущую директорию
MIGRATIONS_DIR=$(pwd)
DB_URL="postgres://postgres:Superdb777@localhost:5433/assistant?sslmode=disable"

case "$1" in
  "create")
    if [ -z "$2" ]; then
      echo "Usage: ./migrate.sh create <migration_name>"
      exit 1
    fi
    docker run --rm -v ${MIGRATIONS_DIR}:/migrations migrate/migrate:latest \
      create -ext sql -dir /migrations -seq "$2"
    ;;
  "up")
    cd ../.. && docker compose up db_migrations
    ;;
  "down")
    if [ -z "$2" ]; then
      # Откатить 1 миграцию
      docker run --rm -v ${MIGRATIONS_DIR}:/migrations migrate/migrate:latest \
        -path /migrations -database "${DB_URL}" down 1
    else
      # Откатить определённое количество миграций
      docker run --rm -v ${MIGRATIONS_DIR}:/migrations migrate/migrate:latest \
        -path /migrations -database "${DB_URL}" down "$2"
    fi
    ;;
  "goto")
    if [ -z "$2" ]; then
      echo "Usage: ./migrate.sh goto <version>"
      exit 1
    fi
    docker run --rm -v ${MIGRATIONS_DIR}:/migrations migrate/migrate:latest \
      -path /migrations -database "${DB_URL}" goto "$2"
    ;;
  "force")
    if [ -z "$2" ]; then
      echo "Usage: ./migrate.sh force <version>"
      exit 1
    fi
    docker run --rm -v ${MIGRATIONS_DIR}:/migrations migrate/migrate:latest \
      -path /migrations -database "${DB_URL}" force "$2"
    ;;
  "version")
    docker run --rm -v ${MIGRATIONS_DIR}:/migrations migrate/migrate:latest \
      -path /migrations -database "${DB_URL}" version
    ;;
  "drop")
    echo "⚠️  ВНИМАНИЕ: Это удалит ВСЕ таблицы! Введите 'yes' для подтверждения:"
    read confirmation
    if [ "$confirmation" = "yes" ]; then
      docker run --rm -v ${MIGRATIONS_DIR}:/migrations migrate/migrate:latest \
        -path /migrations -database "${DB_URL}" drop
    else
      echo "Операция отменена"
    fi
    ;;
  *)
    echo "Usage: ./migrate.sh {create|up|down|goto|force|version|drop}"
    echo ""
    echo "  create <name>     - создать новую миграцию"
    echo "  up               - применить все миграции"
    echo "  down [N]         - откатить N миграций (по умолчанию 1)"
    echo "  goto <version>   - перейти к определённой версии"
    echo "  force <version>  - принудительно установить версию БД"
    echo "  version          - показать текущую версию"
    echo "  drop             - удалить все таблицы (ОПАСНО!)"
    echo ""
    echo "Примеры:"
    echo "  ./migrate.sh create add_users_table"
    echo "  ./migrate.sh down 3        # откатить 3 последние миграции"
    echo "  ./migrate.sh goto 5        # перейти к версии 5"
    ;;
esac 