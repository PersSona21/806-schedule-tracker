from schedule_loader import ScheduleLoader
import argparse

text = """Пример:\n
python cli.py --group М8О-111БВ-24 --week 13 --subject "Экономическая теория" --date 07.05.2025 --type ЛК'"""

def parse_args():
    parser = argparse.ArgumentParser(description=text)
    
    parser.add_argument("--url", type=str, help="URL для загрузки расписания", required=False)
    parser.add_argument("--group", type=str, help="Группа к примеру М8О-111БВ-24", required=False)
    parser.add_argument("--week", type=str, help="Неделя", required=False)
    parser.add_argument("--subject", "-s", type=str, help='Предмет к примеру "Экономическая теория"', required=False)
    parser.add_argument("--date", type=str, help='Дата формата дд.мм.гггг', required=False)
    parser.add_argument("--type", type=str, help='Тип занятия ПЗ|ЛК|ЛР', required=False)
    return parser.parse_args()

def build_url(group: str, week :str =None) -> str:
    if week:
        base_url = "https://mai.ru/education/studies/schedule/index.php?group={group}&week={week}".format(group=group, week=week)
    else:
        base_url = "https://mai.ru/education/studies/schedule/index.php?group={group}".format(group=group)
    return base_url

def date_parse(date: str, year: int = 2025) -> str:
    month_map = {
    "янв": "01",
    "фев": "02",
    "мар": "03",
    "апр": "04",
    "мая": "05",
    "июн": "06",
    "июл": "07",
    "авг": "08",
    "сен": "09",
    "окт": "10",
    "ноя": "11",
    "дек": "12"}

    day_month = date.split(", ")[1]
    day, month_rus = day_month.split()
    month = month_map[month_rus.lower()]
    return f"{day}.{month}.{year}"

def main():
    args = parse_args()
    loader = ScheduleLoader()
    
    if args.url:
        url = args.url
    elif args.group:
        if args.week:
            url = build_url(args.group, args.week)
        else:
            url = build_url(args.group)
    else:
        print("Ошибка: Нужно передать либо URL, либо группу")
        return
    
    data = loader.get_cached_or_parse(url=url.rstrip('#'))
    filtered = data

    if args.date:
        filtered = [elem for elem in filtered if date_parse(elem.get('day')) == args.date]
    if args.subject:
        filtered = [elem for elem in filtered if elem.get('subject').lower() == args.subject.lower()]
    if args.type:
        filtered = [elem for elem in filtered if elem.get('lesson_type').lower() == args.type.lower()]
    for elem in filtered:
        print(elem)

    loader.close()

if __name__ == "__main__":
    main()