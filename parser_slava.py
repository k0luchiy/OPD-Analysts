from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Функция для закрытия всплывающего окна

def close_popup(driver):
    try:
        # print("Проверяем наличие всплывающего окна...")
        # Используем WebDriverWait для ожидания появления кнопки закрытия
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "modal-regions-close"))
        )
        # Прокрутка к кнопке (если она не в зоне видимости)
        driver.execute_script(
            "arguments[0].scrollIntoView(true);", close_button)
        # Клик по кнопке крестика
        close_button.click()
        # print("Всплывающее окно успешно закрыто.")
    except Exception as e:
        pass
        # print(f"Ошибка при закрытии всплывающего окна: {e}")

# Основной скрипт


def parse(name_of_laptop):
    # Настроим веб-драйвер
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Открываем сайт
        driver.get("https://n-katalog.ru/")
        # print("Сайт открыт...")

        # Закрываем всплывающее окно
        close_popup(driver)

        # Ищем поле ввода
        # print("Ищем поле ввода...")
        textarea = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#ek-search"))
        )
        # Прокрутка к полю ввода
        driver.execute_script("arguments[0].scrollIntoView(true);", textarea)
        textarea.click()

        # Вводим запрос
        textarea.send_keys(name_of_laptop)
        # print("Запрос введен.")

        # Нажимаем кнопку поиска
        # print("Нажимаем кнопку поиска...")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-lups"))
        )
        submit_button.click()
        # print("Поиск выполнен.")

        # print("Ожидаем загрузки результатов...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#ek-search__res-wrap"))
        )
        first_laptop_link = driver.find_element(
            By.CSS_SELECTOR, ".model-short-info a")
        link = first_laptop_link.get_attribute("href")
        
        #print("Ссылка на ноутбук:", link)
        # print("Результаты найдены!")
        return link

    except Exception as e:
        pass
        # print(f"Ошибка в основном скрипте: {e}")
    finally:
        # Закрываем браузер
        # print("Закрываем браузер...")
        driver.quit()


# Запуск
if __name__ == "__main__":
    parse("Huawei matebook 16s")
