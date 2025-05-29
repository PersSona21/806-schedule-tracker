from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from postgresql.database import SessionLocal
from postgresql.models import Schedule
import datetime

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "credentials.json"
CALENDAR_ID = "eee4bfd713a748c37944a121c2dc881af521dc32d2316bde65d4e759e48cf727@group.calendar.google.com"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("calendar", "v3", credentials=credentials)

def validate_date(date_str: str) -> str:
    """Преобразует дату в формат YYYY-MM-DD, если возможно."""
    try:
        if not date_str or date_str.strip() == "":
            raise ValueError("Дата не может быть пустой")
        if "." in date_str:
            day, month, year = date_str.split(".")
            date_str = f"{year}-{month}-{day}"
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError as e:
        raise ValueError(f"Некорректный формат даты {date_str}: {e}")

def create_event(audience: str, subject: str, teacher: str, start_time: str, end_time: str, date: str, recurrence: str = None):
    try:
        date = validate_date(date)
        datetime.datetime.strptime(start_time, "%H:%M")
        datetime.datetime.strptime(end_time, "%H:%M")

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

        event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        return event
    except HttpError as e:
        print(f"Ошибка HTTP при создании события: {e}")
        raise
    except Exception as e:
        raise

def sync_db_to_calendar():
    db = SessionLocal()
    failed = False
    try:
        unsynced_events = db.query(Schedule).filter_by(is_synced=False).all()
        if not unsynced_events:
            return

        for event in unsynced_events:
            try:
                if not event.day or event.day.strip() == "":
                    continue  # Пропускаем записи с пустой датой
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
            except Exception:
                failed = True
                continue

        if failed:
            print("Синхронизация завершена с ошибками.")
    except Exception as e:
        print(f"Ошибка синхронизации: {e}")
        failed = True
    finally:
        db.close()
        if failed:
            raise Exception("Синхронизация не удалась из-за ошибок.")

def get_events(date: str):
    try:
        start = f"{validate_date(date)}T00:00:00+03:00"
        end = f"{validate_date(date)}T23:59:59+03:00"

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
    except Exception as e:
        print(f"Ошибка получения событий: {e}")
        return []

def delete_event(event_id: str):
    try:
        service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        print(f"Событие {event_id} удалено.")
    except Exception as e:
        print(f"Ошибка: {e}")
