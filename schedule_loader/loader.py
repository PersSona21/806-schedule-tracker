import re
from selenium import webdriver
from urllib.parse import unquote
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

mai_url = "https://mai.ru/education/studies/schedule/"

def get_links() -> list:
    
    url = "https://clck.ru/3LYESN"
    
    options = Options()
    options.add_argument("--headless")

    # Запуск браузера
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    # Ждём, пока кнопки появятся
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.btn.btn-soft-secondary.btn-xs.mb-1.fw-medium.btn-group"))
    )

    # Ищем все подходящие кнопки
    buttons = driver.find_elements(By.CSS_SELECTOR, "a.btn.btn-soft-secondary.btn-xs.mb-1.fw-medium.btn-group")

    # Собираем ссылки
    hrefs = [unquote(btn.get_attribute("href")) for btn in buttons if btn.get_attribute("href")]
    driver.quit()
    return hrefs


def parse_week_schedule(url: str) -> list:
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(mai_url)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.step > li.step-item"))
        )

        days = driver.find_elements(By.CSS_SELECTOR, "ul.step > li.step-item")
        all_lessons = []

        for day in days:
            try:
                day_title = day.find_element(By.CLASS_NAME, "step-title").text.strip()
                lesson_blocks = day.find_elements(By.CSS_SELECTOR, "div.mb-4")

                for block in lesson_blocks:
                    try:
                        raw_subject = block.find_element(By.CSS_SELECTOR, "p.fw-semi-bold").text.strip()

                        # Выделяем тип занятия
                        match = re.search(r"(.*)\s+(ПЗ|ЛК|ЛР)$", raw_subject)
                        if match:
                            subject = match.group(1).strip()
                            lesson_type = match.group(2)
                        else:
                            subject = raw_subject
                            lesson_type = "Неизвестно"

                        info_items = block.find_elements(By.CSS_SELECTOR, "ul > li")
                        text_info = [elem.text.strip() for elem in info_items]
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
                        
                        all_lessons.append({
                            "day": day_title,
                            "subject": subject,
                            "lesson_type": lesson_type,
                            "time": time,
                            "teachers": teachers,
                            "location": location
                        })

                    except Exception as e:
                        print(f"Ошибка при обработке занятия: {e}")
            except Exception as e:
                print(f"Ошибка при обработке дня: {e}")

        return all_lessons

    finally:
        driver.quit()