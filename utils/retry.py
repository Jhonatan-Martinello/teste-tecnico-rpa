import time
import logging

from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    StaleElementReferenceException
)


logger = logging.getLogger("automation")


def retry(
    func,
    retries=3,
    delay=2,
    exceptions=(
        TimeoutException,
        WebDriverException,
        StaleElementReferenceException
    )
):
    last_exception = None

    for attempt in range(1, retries + 1):

        try:
            return func()

        except exceptions as e:
            last_exception = e
            logger.warning(f"Tentativa {attempt}/{retries} falhou: {e}")

            if attempt < retries:
                time.sleep(delay)

    logger.error("Número máximo de tentativas excedido.",exc_info=True)

    raise last_exception
