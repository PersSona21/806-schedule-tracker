from schedule_loader import ScheduleLoader
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Скачивание расписания МАИ с кэшированием')
    
    parser.add_argument("--url", type=str, help="URL для загрузки расписания", required=False)
    parser.add_argument("--group", type=str, help="Группа для формирования URL", required=False)
    parser.add_argument("--week", type=str, help="Неделя для формирования URL", required=False)
    
    return parser.parse_args()


def build_url(group, week=None):
    if week:
        base_url = "https://mai.ru/education/studies/schedule/index.php?group={group}&week={week}".format(group=group, week=week)
    else:
        base_url = "https://mai.ru/education/studies/schedule/index.php?group={group}".format(group=group)
    return base_url


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
    
    for elem in loader.get_cached_or_parse(url=url.rstrip('#')):
        print(elem)
    
    loader.close()


if __name__ == "__main__":
    main()