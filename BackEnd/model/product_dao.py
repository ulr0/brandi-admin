import pymysql

from util.const import END_DATE, MASTER_ACCOUNT_TYPE, SELLER_ACCOUNT_TYPE


class ProductDao:

    def get_product_list(self, connection, filters, is_count=False):
        """상품 관리 리스트

        Author:
            이서진

        Args:
            connection: 커넥션
            filters: 필터 조건
            is_count: 카운트 조건 여부

        Returns:
        """

        query = "SELECT"

        if is_count is True:
            query += " Count(*) AS count"

        else:
            if filters.get("account_type") == "master":
                query += " ss.name AS seller_category,"

            query += """
                p.created_at AS created_at,
                pi.image_url AS image_url,
                ph.name AS name,
                p.product_code AS product_code,
                p.Id AS product_number,
                ph.price AS price,
                ph.discount_rate AS discount_rate,
                ph.is_sold AS is_sold,
                ph.is_displayed AS is_displayed,
                ph.discount_start_time AS discount_start_time,
                ph.discount_end_time AS discount_end_time,
                ph.price - TRUNCATE((ph.price * (ph.discount_rate/100)), -1) AS sale_price,
                sh.korean_name AS seller_name
            """

        query += f"""
            FROM products AS p
                INNER JOIN product_images AS pi
                    ON p.Id = pi.product_id
                INNER JOIN product_histories AS ph
                    ON p.Id = ph.product_id
                INNER JOIN sellers AS s
                    ON p.seller_id = s.Id
                INNER JOIN seller_subcategories AS ss
                    ON s.seller_subcategory_id = ss.Id
                INNER JOIN seller_histories AS sh
                    ON s.Id = sh.seller_id
            WHERE ph.is_deleted = false
              AND ph.end_time = '{END_DATE}'
              AND pi.is_main = true
        """

        if filters.get("start_date") and filters.get("end_date"):
            query += " AND p.created_at BETWEEN %(start_date)s AND %(end_date)s"

        if filters.get("start_date") and filters.get("end_date") is None:
            query += " AND p.created_at > %(start_date)s"

        if filters.get("start_date") is None and filters.get("end_date"):
            query += " AND p.created_at < %(end_date)s"

        if filters.get("product_name"):
            query += " AND ph.name LIKE %(product_name)s"

        if filters.get("product_number"):
            query += " AND p.Id = %(product_number)s"

        if filters.get("product_code"):
            query += " AND p.product_code = %(product_code)s"

        if filters.get("is_sold") is not None:
            query += " AND ph.is_sold = %(is_sold)s"

        if filters.get("is_displayed") is not None:
            query += " AND ph.is_displayed = %(is_displayed)s"

        if filters.get("is_sale") is True:
            query += """
                AND ph.discount_rate IS NOT NULL
                AND NOW() BETWEEN ph.discount_start_time AND ph.discount_end_time
            """

        if filters.get("is_sale") is False:
            query += """
                AND (ph.discount_rate IS NULL
                 OR (NOW() NOT BETWEEN ph.discount_start_time AND ph.discount_end_time))
            """

        if filters.get("account_type") == SELLER_ACCOUNT_TYPE:
            query += " AND p.seller_id = %(account_id)s"

        elif filters.get("account_type") == MASTER_ACCOUNT_TYPE:

            if filters.get("seller_name_en"):
                query += " AND sh.english_name LIKE %(seller_name_en)s"

            if filters.get("seller_name_kr"):
                query += " AND sh.korean_name LIKE %(seller_name_kr)s"

            if filters.get("seller_category"):
                if len(filters.get("seller_category")) == 1:
                    query += " AND ss.id = %(seller_category)s"
                else:
                    query += " AND ss.id IN %(seller_category)s"

        if is_count is False:
            query += " ORDER BY p.created_at DESC"
            query += " LIMIT %(offset)s, %(limit)s"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filters)
            return cursor.fetchall()

    def select_product_history_id(self, connection, data):
        query = f"""
            SELECT id
            FROM product_histories
            WHERE is_deleted = false
              AND end_time = '{END_DATE}'
              AND product_id = %(product_id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            result = cursor.fetchone()
            return result["id"]

    def update_product_history_end_time(self, connection, data, now):
        query = f"""
            UPDATE product_histories
            SET end_time = '{now}'
            WHERE id = %(product_history_id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            return cursor.execute(query, data)

    def insert_product_history(self, connection, data, now):
        query = f"""
            INSERT INTO product_histories(
                account_id,
                product_id,
                product_subcategory_id,
                `name`,
                shipment_information,
                price,
                detail_page_html,
                discount_rate,
                discount_start_time,
                discount_end_time,
                minimum_sell_quantity,
                maximum_sell_quantity,
                comment,
                start_time,
                end_time,
                is_deleted,
                manufacturer,
                manufactured_date,
                origin,
                is_sold,
                is_displayed
                )
            SELECT account_id,
                product_id,
                product_subcategory_id,
                `name`,
                shipment_information,
                price,
                detail_page_html,
                discount_rate,
                discount_start_time,
                discount_end_time,
                minimum_sell_quantity,
                maximum_sell_quantity,
                comment,
                '{now}',
                '{END_DATE}',
                is_deleted,
                manufacturer,
                manufactured_date,
                origin,
        """

        if "is_sold" in data:
            query += "%(is_sold)s,"
        else:
            query += "is_sold,"

        if "is_displayed" in data:
            query += "%(is_displayed)s"
        else:
            query += "is_displayed"

        query += f"""
            FROM product_histories
            WHERE id = %(product_history_id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            return cursor.execute(query, data)

    def get_product_category_list(self, connection, filters):
        query = """
            SELECT id, name
            FROM product_categories
            WHERE seller_subcategory_id = %(seller_category_id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filters)
            return cursor.fetchall()

    def get_product_subcategory_list(self, connection, filters):
        query = """
            SELECT id, name
            FROM product_subcategories
            WHERE product_category_id = %(product_category_id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filters)
            return cursor.fetchall()

    def insert_new_product(self, connection, data):

        print(data)
        query = """
            INSERT INTO products (
                account_id,
                seller_id,
                created_at
            )
            VALUES (
                %(account_id)s,
                %(seller_id)s,
                NOW()
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            return cursor.lastrowid

    def insert_new_product_history(self, connection, data):
        query = f"""
            INSERT INTO product_histories (
                account_id,
                product_id,
                product_subcategory_id,
                `name`,
                price,
                detail_page_html,
                is_sold,
                is_displayed,
                minimum_sell_quantity,
                maximum_sell_quantity,
                comment,
                start_time,
                end_time,
            """

        if data.get("discount_rate") is not None:
            query += """
                discount_rate,
                discount_start_time,
                discount_end_time,
            """

        if data.get("manufacturer") is not None:
            query += """
                manufacturer,
                manufactured_date,
                origin,
            """

        query += f"""
                is_deleted
            )
            VALUES (
                %(account_id)s,
                %(product_id)s,
                %(product_subcategory_id)s,
                %(name)s,
                %(price)s,
                %(detail_page_html)s,
                %(is_sold)s,
                %(is_displayed)s,
                %(minimum_sell_quantity)s,
                %(maximum_sell_quantity)s,
                %(comment)s,
                NOW(),
                '{END_DATE}',
        """

        if data.get("discount_rate") is not None:
            query += """
                %(discount_rate)s,
                %(discount_start_time)s,
                %(discount_end_time)s,
            """

        if data.get("manufacturer") is not None:
            query += """
                %(manufacturer)s,
                %(manufactured_date)s,
                %(origin_id)s,
            """

        query += """
                False
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            return cursor.execute(query, data)

    def insert_new_product_options(self, connection, option):
        query = """
            INSERT INTO product_options (
                product_id,
                size_id,
                color_id,
        """

        if option.get("stock") is not None:
            query += "stock,"

        query += """
                is_sold_out
            )
            VALUES (
                %(product_id)s,
                %(size_id)s,
                %(color_id)s,
        """

        if option.get("stock") is not None:
            query += "%(stock)s,"

        query += """
                false
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            return cursor.execute(query, option)

    def insert_new_product_image(self, connection, data):
        query = """
            INSERT INTO product_images (
                product_id,
                image_url,
                is_main
            )
            VALUES (
                %(product_id)s,
                %(image_url)s,
                %(is_main)s
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            return cursor.execute(query, data)

