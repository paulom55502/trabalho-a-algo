"""
validators.py
=============
Funções de validação de entrada do usuário.

Todas as entradas devem ser validadas antes de qualquer operação de rede
ou de automação de browser. Um sistema que travar por falta de validação
recebe 0 pontos nos critérios de avaliação.

Complexity
----------
Todas as funções são O(1) — verificações simples de string/inteiro.
"""

import re
from urllib.parse import urlparse


def validate_url(url: str) -> tuple[bool, str]:
    """
    Verifica se ``url`` é uma URL HTTP/HTTPS válida.

    Parameters
    ----------
    url : str
        URL a validar.

    Returns
    -------
    tuple[bool, str]
        ``(True, "")`` se válida, ``(False, mensagem_de_erro)`` caso contrário.

    Complexity
    ----------
    O(1)
    """
    if not url or not isinstance(url, str):
        return False, "URL não pode ser vazia."
    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https"):
        return False, "URL deve começar com http:// ou https://"
    if not parsed.netloc:
        return False, "URL não contém um domínio válido."
    return True, ""


def validate_timeout(value) -> tuple[bool, str]:
    """
    Verifica se ``value`` é um inteiro positivo para uso como timeout.

    Parameters
    ----------
    value : any
        Valor a validar.

    Returns
    -------
    tuple[bool, str]

    Complexity
    ----------
    O(1)
    """
    try:
        v = int(value)
    except (ValueError, TypeError):
        return False, "Timeout deve ser um número inteiro."
    if v <= 0:
        return False, "Timeout deve ser maior que zero."
    if v > 300:
        return False, "Timeout não pode exceder 300 segundos."
    return True, ""


def validate_interval(value) -> tuple[bool, str]:
    """
    Verifica se ``value`` é um inteiro positivo para uso como intervalo de polling.

    Complexity
    ----------
    O(1)
    """
    try:
        v = int(value)
    except (ValueError, TypeError):
        return False, "Intervalo deve ser um número inteiro."
    if v <= 0:
        return False, "Intervalo deve ser maior que zero."
    return True, ""


def validate_username(name: str) -> tuple[bool, str]:
    """
    Valida o nome do usuário: ao menos 3 caracteres, somente letras (permite
    nomes compostos com espaço).

    Parameters
    ----------
    name : str
        Nome informado pelo usuário.

    Returns
    -------
    tuple[bool, str]

    Complexity
    ----------
    O(1)
    """
    if not name or not isinstance(name, str):
        return False, "Nome não pode ser vazio."
    stripped = name.strip()
    if len(stripped) < 3:
        return False, "Nome deve ter ao menos 3 caracteres."
    if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", stripped):
        return False, "Nome deve conter apenas letras (e espaços para nomes compostos)."
    return True, ""


def validate_field_hint(hint: str) -> tuple[bool, str]:
    """
    Valida o rótulo/texto do campo a ser monitorado.

    Complexity
    ----------
    O(1)
    """
    if not hint or not hint.strip():
        return False, "O nome do campo não pode ser vazio."
    if len(hint.strip()) < 2:
        return False, "O nome do campo deve ter ao menos 2 caracteres."
    return True, ""


def validate_numeric_value(raw_text: str) -> tuple[bool, str]:
    """
    Verifica se um texto extraído da página contém um valor numérico válido.

    O critério do trabalho exige validar que o campo monitorado é de fato
    um número — caso contrário o sistema deve rejeitar e não monitorar.

    Parameters
    ----------
    raw_text : str
        Texto bruto extraído do elemento encontrado na página.

    Returns
    -------
    tuple[bool, str]

    Examples
    --------
    >>> validate_numeric_value("R$ 1.500,00")
    (True, "")
    >>> validate_numeric_value("Encerrado")
    (False, "O campo encontrado não contém um valor numérico.")

    Complexity
    ----------
    O(1) — regex aplicada sobre string de tamanho limitado.
    """
    if not raw_text or not raw_text.strip():
        return False, "O texto extraído está vazio."
    # Aceita inteiros e decimais com . ou , como separadores
    if not re.search(r"\d", raw_text):
        return False, "O campo encontrado não contém um valor numérico."
    return True, ""
