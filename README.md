## Как запустить проект

### 1. Клонировать репозиторий
```bash
git clone https://github.com/MaxOn4ik1/my-first-project.git
cd my-first-project
```

### 2. Создать и активировать виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/Mac
# venv\Scripts\activate   # Для Windows
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Настроить переменные окружения
Создайте файл `.env` в корне проекта:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=octagon_db
DB_USER=octagon
DB_PASSWORD=12345
```

### 5. Инициализировать базу данных
```bash
python app/init_db.py
```

### 6. Запустить сервер
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Открыть в браузере
```
http://127.0.0.1:8000/docs
```