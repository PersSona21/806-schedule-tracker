from schedule_loader import ScheduleLoader
from database_manager import Database_manager

if __name__ == "__main__":
    db = Database_manager()
    print("Начало загрузки расписания...")
    loader = ScheduleLoader()
    links = loader.get_links()

    # пример как заносить данные в базу данных
    try:
        for link in links:
            datas = loader.get_cached_or_parse(link)
            if datas is None:
                print(f"NONE для ссылки: {link}")
                continue
            for data in datas:
                data["start_time"] = "test"
                data["end_time"] = "test2"
                print(data)
                db.add_lesson(lesson=data)
        
        print("Данные успешно загружены!")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        db.close()
    print("Данные загружены")