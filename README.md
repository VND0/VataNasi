# VataNasi
###### Сайт для изучения иностранных слов

## Запуск
### Без Docker
```bash
# Клонировать репозиторий
git clone https://github.com/VND0/VataNasi

# Установить зависимости
cd VataNasi
python3 -m venv venv
source venv/bin/activate
pip3 install flask flask_login sqlalchemy

# Создать секретный ключ
echo "Your OWN AND VERY COMPLICATED secret key" > secret_key.txt

# Запустить сервер
python3 app.py
```
### С Docker
```bash
# Клонировать репозиторий
git clone https://github.com/VND0/VataNasi

# Построить образ
cd VataNasi
docker build -t vata-nasi .

# Присоединить БД, секретный ключ и запустить
touch data.db
echo "Your OWN AND VERY COMPLICATED secret key" > secret_key.txt

docker run -p 80:80 -v "$(pwd)/secret_key.txt:/app/secret_key.txt" \
-v "$(pwd)/data.db:/app/data.db" -i vata-nasi
```