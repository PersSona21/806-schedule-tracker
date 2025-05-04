# CS806 Schedule Tracker

Веб-сервис для отслеживания и управления занятостью компьютерных аудиторий кафедры 806 МАИ.  
Проект автоматически собирает расписание с сайта МАИ, сохраняет его в локальную базу данных и синхронизирует с Google Calendar или Google Таблицами для удобного доступа.

---

## 🚀 Возможности

- 🔍 **Сбор расписания** с сайта МАИ с помощью Selenium
- 🗃️ **Хранение данных** в базе (SQLite или PostgreSQL)
- 📅 **Интеграция с Google Calendar** — синхронизация расписаний по аудиториям
- 📊 **Экспорт в Google Таблицы** — генерация табличного вида расписания
- 🔄 **Обновление только при изменениях** — предотвращение дублирования событий
- 🖥️ **CLI-инструмент** для загрузки и управления расписанием

---

## 🛠️ Технологии

- **Backend**: Python 3.x
- **Парсинг**: Selenium, BeautifulSoup
- **База данных**: PostgreSQL
- **Интеграция с Google**: Google Calendar API, Google Sheets API
- **CLI**: `argparse`
- **Кэширование**: Локальное сохранение в виде Json

---

## 📦 Установка

```bash
git clone https://github.com/yourusername/cs806-schedule-tracker.git
cd cs806-schedule-tracker
python -m venv venv
source venv/bin/activate  # В Windows: venv\Scripts\activate
pip install -r requirements.txt

