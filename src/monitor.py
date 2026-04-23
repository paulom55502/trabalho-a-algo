import time
import re
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager



def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    return driver




def extract_number(text):
    if not text:
        return None

    text = text.strip()

    text = text.replace(".", "")

    text = text.replace(",", ".")

    match = re.search(r"\d+(\.\d+)?", text)

    if match:
        return float(match.group())

    return None



def find_price_on_page(driver, field_hint):
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, field_hint)

        if not elements:
            elements = driver.find_elements(By.XPATH, "//*")

        for el in elements:
            text = el.text.strip()

            if not text:
                continue


            if "." not in field_hint and "#" not in field_hint:
                if field_hint.lower() not in text.lower():
                    continue

            value = extract_number(text)

            if value is not None:
                logging.info(f"[FIND] Valor encontrado: {value} | Texto: {text[:30]}")
                return {"value": value}

    except Exception as e:
        logging.warning(f"[FIND] Erro ao buscar: {e}")

    return None



def monitor_price(url, field_hint, interval, timeout, on_change, stop_event):
    logging.info(f"[MONITOR] Monitorando (Selenium) em {url}")

    driver = create_driver()
    driver.get(url)

    time.sleep(5)

    last_value = None

    try:
        while not stop_event.is_set():

            result = find_price_on_page(driver, field_hint)

            if result is None:
                logging.warning("[MONITOR] Campo não encontrado")
            else:
                value = result["value"]

                if last_value is None:
                    last_value = value
                    logging.info(f"[MONITOR] Preço inicial: {value}")

                elif value != last_value:
                    logging.info(f"[MONITOR] ALTEROU: {last_value} → {value}")
                    on_change(last_value, value)
                    last_value = value

                else:
                    logging.info(f"[MONITOR] Sem mudança: {value}")

            time.sleep(interval)
            driver.refresh()

    except Exception as e:
        logging.error(f"[MONITOR] Erro: {e}")

    finally:
        driver.quit()



def interact_with_page(url, old, new, text_selector, button_selector):
    try:
        driver = create_driver()
        driver.get(url)

        time.sleep(3)

        mensagem = f"Preço mudou de {old} para {new}"

        campo = driver.find_element(By.CSS_SELECTOR, text_selector)
        campo.send_keys(mensagem)

        botao = driver.find_element(By.CSS_SELECTOR, button_selector)
        botao.click()

        logging.info("[INTERACT] Mensagem enviada!")

        time.sleep(3)
        driver.quit()

    except Exception as e:
        logging.error(f"[INTERACT] Erro: {e}")