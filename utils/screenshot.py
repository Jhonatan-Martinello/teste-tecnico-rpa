from datetime import datetime
from pathlib import Path

from config import SCREENSHOT_DIR


class Screenshot:

    def __init__(self, driver):
        self.driver = driver
        self.directory = Path(SCREENSHOT_DIR)
        self.directory.mkdir(parents=True, exist_ok=True)


    def capture(self, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.png"
        path = self.directory / filename
        self.driver.save_screenshot(str(path))

        return path