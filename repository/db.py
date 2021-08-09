import jaydebeapi
from pathlib import Path
import os
# from repository import articles_schema as ArticleSchema
import articles_schema as ArticleSchema

_driver_class = "org.h2.Driver"
_jdbc_url = "jdbc:h2:tcp://localhost:5234/articles_classification"
_credentials = ["SA", os.getenv("TEXT_CLASSIFIER_DB_PASSWORD")]
_h2_jar = str(os.path.join(Path(__file__).absolute().parents[1], "h2", "bin", "h2-1.4.200.jar"))


def init_db():
    _execute(
        ("CREATE TABLE IF NOT EXISTS articles ("
            "  source_file_path VARCHAR NOT NULL,"
            "  pre_processed_file_path VARCHAR NOT NULL,"
            "  extraction_date VARCHAR NOT NULL,"
            "  user_classification VARCHAR,"
            "  model_classification VARCHAR)"))


def get_all():
    return _execute("SELECT * FROM articles", returnResult=True)


def get(source_file_path):
    return _execute("SELECT * FROM articles WHERE source_file_path = {}".format(source_file_path), returnResult=True)


def create(article):
    count = _execute("SELECT count(*) AS count FROM articles WHERE source_file_path LIKE '{}'".format(article.get("source_file_path")),
                     returnResult=True)

    if count[0]["count"] > 0:
        return

    columns = ", ".join(article.keys())
    values = ", ".join("'{}'".format(value) for value in article.values())
    _execute("INSERT INTO article ({}) VALUES({})".format(columns, values))

    return {}


def update(articles, source_file_path):
    count = _execute("SELECT count(*) AS count FROM articles WHERE source_file_path = {}".format(source_file_path),
                     returnResult=True)
    if count[0]["count"] == 0:
        return
    values = ["'{}'".format(value) for value in articles.values()]
    update_values = ", ".join("{} = {}".format(key, value) for key, value in zip(articles.keys(), values))
    _execute("UPDATE articles SET {} WHERE source_file_path = {}".format(update_values, source_file_path))
    return {}


def delete(source_file_path):
    count = _execute("SELECT count(*) AS count FROM articles WHERE source_file_path = {}".format(source_file_path),
                     returnResult=True)
    if count[0]["count"] == 0:
        return
    _execute("DELETE FROM articles WHERE source_file_path = {}".format(source_file_path))
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


