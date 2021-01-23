import pymysql

from amazon import settings

db = pymysql.connect(
    host=settings.MYSQL_HOST,
    user=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWORD,
    database=settings.MYSQL_DB,
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = db.cursor()


class Sql:

    @classmethod
    def getBestsellerURL(cls, params):
        sql = """
            SELECT url, country FROM bestsellerURL WHERE category = %s and country = %s
        """
        cursor.execute(sql, (params["category"], params["country"]))
        return cursor.fetchall()
