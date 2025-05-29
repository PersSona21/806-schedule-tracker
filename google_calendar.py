from google.oauth2 import service_account
from googleapiclient.discovery import build

from postgresql.database import SessionLocal
from postgresql.models import Schedule

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "credentials.json"
CALENDAR_ID = "ddd06c1c181506d4be60b744ee077ac3c01f0dd12f1d5b26a15fb19ad4ae813f@group.calendar.google.com"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("calendar", "v3", credentials=credentials)

def create_event(audience: str, subject: str, teacher: str, start_time: str, end_time: str, date: str, recurrence: str = None):
    event = {
        "summary": f"{subject} ({teacher})",
        "location": f"Аудитория {audience}",
        "start": {
            "dateTime": f"{date}T{start_time}:00+03:00",
            "timeZone": "Europe/Moscow",
        },
        "end": {
            "dateTime": f"{date}T{end_time}:00+03:00",
            "timeZone": "Europe/Moscow",
        },
    }

    if recurrence == "even_week":
        event["recurrence"] = ["RRULE:FREQ=WEEKLY;INTERVAL=2"]
    elif recurrence == "odd_week":
        event["recurrence"] = ["RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,TU,WE,TH,FR"]

    try:
        event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"Событие создано: {event.get('htmlLink')}")
    except Exception as e:
        print(f"Ошибка: {e}")

def sync_db_to_calendar():
    db = SessionLocal()
    try:
        unsynced_events = db.query(Schedule).filter_by(is_synced=False).all()
        for event in unsynced_events:
            create_event(
                audience=event.location,
                subject=event.subject,
                teacher=event.teachers,
                start_time=event.start_time,
                end_time=event.end_time,
                date=event.day,
                recurrence=event.recurrence
            )
            event.is_synced = True
            db.commit()
    except Exception as e:
        print(f"Ошибка синхронизации: {e}")
    finally:
        db.close()

def get_events(date: str):
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
    try:
        service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        print(f"Событие {event_id} удалено.")
    except Exception as e:
        print(f"Ошибка: {e}")
