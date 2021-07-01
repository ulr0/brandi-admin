import pymysql

from util.const import OPEN_STORE


class SearchDao:
    def get_seller_name_search_list(self, connection, filters):
        query = f"""
            SELECT
                s.Id,
                s.seller_subcategory_id,
                sh.korean_name,
                sh.english_name
            FROM seller_histories AS sh
                INNER JOIN sellers AS s
                    ON s.Id = sh.seller_id
            WHERE (korean_name LIKE %(search_word)s OR english_name LIKE %(search_word)s)
              AND action_status_id = {OPEN_STORE}
            LIMIT %(limit)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filters)
            return cursor.fetchall()
