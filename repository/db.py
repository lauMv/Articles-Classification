import jaydebeapi
from pathlib import Path
import os
from articles_schema import ArticleSchema


_driver_class = "org.h2.Driver"
_jdbc_url = "jdbc:h2:tcp://localhost:5234/articles_classification"
_credentials = ["SA", os.getenv("TEXT_CLASSIFIER_DB_PASSWORD")]
_h2_jar = str(os.path.join(Path(__file__).absolute().parents[1], "h2", "bin", "h2-1.4.200.jar"))


def initialize():
    _execute(
        ("CREATE TABLE IF NOT EXISTS articles ("
            "  id INT PRIMARY KEY AUTO_INCREMENT,"
            "  source_file_path VARCHAR NOT NULL,"
            "  pre_processed_file_path VARCHAR NOT NULL,"
            "  extraction_date VARCHAR NOT NULL,"
            "  user_classification ('NONE', INT, INT),"
            "  model_classification ('NONE', INT, INT))"))

def get_all():
    return _execute("SELECT * FROM articles", returnResult=True)

def get(Id):
    return _execute("SELECT * FROM articles WHERE id = {}".format(Id), returnResult=True)

def create(articles):
    count = _execute("SELECT count(*) AS count FROM articles WHERE source_file_path LIKE '{}'".format(articles.get("source_file_path")),
                     returnResult=True)
    if count[0]["count"] > 0:
        return

    columns = ", ".join(articles.keys())
    values = ", ".join("'{}'".format(value) for value in articles.values())
    _execute("INSERT INTO article ({}) VALUES({})".format(columns, values))

    return {}

def update(articles, Id):
    count = _execute("SELECT count(*) AS count FROM articles WHERE id = {}".format(Id), returnResult=True)
    if count[0]["count"] == 0:
        return
    values = ["'{}'".format(value) for value in articles.values()]
    update_values = ", ".join("{} = {}".format(key, value) for key, value in zip(articles.keys(), values))
    _execute("UPDATE articles SET {} WHERE id = {}".format(update_values, Id))
    return {}


def delete(Id):
    count = _execute("SELECT count(*) AS count FROM articles WHERE id = {}".format(Id), returnResult=True)
    if count[0]["count"] == 0:
        return
    _execute("DELETE FROM articles WHERE id = {}".format(Id))
    return {}


def _convert_to_schema(cursor):
    column_names = [record[0].lower() for record in cursor.description]
    column_and_values = [dict(zip(column_names, record)) for record in cursor.fetchall()]

    return ArticleSchema().load(column_and_values, many=True)


def _execute(query, returnResult=None):
    connection = jaydebeapi.connect(_driver_class, _jdbc_url, _credentials, _h2_jar)
    cursor = connection.cursor()
    cursor.execute(query)
    if returnResult:
        returnResult = _convert_to_schema(cursor)
    cursor.close()
    connection.close()

    return returnResult