articles_data = [
    {
        "id": "1",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned   15 de mayo de 2021  19 10 h   Rescatan a un mono aullador al que domesticaron en Sipe Sipe   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   15 de mayo de 2021  19 10 h   Rescatan a un mono aullador al que domesticaron en Sipe Sipe   Cochabamba   Opinión Bolivia ",
        "extraction_date": "15 de mayo de 2021  19 10 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "2",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned   16 de mayo de 2021  00 00 h   Brigadas de vecinos patrullan sus calles con silbatos y palos   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   16 de mayo de 2021  00 00 h   Brigadas de vecinos patrullan sus calles con silbatos y palos   Cochabamba   Opinión Bolivia ",
        "extraction_date": "16 de mayo de 2021  00 00 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "3",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned   16 de mayo de 2021  00 00 h   Cochabamba entrena aves con ayuda de México y Colombia   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   16 de mayo de 2021  00 00 h   Cochabamba entrena aves con ayuda de México y Colombia   Cochabamba   Opinión Bolivia ",
        "extraction_date": "16 de mayo de 2021  00 00 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "4",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned   16 de mayo de 2021  10 24 h   Capacitan a personal de Sacaba para combatir incendios   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   16 de mayo de 2021  10 24 h   Capacitan a personal de Sacaba para combatir incendios   Cochabamba   Opinión Bolivia ",
        "extraction_date": "16 de mayo de 2021  10 24 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "5",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned   16 de mayo de 2021  11 28 h   Manfred anuncia que clausurarán definitivamente fiestas clandestinas    Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   16 de mayo de 2021  11 28 h   Manfred anuncia que clausurarán definitivamente fiestas clandestinas    Cochabamba   Opinión Bolivia ",
        "extraction_date": "16 de mayo de 2021  11 28 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "6",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned   18 de mayo de 2021  00 00 h   Aplican 3 799 vacunas  en 10 días inician con los de 40 años   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   18 de mayo de 2021  00 00 h   Aplican 3 799 vacunas  en 10 días inician con los de 40 años   Cochabamba   Opinión Bolivia ",
        "extraction_date": "18 de mayo de 2021  00 00 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "7",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned   18 de mayo de 2021  00 00 h   Con ley prevén recuperar regalías mineras de Cocapata y Bolívar   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   18 de mayo de 2021  00 00 h   Con ley prevén recuperar regalías mineras de Cocapata y Bolívar   Cochabamba   Opinión Bolivia ",
        "extraction_date": "18 de mayo de 2021  00 00 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "8",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned   18 de mayo de 2021  00 00 h   Novillo garantiza apoyo para proyectos de agua y El Sillar   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   18 de mayo de 2021  00 00 h   Novillo garantiza apoyo para proyectos de agua y El Sillar   Cochabamba   Opinión Bolivia ",
        "extraction_date": "18 de mayo de 2021  00 00 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "9",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned   20 de mayo de 2021  15 08 h   Amplían horario de vacunación en tres puntos a partir de hoy   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   20 de mayo de 2021  15 08 h   Amplían horario de vacunación en tres puntos a partir de hoy   Cochabamba   Opinión Bolivia ",
        "extraction_date": "20 de mayo de 2021  15 08 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "10",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned   20 de mayo de 2021  21 51 h   Alcaldía inicia campaña de fumigación en Cochabamba   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   20 de mayo de 2021  21 51 h   Alcaldía inicia campaña de fumigación en Cochabamba   Cochabamba   Opinión Bolivia ",
        "extraction_date": "20 de mayo de 2021  21 51 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "11",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned  16 May 2021 Bruno Rojas logra reunirse con la Viceministra de Deportes  Cielo Veizaga   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  16 May 2021 Bruno Rojas logra reunirse con la Viceministra de Deportes  Cielo Veizaga   Los Tiempos",
        "extraction_date": "16 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "12",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned  16 May 2021 Cientos de personas se suman a limpieza del canal Isuto  en Santa Cruz   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  16 May 2021 Cientos de personas se suman a limpieza del canal Isuto  en Santa Cruz   Los Tiempos",
        "extraction_date": "16 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "13",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned  18 May 2021 Exviceministro Durán es posesionado como gerente de la Gestora Pública   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  18 May 2021 Exviceministro Durán es posesionado como gerente de la Gestora Pública   Los Tiempos",
        "extraction_date": "18 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "14",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned  18 May 2021 Gobierno puede solventar gastos de tres deportistas para Sudamericano de Atletismo   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  18 May 2021 Gobierno puede solventar gastos de tres deportistas para Sudamericano de Atletismo   Los Tiempos",
        "extraction_date": "18 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "15",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned  20 May 2021 Kevin  el cochalo que hace realidad su sueño fabricando su propio Lamborghini   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  20 May 2021 Kevin  el cochalo que hace realidad su sueño fabricando su propio Lamborghini   Los Tiempos",
        "extraction_date": "20 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "16",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned  21 May 2021 Emotiva despedida a Rayza Torriani  destacan su lucha por la comunidad LGBT   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  21 May 2021 Emotiva despedida a Rayza Torriani  destacan su lucha por la comunidad LGBT   Los Tiempos",
        "extraction_date": "21 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "17",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned 09 de mayo de 2021  12 00 h   Intendencia decomisa bebidas adulteradas y sin registro  anuncian estricto control a bares y licorerías   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 de mayo de 2021  12 00 h   Intendencia decomisa bebidas adulteradas y sin registro  anuncian estricto control a bares y licorerías   Cochabamba   Opinión Bolivia ",
        "extraction_date": "09 de mayo de 2021  12 00 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "18",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned 09 de mayo de 2021  16 18 h   Alcaldía interviene presunto loteamiento en Yarwi Yarwi  en la serranía de San Pedro   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 de mayo de 2021  16 18 h   Alcaldía interviene presunto loteamiento en Yarwi Yarwi  en la serranía de San Pedro   Cochabamba   Opinión Bolivia ",
        "extraction_date": "09 de mayo de 2021  16 18 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "19",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned 09 May 2021 Acuático  Familia y teleférico  más visitados pero aflojan bioseguridad   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Acuático  Familia y teleférico  más visitados pero aflojan bioseguridad   Los Tiempos",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "20",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned 09 May 2021 Aduana comisa mercadería de contrabando por valor de Bs 2 3 millones en Cochabamba   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Aduana comisa mercadería de contrabando por valor de Bs 2 3 millones en Cochabamba   Los Tiempos",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "21",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned 09 May 2021 Alcón sugiere priorizar medios locales y alternativos para luchar contra la desinformación   La Razón   Noticias de Bolivia y el Mundo",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Alcón sugiere priorizar medios locales y alternativos para luchar contra la desinformación   La Razón   Noticias de Bolivia y el Mundo",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "22",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned 09 May 2021 ANP rinde homenaje al periodista boliviano   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 ANP rinde homenaje al periodista boliviano   Los Tiempos",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "23",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned 09 May 2021 BMSC sube a 115 sus agencias en el país   La Razón   Noticias de Bolivia y el Mundo",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 BMSC sube a 115 sus agencias en el país   La Razón   Noticias de Bolivia y el Mundo",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "24",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned 09 May 2021 En Bolivia hasta el momento se aplicaron casi un millón de vacunas contra el COVID 19   La Razón   Noticias de Bolivia y el Mundo",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 En Bolivia hasta el momento se aplicaron casi un millón de vacunas contra el COVID 19   La Razón   Noticias de Bolivia y el Mundo",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "25",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned 09 May 2021 Expertos  Avance económico  aún lento  es gracias a factores externos   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Expertos  Avance económico  aún lento  es gracias a factores externos   Los Tiempos",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "26",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned 09 May 2021 Voluntarios recorrieron más de 10 kilómetros para limpiar el río Guadalquivir   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Voluntarios recorrieron más de 10 kilómetros para limpiar el río Guadalquivir   Los Tiempos",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "27",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned 11 de mayo de 2021  13 05 h   Reyes Villa entrega medicamentos e insumos para hospitales del Norte  Sur y Cochabamba   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 11 de mayo de 2021  13 05 h   Reyes Villa entrega medicamentos e insumos para hospitales del Norte  Sur y Cochabamba   Cochabamba   Opinión Bolivia ",
        "extraction_date": "11 de mayo de 2021  13 05 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "28",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned articles 12 de mayo de 2021  00 00 h   Dan Bs 2 millones en mobilario a centro para drogodependientes   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles 12 de mayo de 2021  00 00 h   Dan Bs 2 millones en mobilario a centro para drogodependientes   Cochabamba   Opinión Bolivia ",
        "extraction_date": "12 de mayo de 2021  00 00 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "29",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned articles 12 de mayo de 2021  13 55 h   Inicia campaña de vacunación contra la influenza  disponible en todos los centros de salud   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles 12 de mayo de 2021  13 55 h   Inicia campaña de vacunación contra la influenza  disponible en todos los centros de salud   Cochabamba   Opinión Bolivia ",
        "extraction_date": "12 de mayo de 2021  13 55 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "31",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned articles 14 de mayo de 2021  00 00 h   En un día inmunizan a más del 4  de gente de 50 a 59 años   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles 14 de mayo de 2021  00 00 h   En un día inmunizan a más del 4  de gente de 50 a 59 años   Cochabamba   Opinión Bolivia ",
        "extraction_date": "14 de mayo de 2021  00 00 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "31",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned articles 14 de mayo de 2021  00 00 h   Enseñarán a crear contenido digital a profes   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles 14 de mayo de 2021  00 00 h   Enseñarán a crear contenido digital a profes   Cochabamba   Opinión Bolivia ",
        "extraction_date": "14 de mayo de 2021  00 00 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "32",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned articles 14 de mayo de 2021  00 00 h   La comida es lo que más se compra por internet en Bolivia   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles 14 de mayo de 2021  00 00 h   La comida es lo que más se compra por internet en Bolivia   Cochabamba   Opinión Bolivia ",
        "extraction_date": "14 de mayo de 2021  00 00 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "33",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned articles 14 de mayo de 2021  10 21 h   Zoonosis de Colcapirhua vacuna a perros y gatos en OTB Santa Rosa  acuden a pedido de los barrios   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles 14 de mayo de 2021  10 21 h   Zoonosis de Colcapirhua vacuna a perros y gatos en OTB Santa Rosa  acuden a pedido de los barrios   Cochabamba   Opinión Bolivia ",
        "extraction_date": "14 de mayo de 2021  10 21 h",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "34",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned articles12 May 2021 Felicitan a enfermeras en su “Día” y expresan pésame por Covid 19   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles12 May 2021 Felicitan a enfermeras en su “Día” y expresan pésame por Covid 19   Los Tiempos",
        "extraction_date": "12 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "35",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/buenos_limpios/cleaned articles12 May 2021 Primer festival de artes marciales en apoyo al sensei Juan Reynaldo Villa Fora   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles12 May 2021 Primer festival de artes marciales en apoyo al sensei Juan Reynaldo Villa Fora   Los Tiempos",
        "extraction_date": "12 May 2021",
        "user_classification": "None, 1, 0",
        "model_classification": "None, 1, 0"
    },
    {
        "id": "36",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned   16 de mayo de 2021  00 00 h   En cuatro regiones la basura es un problema y alerta a autoridades   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   16 de mayo de 2021  00 00 h   En cuatro regiones la basura es un problema y alerta a autoridades   Cochabamba   Opinión Bolivia ",
        "extraction_date": " 16 de mayo de 2021  00 00 h",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "37",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned   17 de mayo de 2021  22 01 h   Diputado Arce presentará a Contraloría denuncia sobre  incompatibilidad sobreviniente  por caso de los Reyes Villa   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   17 de mayo de 2021  22 01 h   Diputado Arce presentará a Contraloría denuncia sobre  incompatibilidad sobreviniente  por caso de los Reyes Villa   Cochabamba   Opinión Bolivia ",
        "extraction_date": "17 de mayo de 2021  22 01 h",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "38",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned   21 de mayo de 2021  00 00 h   MAS denuncia a los Reyes Villa y a Quispe ante la Contraloría   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   21 de mayo de 2021  00 00 h   MAS denuncia a los Reyes Villa y a Quispe ante la Contraloría   Cochabamba   Opinión Bolivia ",
        "extraction_date": "21 de mayo de 2021  00 00 h",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "39",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  16 May 2021  Es como para llorar   la basura arrastrada desde urbes causa un drama en una comunidad rural   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  16 May 2021  Es como para llorar   la basura arrastrada desde urbes causa un drama en una comunidad rural   Los Tiempos",
        "extraction_date": "16 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "40",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  16 May 2021 Cochabamba se encierra y transporte amenaza   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  16 May 2021 Cochabamba se encierra y transporte amenaza   Los Tiempos",
        "extraction_date": "16 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "41",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned   18 de mayo de 2021  00 00 h   Con ley prevén recuperar regalías mineras de Cocapata y Bolívar   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned   18 de mayo de 2021  00 00 h   Con ley prevén recuperar regalías mineras de Cocapata y Bolívar   Cochabamba   Opinión Bolivia ",
        "extraction_date": "18 de mayo de 2021  00 00 h",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"

    },
    {
        "id": "42",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  16 May 2021 La crisis golpea más a Cochabamba  1 de cada 10 personas está sin trabajo   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  16 May 2021 La crisis golpea más a Cochabamba  1 de cada 10 personas está sin trabajo   Los Tiempos",
        "extraction_date": "16 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "43",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  17 May 2021 CC propone 30 años de cárcel al gobernante que quebrante la Constitución para quedarse en el poder   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  17 May 2021 CC propone 30 años de cárcel al gobernante que quebrante la Constitución para quedarse en el poder   Los Tiempos",
        "extraction_date": "17 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "44",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  17 May 2021 Senadora Arce presenta denuncia contra jueza que liberó a feminicida   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  17 May 2021 Senadora Arce presenta denuncia contra jueza que liberó a feminicida   Los Tiempos",
        "extraction_date": "17 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "45",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  18 May 2021 500 estudiantes de la “U”  sin inscripción ni seguro   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  18 May 2021 500 estudiantes de la “U”  sin inscripción ni seguro   Los Tiempos",
        "extraction_date": "18 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "46",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  18 May 2021 A pedido de la Procuraduría  Fiscalía amplía otros delitos contra Añez por el caso  Golpe    Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  18 May 2021 A pedido de la Procuraduría  Fiscalía amplía otros delitos contra Añez por el caso  Golpe    Los Tiempos",
        "extraction_date": "18 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "47",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  18 May 2021 Áñez  ‘Han pasado 2 meses desde mi detención  no hay pruebas que me vinculen con delitos’   La Razón   Noticias de Bolivia y el Mundo",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  18 May 2021 Áñez  ‘Han pasado 2 meses desde mi detención  no hay pruebas que me vinculen con delitos’   La Razón   Noticias de Bolivia y el Mundo",
        "extraction_date": "18 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "48",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  18 May 2021 Bolivia registra 47 feminicidios y 11 infanticidios en lo que va del año   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  18 May 2021 Bolivia registra 47 feminicidios y 11 infanticidios en lo que va del año   Los Tiempos",
        "extraction_date": "18 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "49",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  18 May 2021 Caso Gacip  Fiscalía ordena aprehensión de Melisa Ibarra por no presentarse a declarar   La Razón   Noticias de Bolivia y el Mundo",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  18 May 2021 Caso Gacip  Fiscalía ordena aprehensión de Melisa Ibarra por no presentarse a declarar   La Razón   Noticias de Bolivia y el Mundo",
        "extraction_date": "18 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "50",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  18 May 2021 Copa a Morales  “No podemos tratar de pandilleros a las nuevas generaciones que piensan diferente”   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  18 May 2021 Copa a Morales  “No podemos tratar de pandilleros a las nuevas generaciones que piensan diferente”   Los Tiempos",
        "extraction_date": "18 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "51",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  18 May 2021 Del Castillo  Se desbarata red de corrupción que mal usó Bs 156 MM en el Ministerio de Gobierno   La Razón   Noticias de Bolivia y el Mundo",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  18 May 2021 Del Castillo  Se desbarata red de corrupción que mal usó Bs 156 MM en el Ministerio de Gobierno   La Razón   Noticias de Bolivia y el Mundo",
        "extraction_date": "18 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "52",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  22 May 2021 Baldivieso  “Nos reunimos dos veces  pero no hay acuerdo”   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  22 May 2021 Baldivieso  “Nos reunimos dos veces  pero no hay acuerdo”   Los Tiempos",
        "extraction_date": "22 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "53",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned  22 May 2021 Critican al Gobierno por inclusión de Bolivia en“lista de la vergüenza” de UN Watch   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned  22 May 2021 Critican al Gobierno por inclusión de Bolivia en“lista de la vergüenza” de UN Watch   Los Tiempos",
        "extraction_date": "22 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "54",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned 08 de mayo de 2021  13 38 h   Reaparece el expolicía que rechazó el motín en 2019 y pide justicia para los fallecidos en Huayllani   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 08 de mayo de 2021  13 38 h   Reaparece el expolicía que rechazó el motín en 2019 y pide justicia para los fallecidos en Huayllani   Cochabamba   Opinión Bolivia ",
        "extraction_date": "08 de mayo de 2021  13 38 h",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "55",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned 09 May 2021 Advierten ascenso de casos de Covid por el frío y la relajación de medidas   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Advierten ascenso de casos de Covid por el frío y la relajación de medidas   Los Tiempos",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "56",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned 09 May 2021 Cochabamba es la segunda región con más nuevos casos de COVID 19 desde hace seis días   La Razón   Noticias de Bolivia y el Mundo",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Cochabamba es la segunda región con más nuevos casos de COVID 19 desde hace seis días   La Razón   Noticias de Bolivia y el Mundo",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "57",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned 09 May 2021 Grover León  “Estamos saturados para la tercera ola  así no va a dar”   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Grover León  “Estamos saturados para la tercera ola  así no va a dar”   Los Tiempos",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "58",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned 09 May 2021 Gualberti  No puede haber reconciliación y paz si no hay una justicia independiente   La Razón   Noticias de Bolivia y el Mundo",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Gualberti  No puede haber reconciliación y paz si no hay una justicia independiente   La Razón   Noticias de Bolivia y el Mundo",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "59",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned 09 May 2021 Informe que presentó el Gobierno ante la ONU tiene al menos 7 omisiones y contradicciones   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Informe que presentó el Gobierno ante la ONU tiene al menos 7 omisiones y contradicciones   Los Tiempos",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "60",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned 09 May 2021 Periodistas hacen frente a las crisis sanitaria  económica y política   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Periodistas hacen frente a las crisis sanitaria  económica y política   Los Tiempos",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
         "id": "61",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned 09 May 2021 Urbanizaciones y deforestación ponen en peligro La Angostura   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 09 May 2021 Urbanizaciones y deforestación ponen en peligro La Angostura   Los Tiempos",
        "extraction_date": "09 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "62",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned 11 de mayo de 2021  15 30 h   Arranca el control de las medidas de bioseguridad en el servicio de transporte público   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 11 de mayo de 2021  15 30 h   Arranca el control de las medidas de bioseguridad en el servicio de transporte público   Cochabamba   Opinión Bolivia ",
        "extraction_date": "11 de mayo de 2021  15 30 h",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "63",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned 19 Jun 2021 El Procurador llama ‘cínico’ a Mesa por negarse a testificar en el caso Golpe de Estado   La Razón   Noticias de Bolivia y el Mundo",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned 19 Jun 2021 El Procurador llama ‘cínico’ a Mesa por negarse a testificar en el caso Golpe de Estado   La Razón   Noticias de Bolivia y el Mundo",
        "extraction_date": "19 Jun 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "64",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned articles 12 de mayo de 2021  00 00 h   Comerciantes piden plan y  rayar la cancha  al Intendente   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles 12 de mayo de 2021  00 00 h   Comerciantes piden plan y  rayar la cancha  al Intendente   Cochabamba   Opinión Bolivia ",
        "extraction_date": "12 de mayo de 2021  00 00 h",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "65",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned articles 12 de mayo de 2021  16 49 h   Transporte bloquea contra ferrocarril Arica La Paz y deja varados a decenas de camiones en Suticollo   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles 12 de mayo de 2021  16 49 h   Transporte bloquea contra ferrocarril Arica La Paz y deja varados a decenas de camiones en Suticollo   Cochabamba   Opinión Bolivia ",
        "extraction_date": "12 de mayo de 2021  16 49 h",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "66",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned articles 14 de mayo de 2021  00 00 h   15 municipios prevén declarar emergencia por falta de agua   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles 14 de mayo de 2021  00 00 h   15 municipios prevén declarar emergencia por falta de agua   Cochabamba   Opinión Bolivia ",
        "extraction_date": "14 de mayo de 2021  00 00 h",
        "user_classification":  "None, 0, 1",
        "model_classification":  "None, 0, 1"
    },
    {
        "id": "67",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned articles 14 de mayo de 2021  11 35 h   Reyes Villa dice que hubo  megacorrupción  en la Alcaldía y anuncia audiencias públicas   Cochabamba   Opinión Bolivia ",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles 14 de mayo de 2021  11 35 h   Reyes Villa dice que hubo  megacorrupción  en la Alcaldía y anuncia audiencias públicas   Cochabamba   Opinión Bolivia ",
        "extraction_date": "14 de mayo de 2021  11 35 h",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "68",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned articles12 May 2021 10 clubes amenazan con paralizar el torneo por el caso Robert Blanco   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles12 May 2021 10 clubes amenazan con paralizar el torneo por el caso Robert Blanco   Los Tiempos",
        "extraction_date": "12 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "69",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned articles14 May 2021 Adepcoca anuncia movilizaciones en caso de que exista un proyecto del pago de impuestos   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles14 May 2021 Adepcoca anuncia movilizaciones en caso de que exista un proyecto del pago de impuestos   Los Tiempos",
        "extraction_date": "14 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    },
    {
        "id": "70",
        "source_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/articulos_pre_clasificados/malos_limpios/cleaned articles14 May 2021 La Paz decreta alerta naranja por Covid 19  gremios frenan la implementación de restricciones   Los Tiempos",
        "pre_processed_file_path": "D:/Universidad/semestre 11/taller/Proyecto/Articles-Classification/cleaned_articles/cleaned articles14 May 2021 La Paz decreta alerta naranja por Covid 19  gremios frenan la implementación de restricciones   Los Tiempos",
        "extraction_date": "14 May 2021",
        "user_classification": "None, 0, 1",
        "model_classification": "None, 0, 1"
    }]

if __name__ == '__main__':
    init_db()
    schema = ArticleSchema(many=True)
    result = schema.dump(articles_data)
    print(result)
