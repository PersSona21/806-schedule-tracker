from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from datetime import datetime, timedelta

# Конфигурация
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = r"C:\Users\Кирилл\Desktop\учеб\Python_project\calendar\credentials.json"  # Путь к JSON-ключу
CALENDAR_ID = "649729f42af022a458dbf43bfa0cf12eea5e98a45c4bd10833e8e6134d42f3ec@group.calendar.google.com"  # ID календаря

# Загрузка учетных данных
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Создание клиента Google Calendar API
service = build("calendar", "v3", credentials=credentials)


from database import Session, Schedule






def create_event(audience: str, subject: str, teacher: str, start_time: str, end_time: str, date: str, recurrence: str = None):
    """
    Добавляет событие в Google Calendar.
    
    Параметры:
    - audience: Аудитория
    - subject: Название предмета
    - teacher: Преподаватель
    - start_time: Время начала (формат "HH:MM")
    - end_time: Время окончания (формат "HH:MM")
    - date: Дата (формат "YYYY-MM-DD")
    - recurrence: Повторение ("even_week", "odd_week", None)
    """
    event = {
        "summary": f"{subject} ({teacher})",
        "location": f"Аудитория {audience}",
        "start": {
            "dateTime": f"{date}T{start_time}:00+03:00",  # UTC+3 (Москва)
            "timeZone": "Europe/Moscow",
        },
        "end": {
            "dateTime": f"{date}T{end_time}:00+03:00",
            "timeZone": "Europe/Moscow",
        },
    }

    # Настройка повторений
    if recurrence == "even_week":
        event["recurrence"] = ["RRULE:FREQ=WEEKLY;INTERVAL=2"]
    elif recurrence == "odd_week":
        event["recurrence"] = ["RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,TU,WE,TH,FR"]

    # Отправка запроса
    try:
        event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"Событие создано: {event.get('htmlLink')}")
    except Exception as e:
        print(f"Ошибка: {e}")


def sync_db_to_calendar():
    session = Session()
    unsynced_events = session.query(Schedule).filter_by(is_synced=False).all()

    for event in unsynced_events:
        create_event(
            audience=event.audience,
            subject=event.subject,
            teacher=event.teacher,
            start_time=event.start_time,
            end_time=event.end_time,
            date=event.day,
            recurrence=event.recurrence
        )
        event.is_synced = True
        session.commit()


sync_db_to_calendar()

def get_events(date: str):
    """
    Возвращает все события на указанную дату.
    """
    start = f"{date}T00:00:00+03:00"
    end = f"{date}T23:59:59+03:00"
    
    events_result = (
        service.events()
        .list(
            calendarId=CALENDAR_ID,
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    
    return events_result.get("items", [])


def delete_event(event_id: str):
    """
    Удаляет событие по его ID.
    """
    try:
        service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        print(f"Событие {event_id} удалено.")
    except Exception as e:
        print(f"Ошибка: {e}")


