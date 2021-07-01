import pymysql


class UtilDao:

    def select_now(self, connection):
        query = "SELECT NOW() AS now"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return result.get("now")
