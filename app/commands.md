# Добавить файлы к коммиту
git add .

# Сделать коммит
git commit -m "Описание изменений"

# Отправить изменения на удалённый репозиторий
git push

pipenv install requests

# найти процессы питон
tasklist /FI "IMAGENAME eq python.exe"

# убить процесс
taskkill /F /PID 15696

docker exec -it weather_service_mongo mongosh -u root -p example --authenticationDatabase admin
show dbs                // показать базы
use weather_service      // выбрать базу
show collections         // показать коллекции
db.users.find().pretty() // вывести все документы из коллекции users

docker-compose down
docker-compose up --build -d  
docker compose up -d
