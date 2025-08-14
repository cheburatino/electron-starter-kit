# Создать новую миграцию
./migrate.sh create add_users_table

# Применить все миграции
./migrate.sh up

# Откатить последнюю миграцию
./migrate.sh down

# Откатить 3 последние миграции
./migrate.sh down 3

# Перейти к конкретной версии (например, к версии 5)
./migrate.sh goto 5

# Посмотреть текущую версию
./migrate.sh version

# Принудительно установить версию (если что-то сломалось)
./migrate.sh force 3

# Удалить все таблицы (ОСТОРОЖНО!)
./migrate.sh drop