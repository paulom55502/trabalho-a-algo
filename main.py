import logging
import sys
import threading

from src.validators import (
    validate_url,
    validate_timeout,
    validate_interval,
    validate_username,
    validate_field_hint,
)

from src.user_logger import log_action, get_log_path
from src.monitor import monitor_price, interact_with_page

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def ask(prompt, validator):
    while True:
        value = input(prompt).strip()
        ok, msg = validator(value)
        if ok:
            return value
        print(f"Erro: {msg}")


def main():
    print("\n==============================")
    print("           Assistente          ")
    print("==============================\n")

   
    username = ask("Seu nome: ", validate_username)
    log_action(username, "Sistema iniciado")

    
    url = ask("URL do produto: ", validate_url)

    
    hint = ask("Texto do preço (ex: R$): ", validate_field_hint)


    interval = int(ask("Intervalo (segundos): ", validate_interval))
    timeout = int(ask("Timeout: ", validate_timeout))

   
    print("\n--- Página de notificação ---")
    target_url = ask("URL destino: ", validate_url)
    text_selector = input("Campo texto (ex: textarea): ") or "textarea"
    button_selector = input("Botão (ex: button): ") or "button"

    
    def on_change(old, new):
        print(f"\n🔥 MUDOU: {old} → {new}\n")
        log_action(username, f"Mudança: {old} → {new}")

        interact_with_page(
            target_url,
            old,
            new,
            text_selector,
            button_selector,
        )

  
    stop_event = threading.Event()

    thread = threading.Thread(
        target=monitor_price,
        kwargs={
            "url": url,
            "field_hint": hint,
            "interval": interval,
            "timeout": timeout,
            "on_change": on_change,
            "stop_event": stop_event,
        },
        daemon=True,
    )

    thread.start()

    print("\nMonitorando... CTRL+C para parar\n")

    try:
        thread.join()
    except KeyboardInterrupt:
        print("\nEncerrando...")
        stop_event.set()
        thread.join()


if __name__ == "__main__":
    main()