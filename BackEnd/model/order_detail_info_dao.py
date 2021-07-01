import pymysql

class OrderDetailInfoDao:
    def get_order_detail_info(self, connection, data):
        query = """
            SELECT 
                o.id AS order_id,
                o.created_at AS order_created_at,
                oh.total_price, 
                op.id AS order_product_id, 
                os.order_status, 
                o.paid_at, 
                oph.order_status_id, 
                uh.phone_number AS order_phone, 
                p.id AS product_id, 
                ph.`name` AS product_name, 
                oph.price, 
                oph.discount_rate, 
                oph.price - truncate(oph.price * (oph.discount_rate / 100), -1) AS sale_price, 
                sh.korean_name AS seller_name, 
                CONCAT(c.color, "/", sz.size) AS option_info,  
                oph.quantity, 
                po.extra_price, 
                u.id AS user_id, 
                oh.`name` AS order_name, 
                adh.`name` AS receive_name, 
                adh.phone_number AS receive_phone, 
                adh.address,
                adh.additional_address,
                adh.zip_code, 
                smm.content AS shipment_message, 
                sm.message
            FROM order_products AS op
            INNER JOIN orders AS o 
                ON op.order_id = o.id
            INNER JOIN order_histories AS oh 
            ON o.id = oh.order_id
            INNER JOIN order_product_histories AS oph 
                ON op.id = oph.order_product_id
            INNER JOIN order_status AS os 
                ON oph.order_status_id = os.id 
            INNER JOIN users AS u 
                ON o.user_id = u.id 
            INNER JOIN user_histories AS uh 
                ON u.id = uh.user_id 
            INNER JOIN product_options AS po 
                ON op.product_option_id = po.id 
            INNER JOIN products AS p 
                ON po.product_id = p.id 
            INNER JOIN product_histories AS ph 
                ON p.id = ph.product_id 
            INNER JOIN sellers AS s 
                ON p.seller_id = s.id 
            INNER JOIN seller_histories AS sh 
                ON s.id = sh.seller_id 
            INNER JOIN sizes AS sz 
                ON po.size_id = sz.id 
            INNER JOIN colors AS c 
                ON po.color_id = c.id 
            INNER JOIN shipments AS sm 
                ON op.id = sm.order_product_id 
            INNER JOIN addresses AS ad 
                ON sm.address_id = ad.id 
            INNER JOIN address_histories AS adh 
                ON ad.id = adh.address_id 
            INNER JOIN shipment_memo as smm 
                ON sm.shipment_memo_id = smm.id 
            WHERE op.id = %(order_product_id)s
                AND oph.end_time = %(end_date)s
            """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
        
            return cursor.fetchone()

    def get_order_log(self, connection, data):
        query = """
            SELECT 
                oph.start_time, 
                oph.end_time,  
                os.order_status 
            FROM order_product_histories as oph 
            INNER JOIN order_status AS os 
                ON oph.order_status_id = os.id 
            WHERE oph.order_product_id = %(order_product_id)s
            """
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)

            return cursor.fetchall()