# Monitor de Preços com Python + Selenium

Este projeto é um sistema em Python que monitora automaticamente preços de ativos (como criptomoedas e moedas) em páginas web, utilizando **Selenium** e validações personalizadas.

---

## Funcionalidades

- Monitoramento automático de preços em tempo real
- Suporte a sites com conteúdo dinâmico (JavaScript)
- Detecção de mudanças de valor
- Ação automática quando o preço muda
- Validação de entradas (URL, intervalo, timeout, etc.)
- Sistema de logs para registrar eventos
- Interface via terminal

---

## Tecnologias utilizadas

- Python 3
- Selenium
- WebDriver Manager
- Regex (tratamento de números)
- Threading (execução em paralelo)
- Logging

---

## Instalação

### 1. Clone o repositório

## Instale as dependências
pip install -r requirements.txt

Se não tiver o arquivo, instale manualmente:

pip install selenium webdriver-manager pytest

## Testar o Programa 

URL:https://www.google.com/search?q=dolar+hoje
Campo:span.DFlfde.SwHCTb
URL destino: https://pastebin.com
Campo texto: textarea#postform-text
Botão: button[type=submit]

## Calculo Do Big 0

Main.py 
varrer página (Selenium) =	O(n)
loop de monitoramento = O(k)
sistema completo = O(k × n)

Validators.py
  Todas as funções são O(1) — verificações simples de string/inteiro.
  
User_logger.py
  log_action: O(1) — escrita sequencial em arquivo

Main.py 
  varrer DOM = O(n)
  loop de monitoramento = O(k)
  sistema completo = O(k × n)

test_validators.py
  validações	= O(1)
  Selenium	= O(n)
  total	= O(t × n)

  ## Para realizar testes use o comando 
   python -m pytest tests/ -v   
      

  
