1. Остановить все контейнеры
docker stop $(docker ps -aq)

2. Удалить все контейнеры
docker rm $(docker ps -aq)

3. Удалить все образы
docker rmi $(docker images -q)

4. Удалить все volumes
docker volume rm $(docker volume ls -q)

5. Удалить все сети
docker network rm $(docker network ls -q)

6. Полная очистка системы (всё сразу)
docker system prune -a --volumes
Флаги для system prune:
-a - удаляет ВСЕ неиспользуемые образы (не только dangling)
--volumes - удаляет неиспользуемые volumes
--force - не спрашивает подтверждения

7. Самая радикальная очистка
docker system prune -a --volumes --force
docker builder prune --all --force