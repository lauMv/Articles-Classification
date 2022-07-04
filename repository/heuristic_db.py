import jaydebeapi
from pathlib import Path
import os
from repository.heuristic_schema import HeuristicSchema


_driver_class = "org.h2.Driver"
_jdbc_url = "jdbc:h2:tcp://localhost:5234/articles_classification"
_credentials = ["SA", os.getenv("TEXT_CLASSIFIER_DB_PASSWORD")]
_h2_jar = str(os.path.join(Path(__file__).absolute().parents[1], "h2", "bin", "h2-1.4.200.jar"))


def init_heuristics_db():
    _execute(
        ("CREATE TABLE IF NOT EXISTS Heuristics ("
         "  word VARCHAR,"
         "  type BOOLEAN)"))


def get_conflict_words():
    return _execute("SELECT * FROM Heuristics WHERE type = TRUE")


def get_save_words():
    return _execute("SELECT * FROM Heuristics WHERE type = FALSE")


def create(heuristic):
    word = heuristic.get("word")
    query = r"SELECT count(*) AS count FROM Heuristics WHERE word = '{0}'".format(word)
    count = _execute(query, return_entity=False)

    if count[0]["count"] > 0:
        return

    columns = ", ".join(heuristic.keys())
    values = ", ".join("'{}'".format(value) for value in heuristic.values())
    _execute("INSERT INTO Heuristics ({}) VALUES({})".format(columns, values))

    return {}


def delete(word):
    count = _execute("SELECT count(*) AS count FROM Heuristics WHERE word = '{}'".format(word),
                     return_entity=False)
    if count[0]["count"] == 0:
        return
    _execute("DELETE FROM Heuristics WHERE word = '{}'".format(word))
    return {}



# Helper methods
def _build_list_of_dicts(cursor):
    column_names = [record[0].lower() for record in cursor.description]
    column_and_values = [dict(zip(column_names, record)) for record in cursor.fetchall()]
    return column_and_values


def _convert_to_schema(list_of_dicts):
    return HeuristicSchema().load(list_of_dicts, many=True)


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
