from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

URL = "https://www.saucedemo.com"

USERNAME = "standard_user"
PASSWORD = "secret_sauce"

CSV_FILE = BASE_DIR / "data" / "produtos_compra.csv"

SCREENSHOT_DIR = BASE_DIR / "screenshots"

LOG_DIR = BASE_DIR / "logs"