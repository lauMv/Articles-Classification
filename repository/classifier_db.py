import jaydebeapi
from pathlib import Path
import os
from repository.classifier_schema import ClassifierSchema


_driver_class = "org.h2.Driver"
_jdbc_url = "jdbc:h2:tcp://localhost:5234/articles_classification"
_credentials = ["SA", os.getenv("TEXT_CLASSIFIER_DB_PASSWORD")]
_h2_jar = str(os.path.join(Path(__file__).absolute().parents[1], "h2", "bin", "h2-1.4.200.jar"))


def init_classifier_db():
    _execute(
        ("CREATE TABLE IF NOT EXISTS Classifier ("
         "  version VARCHAR NOT NULL,"
         "  model_path VARCHAR NOT NULL,"
         "  model_accuracy FLOAT NOT NULL,"
         "  model_precision FLOAT NOT NULL,"
         "  model_recall FLOAT NOT NULL,"
         "  model_f1 FLOAT NOT NULL,"
         "  creation_date DATE,"
         "  is_in_use BOOLEAN)"))


def get_all():
    return _execute("SELECT * FROM Classifier", return_entity=False)


def get_cant_classifier():
    return _execute("SELECT count(*) as count FROM Classifier", return_entity=False)


def get(version):
    return _execute("SELECT * FROM Classifier WHERE id = {}".format(version), return_entity=True)


def get_use_classifier():
    classifier = _execute("SELECT * FROM Classifier WHERE is_in_use = 'TRUE'", return_entity=True)
    version = classifier[0].get("version")
    return version


def create(classifier):
    version = classifier.get("version")
    query = r"SELECT count(*) AS count FROM Classifier WHERE version = '{0}'".format(version)
    count = _execute(query, return_entity=False)

    if count[0]["count"] > 0:
        return

    columns = ", ".join(classifier.keys())
    values = ", ".join("'{}'".format(value) for value in classifier.values())
    _execute("INSERT INTO Classifier ({}) VALUES({})".format(columns, values))

    return {}


def update_state(version):
    query = "SELECT count(*) AS count FROM Classifier WHERE version = '{}'".format(version)
    count = _execute(query, return_entity=False)

    if count[0]["count"] == 0:
        return
    classifier = {
        'version': version,
        'is_in_use': 'FALSE'
    }
    values = ["'{}'".format(value) for value in classifier.values()]
    update_values = ", ".join("{} = {}".format(key, value) for key, value in zip(classifier.keys(), values))
    _execute("UPDATE Classifier SET {} WHERE version = '{}'".format(update_values, version))
    return {}


def update(classifier):
    version = classifier.get('version')
    query = "SELECT count(*) AS count FROM Classifier WHERE version = '{}'".format(version)
    count = _execute(query, return_entity=False)

    if count[0]["count"] == 0:
        return

    values = ["'{}'".format(value) for value in classifier.values()]
    update_values = ", ".join("{} = {}".format(key, value) for key, value in zip(classifier.keys(), values))
    _execute("UPDATE Classifier SET {} WHERE version = '{}'".format(update_values, version))
    return {}


# Helper methods
def _build_list_of_dicts(cursor):
    column_names = [record[0].lower() for record in cursor.description]
    column_and_values = [dict(zip(column_names, record)) for record in cursor.fetchall()]
    return column_and_values


def _convert_to_schema(list_of_dicts):
    return ClassifierSchema().load(list_of_dicts, many=True)


def _execute(query, return_entity=None):
    connection = jaydebeapi.connect(_driver_class, _jdbc_url, _credentials, _h2_jar)
    cursor = connection.cursor()
    cursor.execute(query)

    query_result = None
    if cursor.rowcount == -1:
        query_result = _build_list_of_dicts(cursor)

    if query_result is not None and return_entity:
        query_result = _convert_to_schema(query_result)

    cursor.close()
    connection.close()
    return query_result
