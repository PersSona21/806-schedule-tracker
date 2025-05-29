from schedule_loader import ScheduleLoader
from database_manager import Database_manager
from google_calendar import sync_db_to_calendar
import argparse
from tabulate import tabulate
from colorama import init, Fore, Style

# Инициализация colorama для цветного вывода
init(autoreset=True)

text = """Пример:
python cli.py --group М8О-111БВ-24 --week 13 --subject "Экономическая теория" --date 07.05.2025 --type ЛК --print
python cli.py --group М8О-111БВ-24 --week 13"""

def parse_args():
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument("--url", type=str, help="URL для загрузки расписания", required=False)
    parser.add_argument("--group", type=str, help="Группа, например М8О-111БВ-24", required=False)
    parser.add_argument("--week", type=str, help="Неделя", required=False)
    parser.add_argument("--subject", "-s", type=str, help='Предмет, например "Экономическая теория"', required=False)
    parser.add_argument("--date", type=str, help='Дата формата дд.мм.гггг', required=False)
    parser.add_argument("--type", type=str, help='Тип занятия ПЗ|ЛК|ЛР', required=False)
    parser.add_argument("--print", action="store_true", help="Выводить данные в консоль в виде таблицы")
    return parser.parse_args()

def build_url(group: str, week: str = None) -> str:
    if week:
        return f"https://mai.ru/education/studies/schedule/index.php?group={group}&week={week}"
    return f"https://mai.ru/education/studies/schedule/index.php?group={group}"

def date_parse(date: str, year: int = 2025) -> str:
    month_map = {
        "янв": "01", "фев": "02", "мар": "03", "апр": "04", "мая": "05", "июн": "06",
        "июл": "07", "авг": "08", "сен": "09", "окт": "10", "ноя": "11", "дек": "12"
    }
    try:
        if not date or date.strip() == "":
            return ""
        day_month = date.split(", ")[1]
        day, month_rus = day_month.split()
        month = month_map[month_rus.lower()]
        return f"{year}-{month}-{day.zfill(2)}"
    except Exception as e:
        return ""

def main():
    args = parse_args()
    loader = ScheduleLoader()
    db = Database_manager()

    # Формирование URL
    if args.url:
        url = args.url
    elif args.group:
        url = build_url(args.group, args.week)
    else:
        print(f"{Fore.RED}Ошибка: Нужно передать либо URL, либо группу{Style.RESET_ALL}")
        return

    try:
        # Загрузка данных
        data = loader.get_cached_or_parse(url.rstrip('#'))
        if not data:
            print(f"{Fore.YELLOW}Нет данных для URL {url}{Style.RESET_ALL}")
            return

        # Сохранение в базу данных
        for item in data:
            item['day'] = date_parse(item.get('day', ''))
            if not item['day']:  # Пропускаем записи с пустой датой
                continue
            db.add_lesson(lesson=item)

        # Синхронизация с Google Calendar
        sync_db_to_calendar()

        # Фильтрация данных
        filtered = data
        if args.date:
            filtered = [elem for elem in filtered if elem.get('day') == args.date]
        if args.subject:
            filtered = [elem for elem in filtered if elem.get('subject').lower() == args.subject.lower()]
        if args.type:
            filtered = [elem for elem in filtered if elem.get('lesson_type').lower() == args.type.lower()]

        # Вывод в консоль
        if args.print:
            if filtered:
                table_data = [
                    [
                        elem['day'],
                        elem['subject'],
                        elem['lesson_type'],
                        f"{elem['start_time']} - {elem['end_time']}",
                        ", ".join(elem['teachers']) if isinstance(elem['teachers'], list) else elem['teachers'],
                        elem['location']
                    ]
                    for elem in filtered if elem.get('day')
                ]
                headers = [
                    Fore.CYAN + "День" + Style.RESET_ALL,
                    Fore.CYAN + "Предмет" + Style.RESET_ALL,
                    Fore.CYAN + "Тип" + Style.RESET_ALL,
                    Fore.CYAN + "Время" + Style.RESET_ALL,
                    Fore.CYAN + "Преподаватели" + Style.RESET_ALL,
                    Fore.CYAN + "Аудитория" + Style.RESET_ALL
                ]
                print(f"\n{Fore.GREEN}Расписание:{Style.RESET_ALL}")
                print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
            else:
                print(f"{Fore.YELLOW}Нет данных, соответствующих фильтрам.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
    finally:
        loader.close()
        db.close()

if __name__ == "__main__":
    main()