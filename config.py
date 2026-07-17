from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

SAUCE_URL = os.getenv("SAUCE_URL")
SAUCE_USERNAME = os.getenv("SAUCE_USERNAME")
SAUCE_PASSWORD = os.getenv("SAUCE_PASSWORD")

CSV_FILE = BASE_DIR / "data" / "produtos_compra.csv"

SCREENSHOT_DIR = BASE_DIR / "screenshots"

LOG_DIR = BASE_DIR / "logs"

DEFAULT_TIMEOUT = 50

PERSONAL_FISRT_NAME = "Jhonatan"
PERSONAL_LAST_NAME = "Martinello"
PERSONAL_POSTAL_CODE = "89990-000"