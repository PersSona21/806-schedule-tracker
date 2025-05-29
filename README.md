# 📅 806-Schedule-Tracker

🚀 **Автоматизация расписания МАИ**: парсит занятия с [mai.ru](https://mai.ru/education/studies/schedule/), сохраняет в PostgreSQL и синхронизирует с Google Calendar. Фильтруйте по предмету, дате или типу занятия через удобный CLI-интерфейс.

## ✨ Возможности
- 🕒 Парсинг расписания для группы и недели.
- 💾 Хранение данных в PostgreSQL.
- 📆 Синхронизация с Google Calendar.
- 🔍 Фильтрация по предмету, дате, типу (ЛК, ПЗ, ЛР).
- 📋 Вывод таблицы с опцией `--print`.

## 🛠 Технологии
- 🐍 **Python 3.8+**
- 🌐 **Selenium** (GeckoDriver)
- 🗄 **SQLAlchemy**
- ✅ **Pydantic**
- 📅 **Google API Client**
- 🐘 **PostgreSQL**
- 🎨 **Colorama**
- 📊 **Tabulate**

## ⚙️ Установка

1. **Клонируйте проект**:
   ```bash
   git clone https://github.com/your-username/806-schedule-tracker.git
   cd 806-schedule-tracker
   ```

2. **Создайте виртуальное окружение**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Установите зависимости**:
   ```bash
   pip install sqlalchemy psycopg2-binary pydantic colorama tabulate selenium google-api-python-client google-auth-oauthlib google-auth-httplib2
   ```

4. **Настройте PostgreSQL**:
   ```bash
   psql -U postgres
   ```
   ```sql
   CREATE DATABASE schedule_db;
   CREATE USER schedule_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE schedule_db TO schedule_user;
   ```

5. **Подключите Google Calendar API**:
   - Включите API в [Google Cloud Console](https://console.cloud.google.com/).
   - Скачайте `credentials.json` и поместите в корень проекта.
   - Укажите ID календаря в `google_calendar.py`.

6. **Установите GeckoDriver**:
   - Скачайте с [GitHub](https://github.com/mozilla/geckodriver/releases).
   - Добавьте в PATH: `mv geckodriver /usr/local/bin/`.

## 🚀 Использование

Запускайте через `cli.py` в активированном окружении.

- **Загрузка и синхронизация**:
  ```bash
  python cli.py --group М8О-111БВ-24 --week 13
  ```

- **Фильтрация с таблицей**:
  ```bash
  python cli.py --group М8О-111БВ-24 --week 13 --subject "Экономическая теория" --print
  ```

**Аргументы**:
- `--url`: URL расписания.
- `--group`: Код группы (М8О-111БВ-24).
- `--week`: Номер недели.
- `--subject`: Предмет.
- `--date`: Дата (дд.мм.гггг).
- `--type`: Тип (ЛК, ПЗ, ЛР).
- `--print`: Показать таблицу.

## 🔧 Если что-то пошло не так
- **Ошибка импорта**: Убедитесь, что в `database_manager.py` есть класс `DatabaseManager`.
- **Selenium не работает**: Проверьте GeckoDriver (`geckodriver --version`).
- **Google Calendar**: Проверьте `credentials.json` и ID календаря.