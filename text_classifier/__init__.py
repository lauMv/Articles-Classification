# import schedule
import time

from .extraction import execute as execute_extraction
from .pre_processing import execute as execute_preprocessing
from .classifier import execute as execute_classifier
from repository import init_db


def main():
    # init_db()
    # execute_extraction()
    # execute_preprocessing()
    execute_classifier()


print("Iniciando main()")

main()

# schedule.every(1).hours.do(main)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
