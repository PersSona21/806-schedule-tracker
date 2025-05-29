import re
import json
import os
import hashlib
from selenium import webdriver
from urllib.parse import unquote
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

mai_url = "https://mai.ru/education/studies/schedule/"

class ScheduleLoader:
    
    def __init__(self):
        os.makedirs("cache", exist_ok=True)
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=self.options)
    
    def get_links(self, url="https://clck.ru/3LYESN") -> list[str]:
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn.btn-soft-secondary.btn-xs.mb-1.fw-medium.btn-group"))
        )
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "a.btn.btn-soft-secondary.btn-xs.mb-1.fw-medium.btn-group")
        hrefs = [unquote(btn.get_attribute("href")) for btn in buttons if btn.get_attribute("href")]
        return hrefs

    def _get_cache_filename(self, url: str) -> str:
        hashed = hashlib.md5(unquote(url).encode("utf-8")).hexdigest()
        return os.path.join("cache", f"{hashed}.json")

    def _load_from_cache(self, url: str) -> list[dict] | None:
        path = self._get_cache_filename(url)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def _save_to_cache(self, url: str, data: list[dict]):
        path = self._get_cache_filename(url)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_cached_or_parse(self, url: str) -> list[dict]:
        cached = self._load_from_cache(url)
        if cached:
            return cached
        data = self._parse_week_schedule(url)
        if data:
            self._save_to_cache(url, data)
        return data

    def _parse_week_schedule(self, url: str) -> list[dict]:
        try:
            self.driver.get(mai_url)  # Устанавливаем куки
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.step > li.step-item"))
            )
            days = self.driver.find_elements(By.CSS_SELECTOR, "ul.step > li.step-item")
            all_lessons = []

            for day in days:
                try:
                    day_title = day.find_element(By.CLASS_NAME, "step-title").text.strip()
                    lesson_blocks = day.find_elements(By.CSS_SELECTOR, "div.mb-4")

                    for block in lesson_blocks:
                        try:
                            raw_subject = block.find_element(By.CSS_SELECTOR, "p.fw-semi-bold").text.strip()
                            match = re.search(r"(.*)\s+(ПЗ|ЛК|ЛР)$", raw_subject)
                            if match:
                                subject = match.group(1).strip()
                                lesson_type = match.group(2)
                            else:
                                subject = raw_subject
                                lesson_type = "Неизвестно"

                            info_items = block.find_elements(By.CSS_SELECTOR, "ul > li")
                            text_info = [elem.text.strip() for elem in info_items]
                            # print(f"Извлечённые данные info_items: {text_info}")  # Отладка

                            if len(text_info) > 2:
                                time = text_info[0]
                                teachers = text_info[1:-1]
                                location = text_info[-1]
                            elif len(text_info) == 2:
                                time = text_info[0]
                                teachers = ["Неизвестно"]
                                location = text_info[1]
                            elif len(text_info) == 1:
                                time = text_info[0]
                                teachers = ["Неизвестно"]
                                location = "Неизвестно"
                            else:
                                time = "Неизвестно"
                                teachers = ["Неизвестно"]
                                location = "Неизвестно"

                            # Разделяем время на start_time и end_time
                            try:
                                if time and " – " in time:
                                    start_time, end_time = time.split(" – ")
                                    start_time = start_time.strip()
                                    end_time = end_time.strip()
                                else:
                                    print(f"Некорректное время: {time}")
                                    start_time = "00:00"
                                    end_time = "00:00"
                            except ValueError as e:
                                print(f"Ошибка при разборе времени '{time}': {e}")
                                start_time = "00:00"
                                end_time = "00:00"

                            all_lessons.append({
                                "day": day_title,
                                "subject": subject,
                                "lesson_type": lesson_type,
                                "start_time": start_time,
                                "end_time": end_time,
                                "teachers": teachers,
                                "location": location
                            })

                        except Exception as e:
                            print(f"Ошибка при обработке занятия: {e}")
                except Exception as e:
                    print(f"Ошибка при обработке дня: {e}")
            return all_lessons
        except Exception as e:
            print(f"Ошибка: {e}")
            return []

    def format_json(self, url: str) -> None:
        with open("output.json", "w", encoding="UTF-8") as file_out:
            json.dump(self._parse_week_schedule(url), file_out, ensure_ascii=False, indent=2)

    def close(self):
        self.driver.quit()