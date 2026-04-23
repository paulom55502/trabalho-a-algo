import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from src.validators import (
    validate_url,
    validate_timeout,
    validate_interval,
    validate_username,
    validate_field_hint,
)

from src.monitor import find_price_on_page


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # não abre janela
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver
    driver.quit()



class TestValidateUrl:
    def test_valid_http(self):
        ok, msg = validate_url("http://example.com")
        assert ok is True
        assert msg == ""

    def test_valid_https(self):
        ok, msg = validate_url("https://leilao.com/item/123")
        assert ok is True

    def test_missing_scheme(self):
        ok, msg = validate_url("example.com")
        assert ok is False

    def test_ftp_scheme(self):
        ok, msg = validate_url("ftp://files.example.com")
        assert ok is False

    def test_empty_url(self):
        ok, msg = validate_url("")
        assert ok is False

    def test_none_url(self):
        ok, msg = validate_url(None)
        assert ok is False



class TestValidateTimeout:
    def test_valid_timeout(self):
        ok, _ = validate_timeout(10)
        assert ok is True

    def test_zero_timeout(self):
        ok, _ = validate_timeout(0)
        assert ok is False

    def test_negative_timeout(self):
        ok, _ = validate_timeout(-5)
        assert ok is False

    def test_too_large_timeout(self):
        ok, _ = validate_timeout(301)
        assert ok is False



class TestValidateInterval:
    def test_valid_interval(self):
        ok, _ = validate_interval(5)
        assert ok is True

    def test_zero_interval(self):
        ok, _ = validate_interval(0)
        assert ok is False



class TestValidateUsername:
    def test_simple_name(self):
        ok, _ = validate_username("Ana")
        assert ok is True

    def test_too_short(self):
        ok, _ = validate_username("Jo")
        assert ok is False

    def test_numbers(self):
        ok, _ = validate_username("Ana123")
        assert ok is False




class TestValidateFieldHint:
    def test_valid_hint(self):
        ok, _ = validate_field_hint("Preço")
        assert ok is True

    def test_empty_hint(self):
        ok, _ = validate_field_hint("")
        assert ok is False




class TestValidateNumericValue:

    def test_finds_integer_price(self, driver):
        html = """
        <html>
        <body>
            <div>Lance Atual 1500</div>
        </body>
        </html>
        """

        driver.get("data:text/html;charset=utf-8," + html)

        result = find_price_on_page(driver, "Lance Atual")

        assert result is not None
        assert result["value"] == 1500.0


    def test_finds_decimal_price(self, driver):
        html = """
        <html>
        <body>
            <div>Preço 2.350,99</div>
        </body>
        </html>
        """

        driver.get("data:text/html;charset=utf-8," + html)

        result = find_price_on_page(driver, "Preço")

        assert result is not None
        assert result["value"] == pytest.approx(2350.99, abs=1)


    def test_not_found(self, driver):
        html = "<html><body><p>Sem dados</p></body></html>"

        driver.get("data:text/html;charset=utf-8," + html)

        result = find_price_on_page(driver, "Lance Atual")

        assert result is None