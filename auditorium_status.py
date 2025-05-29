from flask import Flask, render_template
from postgresql.database import SessionLocal
from postgresql.models import Schedule
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import and_

app = Flask(__name__)

# Список аудиторий
AUDITORIUMS = [f"IT{i}" for i in range(1, 20)]

def get_auditorium_status():
    """Проверяет статус аудиторий (занята/свободна) на текущий момент."""
    db = SessionLocal()
    try:
        # Текущее время в Москве (UTC+3)
        moscow_tz = ZoneInfo("Europe/Moscow")
        now = datetime.now(moscow_tz)
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M")

        status_list = []
        for auditorium in AUDITORIUMS:
            # Ищем занятия в данной аудитории на текущую дату и время
            lesson = db.query(Schedule).filter(
                and_(
                    Schedule.location == auditorium,
                    Schedule.day == current_date,
                    Schedule.start_time <= current_time,
                    Schedule.end_time >= current_time
                )
            ).first()

            # Формируем статус
            status = {
                "auditorium": auditorium,
                "is_occupied": bool(lesson),
                "status_text": "Занята" if lesson else "Свободна",
                "color": "red" if lesson else "green"
            }
            status_list.append(status)

        return status_list
    finally:
        db.close()

@app.route("/")
def index():
    """Отображает веб-страницу со статусом аудиторий."""
    statuses = get_auditorium_status()
    return render_template("index.html", statuses=statuses)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5021)