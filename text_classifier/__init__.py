# import schedule
import time

from .extraction import execute as execute_extraction
from .pre_processing import execute as execute_preprocessing
from .predictor import execute as execute_predictor
from repository import init_db, init_classifier_db
from .test_classifier import execute_ as execute_classifier


def main():
    init_db()
    init_classifier_db()
    execute_extraction()
    execute_preprocessing()
    execute_predictor()


print("Iniciando main()")

main()

# schedule.every(1).hours.do(main)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
