from schedule_loader import ScheduleLoader
from database_manager import Database_manager

if __name__ == "__main__":
    db = Database_manager()
    print("Начало загрузки расписания...")
    loader = ScheduleLoader()
    links = loader.get_links()

    # пример как заносить данные в базу данных
    try:
        link = "https://mai.ru/education/studies/schedule/index.php?group=%D0%9C8%D0%9E-111%D0%91%D0%92-24&week=14#"
        datas = loader.get_cached_or_parse(link)
        if datas is None:
            print(f"NONE для ссылки: {link}")
        for data in datas:
            db.add_lesson(lesson=data)
        
        print("Данные успешно загружены!")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        db.close()
    print("Данные загружены")