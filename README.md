# 📅 806-Schedule-Tracker

🚀 Автоматизирует расписание МАИ: парсит занятия с [mai.ru](https://mai.ru/education/studies/schedule/), сохраняет в PostgreSQL, синхронизирует с Google Calendar и показывает занятость аудиторий в реальном времени через веб-интерфейс.

## ✨ Возможности
- 🕒 Парсинг расписания для группы и недели.
- 💾 Хранение в PostgreSQL.
- 📆 Синхронизация с Google Calendar.
- 🔍 Фильтрация по предмету, дате, типу (ЛК, ПЗ, ЛР).
- 🌐 Веб-интерфейс для проверки занятости аудиторий `IT1`–`IT19` в реальном времени.

## 🛠 Технологии
- 🐍 Python 3.8+
- 🌐 Selenium (GeckoDriver)
- 🗄 SQLAlchemy
- ✅ Pydantic
- 📅 Google API Client
- 🐘 PostgreSQL
- 🎨 Colorama
- 📊 Tabulate
- ⚡ Flask

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
   pip install -r requirements.txt
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

5. **Настройте Google Calendar API**:
   - Включите API в [Google Cloud Console](https://console.cloud.google.com/).
   - Скачайте `credentials.json` в корень проекта.
   - Укажите ID календаря в `google_calendar.py`.

6. **Установите GeckoDriver**:
   - Скачайте с [GitHub](https://github.com/mozilla/geckodriver/releases).
   - Добавьте в PATH: `mv geckodriver /usr/local/bin/`.

## 🚀 Использование

### Парсинг и синхронизация
Запустите в активированном окружении:
```bash
python cli.py --group М8О-111БВ-24 --week 13
```

### Фильтрация с выводом
```bash
python cli.py --group М8О-111БВ-24 --week 13 --subject "Экономическая теория" --print
```

**Аргументы**:
- `--url`: URL расписания.
- `--group`: Код группы.
- `--week`: Номер недели.
- `--subject`: Предмет.
- `--date`: Дата (дд.мм.гггг).
- `--type`: Тип (ЛК, ПЗ, ЛР).
- `--print`: Показать таблицу.

### Проверка занятости аудиторий
Запустите веб-интерфейс:
```bash
python auditorium_status.py
```
Откройте `http://localhost:5021` для просмотра статуса аудиторий `IT1`–`IT19` в реальном времени.

## 🔧 Устранение неполадок
- **Парсинг не работает**: Проверьте GeckoDriver (`geckodriver --version`).
- **Веб-страница недоступна**: Убедитесь, что порт `5021` свободен.
- **Google Calendar**: Проверьте `credentials.json` и ID календаря.
- **Старые аудитории**: Очистите кэш (`rm -rf cache/*`) и обновите базу:
  ```sql
  UPDATE schedule SET location = 'IT1' WHERE location = 'ГУК Б-422';
  -- Повторите для IT2–IT19
  ```