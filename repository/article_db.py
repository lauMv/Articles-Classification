import jaydebeapi
from pathlib import Path
import os
from repository.article_schema import ArticleSchema


_driver_class = "org.h2.Driver"
_jdbc_url = "jdbc:h2:tcp://localhost:5234/articles_classification"
_credentials = ["SA", os.getenv("TEXT_CLASSIFIER_DB_PASSWORD")]
_h2_jar = str(os.path.join(Path(__file__).absolute().parents[1], "h2", "bin", "h2-1.4.200.jar"))


def init_db():
    _execute(
        ("CREATE TABLE IF NOT EXISTS Article ("
         "  source_file_path VARCHAR NOT NULL,"
         "  pre_processed_file_path VARCHAR NOT NULL,"
         "  filename VARCHAR NOT NULL,"
         "  extraction_date DATE NOT NULL,"
         "  paper VARCHAR NOT NULL,"
         "  article_content VARCHAR NOT NULL,"
         "  user_classification VARCHAR NOT NULL,"
         "  model_classification BOOLEAN,"
         "  used_in_classifier BOOLEAN)"))


def get_all():
    return _execute("SELECT * FROM Article", return_entity=False)


def get(filename):
    return _execute("SELECT * FROM Article WHERE filename = {}".format(filename), return_entity=True)


def get_by_user_classification(user_classification):
    return _execute("SELECT * FROM Article WHERE user_classification = {}".format(user_classification),
                    return_entity=True)


def get_used_in_classifier():
    return _execute("SELECT * FROM Article WHERE used_in_classifier = TRUE")


def create(article):
    source_file_path = article.get("source_file_path")
    query = r"SELECT count(*) AS count FROM Article WHERE source_file_path = '{0}'".format(source_file_path)
    count = _execute(query, return_entity=False)

    if count[0]["count"] > 0:
        return

    columns = ", ".join(article.keys())
    values = ", ".join("'{}'".format(value) for value in article.values())
    _execute("INSERT INTO Article ({}) VALUES({})".format(columns, values))

    return {}


def update(article, filename):
    source_file_path = os.path.join(os.getenv("TEXT_CLASSIFIER_DATA"), "articles", filename)
    query = "SELECT count(*) AS count FROM Article WHERE source_file_path = '{}'".format(source_file_path)
    count = _execute(query, return_entity=False)

    if count[0]["count"] == 0:
        return

    values = ["'{}'".format(value) for value in article.values()]
    update_values = ", ".join("{} = {}".format(key, value) for key, value in zip(article.keys(), values))
    _execute("UPDATE Article SET {} WHERE source_file_path = '{}'".format(update_values, source_file_path))
    return {}


def delete(source_file_path):
    count = _execute("SELECT count(*) AS count FROM Article WHERE source_file_path = '{}'".format(source_file_path),
                     return_entity=False)
    if count[0]["count"] == 0:
        return
    _execute("DELETE FROM Article WHERE source_file_path = '{}'".format(source_file_path))
    return {}



# Helper methods
def _build_list_of_dicts(cursor):
    column_names = [record[0].lower() for record in cursor.description]
    column_and_values = [dict(zip(column_names, record)) for record in cursor.fetchall()]
    return column_and_values


def _convert_to_schema(list_of_dicts):
    return ArticleSchema().load(list_of_dicts, many=True)


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
