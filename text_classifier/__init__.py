import schedule
import time
from .extraction import execute as execute_extraction
from .pre_processing import execute as execute_preprocessing


def main():
    execute_extraction()
    execute_preprocessing()


schedule.every(10).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)