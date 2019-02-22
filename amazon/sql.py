import pymysql

from amazon import settings

db = pymysql.connect(
    settings.MYSQL_HOST,
    settings.MYSQL_USER,
    settings.MYSQL_PASSWORD,
    settings.MYSQL_DB,
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = db.cursor()


class Sql:

    @classmethod
    def getBestsellerURL(cls, params):
        sql = """
            SELECT url FROM bestsellerURL WHERE category_title = %s
        """
        cursor.execute(sql, (params["category_title"]))
        return cursor.fetchall()
