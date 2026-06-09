# Перейти в корневую папку проекта
cd C:\Users\H4Z\Desktop\TechnoWorld

# Сборка и запуск контейнеров
docker-compose up --build

# Для запуска в фоновом режиме:
docker-compose up -d --build

# Остановка:
docker-compose down

# Просмотр логов:
docker-compose logs -f

# Пересборка после изменений:
docker-compose up --build --force-recreate