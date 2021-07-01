from flask import request

import pymysql

from util.const import (ORDER_STATUS_PRODUCT_PREPARE, SHIPMENT_STATUS_BEFORE_DELIVERY, 
                        ORDER_STATUS_SHIPPING, SHIPMENT_STATUS_SHIPPING,
                        END_DATE)

class ProductPrepareDao:
    def get_product_prepare(self, connection, filter):
        query = f"""
            SELECT 
                o.paid_at, 
                o.id AS order_id, 
                op.id AS order_product_id, 
                sh.korean_name AS seller_name, 
                ph.`name` AS product_name,
                CONCAT(c.color, "/", sz.size) AS option_info, 
                po.extra_price, 
                oph.quantity, 
                oh.`name` AS order_name, 
                oh.phone_number AS order_phone, 
                oh.total_price, 
                oph.order_status_id,
                os.order_status
            FROM orders AS o
                INNER JOIN order_products AS op
                    ON o.id = op.order_id   
                INNER JOIN products AS p
                    ON op.product_id = p.id
                INNER JOIN order_histories AS oh 
                    ON o.id = oh.order_id
                INNER JOIN order_product_histories AS oph
                    ON op.id = oph.order_product_id 
                INNER JOIN product_histories AS ph
                    ON p.id = ph.product_id
                INNER JOIN seller_histories AS sh 
                    ON p.seller_id = sh.seller_id 
                INNER JOIN sellers AS s
                    ON sh.seller_id = s.id
                INNER JOIN shipments AS sm 
                    ON op.id = sm.order_product_id
                INNER JOIN product_options AS po 
                    ON op.product_option_id = po.id
                INNER JOIN sizes AS sz 
                    ON po.size_id = sz.id
                INNER JOIN colors AS c 
                    ON po.color_id = c.id
                INNER JOIN order_status AS os 
                    ON oph.order_status_id = os.id
            WHERE 
                sm.shipment_status_id = {SHIPMENT_STATUS_BEFORE_DELIVERY}
                AND oph.order_status_id = {ORDER_STATUS_PRODUCT_PREPARE}
                """

        if filter.get("start_date"):
            query += " AND o.paid_at >= %(start_date)s"
        
        if filter.get("end_date"):
            query += " AND o.paid_at <= %(end_date)s"

        if filter.get("order_id"): 
            query += " AND o.id LIKE %(order_id)s"

        if request.path == "/order/product-prepare":
            if filter.get("order_product_id"):
                query += " AND op.id LIKE %(order_product_id)s"
        
        if filter.get("order_name"):
            query += " AND oh.`name` LIKE %(order_name)s"

        if filter.get("order_phone"):
            query += " AND oh.phone_number LIKE %(order_phone)s"

        if filter.get("seller_name"):
            query += " AND sh.korean_name LIKE %(seller_name)s"

        if filter.get("product_name"):
            query += " AND ph.`name` LIKE %(product_name)s"

        if type(filter.get("seller_attribute")) == int:
            query += " AND s.seller_subcategory_id = %(seller_attribute)s"

        if type(filter.get("seller_attribute")) == tuple:
            query += " AND s.seller_subcategory_id IN %(seller_attribute)s"

        if filter.get("account_id"):
            query += " AND s.id = %(account_id)s"

        if request.path == "/order/product-prepare/download":
            if type(filter.get('order_product_id')) == int:
                query += " AND op.id = %(order_product_id)s"

            if type(filter.get("order_product_id")) == tuple:
                query += " AND op.id in %(order_product_id)s"

        if filter.get("order_by") == 1:
            query += " ORDER BY o.paid_at DESC"

        else:
            query += " ORDER BY o.paid_at ASC"

        if filter.get("limit"):
                query += " LIMIT %(offset)s, %(limit)s"
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filter)

            return cursor.fetchall()

    def get_product_prepare_count(self, connection, filter):
        query = f"""
            SELECT
                COUNT(*) AS count
            FROM orders AS o
                INNER JOIN order_products AS op
                    ON o.id = op.order_id
                INNER JOIN products AS p
                    ON op.product_id = p.id
                INNER JOIN order_histories AS oh
                    ON o.id = oh.order_id
                INNER JOIN order_product_histories AS oph
                    ON op.id = oph.order_product_id
                INNER JOIN product_histories AS ph
                    ON p.id = ph.product_id
                INNER JOIN seller_histories AS sh
                    ON p.seller_id = sh.seller_id
                INNER JOIN sellers AS s
                    ON sh.seller_id = s.id
                INNER JOIN shipments AS sm
                    ON op.id = sm.order_product_id
                INNER JOIN product_options AS po
                    ON op.product_option_id = po.id
                INNER JOIN sizes AS sz
                    ON po.size_id = sz.id
                INNER JOIN colors AS c
                    ON po.color_id = c.id
                INNER JOIN order_status AS os 
                    ON oph.order_status_id = os.id
            WHERE
                sm.shipment_status_id = {SHIPMENT_STATUS_BEFORE_DELIVERY}
                AND oph.order_status_id = {ORDER_STATUS_PRODUCT_PREPARE}
                """

        if filter.get("start_date"):
            query += " AND o.paid_at >= %(start_date)s"
        
        if filter.get("end_date"):
            query += " AND o.paid_at <= %(end_date)s"

        if filter.get("order_number"):
            query += " AND o.id LIKE %(order_id)s"

        if filter.get("order_detail_number"):
            query += " AND op.id LIKE %(order_product_id)s"

        if filter.get("order_name"):
            query += " AND oh.`name` LIKE %(order_name)s"

        if filter.get("order_phone"):
            query += " AND oh.phone_number LIKE %(order_phone)s"

        if filter.get("seller_name"):
            query += " AND sh.korean_name LIKE %(seller_name)s"

        if filter.get("product_name"):
            query += " AND ph.`name` LIKE %(product_name)s"
        
        if filter.get("account_id"):
            query += " AND s.id = %(account_id)s"

        if type(filter.get("seller_attribute")) == int:
            query += " AND s.seller_subcategory_id = %(seller_attribute)s"

        if type(filter.get("seller_attribute")) == tuple:
            query += " AND s.seller_subcategory_id IN %(seller_attribute)s"

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filter)

            return cursor.fetchone()

    def select_log_primary_key(self, connection, order_product):
        query = f"""
            SELECT oph.id
                FROM order_product_histories AS oph
            INNER JOIN order_products AS op
                ON oph.order_product_id = op.id
            INNER JOIN products AS p 
                ON op.product_id = p.id
            WHERE oph.order_status_id = {ORDER_STATUS_PRODUCT_PREPARE}
                AND oph.end_time = %(end_date)s
                AND oph.order_product_id = %(order_product_id)s
            """

        if order_product.get("account_id"):
            query += " AND p.seller_id = %(account_id)s"
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, order_product)

            return cursor.fetchone()

    def patch_order_log_end(self, connection, order_product):
        query = f"""
            UPDATE  
                order_product_histories AS oph
            INNER JOIN order_products AS op
                ON oph.order_product_id = op.id
            INNER JOIN products AS p
                ON op.product_id = p.id
            SET 
                oph.end_time = %(now)s
            WHERE 
                oph.order_status_id = {ORDER_STATUS_PRODUCT_PREPARE}
                AND oph.order_product_id = %(order_product_id)s
                AND oph.end_time = %(end_date)s
            """
        
        if order_product.get("account_id"):
            query += " AND p.seller_id = %(account_id)s"
        
        with connection.cursor() as cursor:
            
            return cursor.execute(query, order_product)

    def patch_order_log_start(self, connection, order_product):
        query = f"""
            INSERT INTO 
                order_product_histories(
                    order_status_id,
                    order_product_id,
                    start_time,
                    end_time,
                    is_canceled,
                    price,
                    quantity
                )
            SELECT
                {ORDER_STATUS_SHIPPING},
                oph.order_product_id,
                %(now)s,
                %(end_date)s,
                oph.is_canceled,
                oph.price,
                oph.quantity
            FROM 
                order_product_histories AS oph
            INNER JOIN order_products AS op
                ON oph.order_product_id = op.id
            INNER JOIN products AS p
                ON op.product_id = p.id
            WHERE
                oph.order_status_id = {ORDER_STATUS_PRODUCT_PREPARE}
                AND oph.order_product_id = %(order_product_id)s
                AND oph.id = %(order_product_history_id)s
                """
        
        if order_product.get("account_id"):
            query += " AND p.seller_id = %(account_id)s"

        with connection.cursor() as cursor:
            
            return cursor.execute(query, order_product)

    def patch_shipments_info(self, connection, order_product):
        query = f"""
            UPDATE 
                shipments AS sm
            INNER JOIN order_products AS op
                ON sm.order_product_id = op.id
            INNER JOIN order_product_histories AS oph
                ON op.id = oph.order_product_id
            INNER JOIN products AS p
                ON op.product_id = p.id
            SET 
                sm.shipment_status_id = {SHIPMENT_STATUS_SHIPPING},
                sm.start_time = %(now)s
            WHERE sm.order_product_id = %(order_product_id)s
                AND oph.order_status_id = {ORDER_STATUS_SHIPPING}
                AND oph.start_time = %(now)s
                AND oph.end_time = %(end_date)s
                """

        if order_product.get("account_id"):
            query += " AND p.seller_id = %(account_id)s"

        with connection.cursor() as cursor:

            return cursor.execute(query, order_product)