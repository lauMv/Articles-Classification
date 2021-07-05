import jaydebeapi
from pathlib import Path
import os


def init_db():
    connection = jaydebeapi.connect(_driver_class, _jdbc_url, _credentials, _h2_jar)
    #TODO incluir la aquí la inicialización del esquema de la BD
    connection.close()


_driver_class = "org.h2.Driver"
_jdbc_url = "jdbc:h2:tcp://localhost:5234/articles_classification"
_credentials = ["SA", os.getenv("TEXT_CLASSIFIER_DB_PASSWORD")]
_h2_jar = str(os.path.join(Path(__file__).absolute().parents[1], "h2", "bin", "h2-1.4.200.jar"))
