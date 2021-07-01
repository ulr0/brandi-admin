import pymysql

from util.const import END_DATE

class MasterDao:
    def get_seller_list(self, connection, filter):
        """셀러 계정 목록을 조회

        Author:
            김현영
        
        Args:
            connection (객체): pymysql 객체
            filter (dict): {
                "seller_id"          : 셀러 번호,
                "seller_nickname"    : 셀러 아이디,
                "english_name"       : 셀러 상호 영문이름,
                "korean_name"        : 셀러 상호 한글이름,
                "seller_type"        : 셀러 구분,
                "clerk_name"         : 담당자 이름,
                "clerk_phone_number" : 담당자 연락처,
                "clerk_email"        : 담당자 이메일,
                "start_date"         : 조회 시작 일자,
                "end_date"           : 조회 종료 일자,
                "action_status_id"   : 셀러 상태 아이디,
                "action_status"      : 셀러 상태,
                "offset"             : 보여줄 데이터 시작,
                "limit"              : 보여줄 데이터 개수
            }
        
        Raises:
            e: [description]
        
        Returns:
            list :  [
                        {
                            "Id"                 : 셀러번호,
                            "action_status_id"   : 셀러 상태 아이디,
                            "clerk_email"        : 담당자 이메일,
                            "clerk_name"         : 담당자 이름,
                            "clerk_phone_number" : 담당자 연락처,
                            "created_at"         : 셀러 계정 생성날짜,
                            "english_name"       : 셀러상호 영문명,
                            "korean_name"        : 셀러상호 한글명,
                            "product_count"      : 보유 상품 개수,
                            "seller_attribute"   : 셀러 카테고리명,
                            "seller_id"          : 셀러 아이디,
                            "seller_type"        : 셀러 구분,
                            "status"             : 셀러 상태
                        }
                    ]
        """
        query = f"""
            SELECT
                a.Id,
                a.nickname AS seller_id,
                sh.korean_name,
                sh.english_name,
                st.seller_type,
                sl.name AS clerk_name,
                `as`.Id AS action_status_id,
                `as`.status,
                sl.phone_number AS clerk_phone_number,
                sl.email AS clerk_email,
                ss.name AS seller_attribute,
                (
                    SELECT
                        COUNT(*)
                    FROM products AS p
                        INNER JOIN product_histories AS ph
                                ON p.Id = ph.product_id
                    WHERE
                        p.seller_id = s.Id
                        AND ph.is_deleted = false
                ) AS product_count,
                a.created_at
            FROM accounts AS a
                INNER JOIN sellers AS s
                        ON a.Id = s.Id
                INNER JOIN seller_histories AS sh
                        ON s.Id = sh.seller_id
                INNER JOIN seller_subcategories AS ss
                        ON ss.Id = s.seller_subcategory_id
                INNER JOIN seller_categories AS sc
                        ON ss.seller_category_id = sc.Id
                INNER JOIN seller_types AS st
                        ON sc.seller_type_id = st.Id
                INNER JOIN action_status AS `as`
                        ON sh.action_status_id = `as`.Id
                LEFT JOIN seller_clerks AS sl
                        ON sl.Id = 
                        (SELECT
                             MIN(Id)
                         FROM 
                            seller_clerks
                         WHERE 
                            seller_id = s.Id
                            AND is_deleted = false)
            WHERE
                sh.end_time = "{END_DATE}"
                AND sh.is_deleted = false
        """

        if filter.get("seller_id"):
            query += " AND a.Id LIKE %(seller_id)s"

        if filter.get("seller_nickname"):
            query += " AND a.nickname LIKE %(seller_nickname)s"
        
        if filter.get("english_name"):
            query += " AND sh.english_name LIKE %(english_name)s"

        if filter.get("korean_name"):
            query += " AND sh.korean_name LIKE %(korean_name)s"

        if filter.get("seller_type"):
            query += " AND st.Id LIKE %(seller_type)s"
                    
        if filter.get("clerk_name"):
            query += " AND sl.name LIKE %(clerk_name)s"
        
        if filter.get("clerk_phone_number"):
            query += " AND sl.phone_number LIKE %(clerk_phone_number)s"
        
        if filter.get("clerk_email"):
            query += " AND sl.email LIKE %(clerk_email)s"
        
        if filter.get("action_status"):
            query += " AND `as`.Id = %(action_status)s"
        
        if filter.get("seller_attribute"):
            query += " AND ss.Id = %(seller_attribute)s"

        if filter.get("start_date"):
            query += " AND a.created_at >= %(start_date)s"
        
        if filter.get("end_date"):
            query += " AND a.created_at <= %(end_date)s"
        
        if filter.get("limit"):
            if "offset" in filter:
                query += " LIMIT %(offset)s, %(limit)s"
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filter)
            return cursor.fetchall()
        
      
    def get_seller_list_count(self, connection, filter):
        """셀러 계정 목록의 총 계정수 조회.
        
        Author:
            김현영
        
        Args:
            connection (객체): pymysql 객체
            filter (dict): {
                "seller_id"          : 셀러 번호,
                "seller_nickname"    : 셀러 아이디,
                "english_name"       : 셀러 상호 영문이름,
                "korean_name"        : 셀러 상호 한글이름,
                "seller_type"        : 셀러 구분,
                "clerk_name"         : 담당자 이름,
                "clerk_phone_number" : 담당자 연락처,
                "clerk_email"        : 담당자 이메일,
                "start_date"         : 조회 시작 일자,
                "end_date"           : 조회 종료 일자,
                "action_status_id"   : 셀러 상태 아이디,
                "action_status"      : 셀러 상태,
                "offset"             : 보여줄 데이터 시작,
                "limit"              : 보여줄 데이터 개수
            }
        
        Raises:
            e: [description]
        
        Returns:
            dict : {"count" : 총 셀러 계정수 }       
        """
        query = f"""
            SELECT
                COUNT(*) AS count
            FROM accounts AS a
                INNER JOIN sellers AS s
                        ON a.Id = s.Id
                INNER JOIN seller_histories AS sh
                        ON s.Id = sh.seller_id
                INNER JOIN seller_subcategories AS ss
                        ON ss.Id = s.seller_subcategory_id
                INNER JOIN seller_categories AS sc
                        ON ss.seller_category_id = sc.Id
                INNER JOIN seller_types AS st
                        ON sc.seller_type_id = st.Id
                INNER JOIN action_status AS `as`
                        ON sh.action_status_id = `as`.Id
                LEFT JOIN seller_clerks AS sl
                        ON sl.Id = 
                        (SELECT
                             MIN(Id)
                         FROM 
                            seller_clerks
                         WHERE 
                            seller_id = s.Id
                            AND is_deleted = false)
            WHERE
                sh.end_time = "{END_DATE}"
                AND sh.is_deleted = false
        """

        if filter.get("seller_id"):
            query += " AND a.Id LIKE %(seller_id)s"

        if filter.get("seller_nickname"):
            query += " AND a.nickname LIKE %(seller_nickname)s"
        
        if filter.get("english_name"):
            query += " AND sh.english_name LIKE %(english_name)s"

        if filter.get("korean_name"):
            query += " AND sh.korean_name LIKE %(korean_name)s"

        if filter.get("seller_type"):
            query += " AND st.Id LIKE %(seller_type)s"
        
        if filter.get("clerk_name"):
            query += " AND sl.name LIKE %(clerk_name)s"
        
        if filter.get("clerk_phone_number"):
            query += " AND sl.phone_number LIKE %(clerk_phone_number)s"
        
        if filter.get("clerk_email"):
            query += " AND sl.email LIKE %(clerk_email)s"
        
        if filter.get("action_status"):
            query += " AND `as`.Id = %(action_status)s"
        
        if filter.get("seller_attribute"):
            query += " AND ss.Id = %(seller_attribute)s"

        if filter.get("start_date"):
            query += " AND a.created_at >= %(start_date)s"
        
        if filter.get("end_date"):
            query += " AND a.created_at <= %(end_date)s"
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, filter)
            return cursor.fetchone()

    def get_master_action_list(self, connection):
        """셀러 상태 변경 액션 목록 조회
        
        Author:
            김현영
        
        Args:
            connection (객체): pymysql 객체
        
        Raises:
        
        Returns:
            list : [ 
                        {
                            "action_status_id" : 셀러 상태 번호, 
                            "master_action_id" : 마스터 액션 번호,
                            "status" : 셀러 상태, 
                            "action" : 마스터 액션
                         }
                    ]    
        """
        query = """
            SELECT
                `as`.Id AS action_status_id,
                ma.Id AS master_action_id,
                `as`.status,
                ma.action
            FROM status_masters
            INNER JOIN action_status AS `as`
                    ON status_masters.action_status_id = `as`.Id
            INNER JOIN master_actions AS ma
                    ON status_masters.master_action_id = ma.Id
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    
    def get_seller_history_id(self, connection, data):
        """셀러의 최신 이력 데이터의 PK값 조회.
        
        Author:
            김현영
        
        Args:
            connection (객체): pymysql 객체
            data (dict): {
                "account_id"       : 이력을 수정한 계정 번호,
                "seller_id"        : 셀러 번호,
                "master_action_id" : 마스터가 실행한 action번호
            }
        
        Raises:
        
        Returns:
            dict : { "Id" : 해당 셀러의 마지막 이력 데이터의 PK값 }    
        """
        query = f"""
            SELECT
                Id
            FROM 
                seller_histories AS sh
            WHERE
                sh.seller_id = %(seller_id)s
                AND sh.is_deleted = false
                AND sh.end_time = "{END_DATE}"
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            return cursor.fetchone()

    def update_seller_history_end_time(self, connection, data, now):
        """셀러 이력의 end_time을 갱신.
        
        Author:
            김현영
        
        Args:
            connection (객체): pymysql 객체
            data (dict): {
                "account_id"       : 이력을 수정한 계정 번호,
                "seller_id"        : 셀러 번호,
                "master_action_id" : 마스터가 실행한 action번호
            }
            now (datetime): 이력 변경을 실행한 시간 
        
        Raises:
        
        Returns:
            int : 쿼리를 실행하여 갱신된 row 개수   
        """
        query = f"""
            UPDATE 
                seller_histories
            SET 
                end_time = "{now}"
            WHERE 
                is_deleted = false
                AND seller_id = %(seller_id)s
                AND end_time = "{END_DATE}"
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            return cursor.execute(query, data)

    def change_action_status_and_insert(self, connection, data, now):
        """셀러 상태를 갱신하여 새로운 이력 데이터 생성.
        
        Author:
            김현영
        
        Args:
            connection (객체): pymysql 객체
            data (dict): {
                "account_id"       : 이력을 수정한 계정 번호,
                "seller_id"        : 셀러 번호,
                "action_status_id" : 셀러 상태 번호
            }
            now (datetime): 이력 변경을 실행한 시간 
        
        Raises:
        
        Returns:
            int : 쿼리를 실행하여 갱신된 row 개수   
        """
        query = f"""
            INSERT INTO seller_histories(
                account_id,
                action_status_id,
                seller_id,
                password,
                seller_phone_number,
                korean_name,
                english_name,
                cs_phone_number,
                cs_nickname,
                start_time,
                end_time,
                is_deleted,
                refund_information,
                profile_image_url,
                shipment_information,
                background_image_url,
                comment,
                detail_comment,
                address,
                detail_address,
                zip_code,
                cs_start_time,
                cs_end_time,
                is_opened_cs
            )
            SELECT
                %(account_id)s,
                %(action_status_id)s,
                seller_id,
                password,
                seller_phone_number,
                korean_name,
                english_name,
                cs_phone_number,
                cs_nickname,
                "{now}",
                "{END_DATE}",
                is_deleted,
                refund_information,
                profile_image_url,
                shipment_information,
                background_image_url,
                comment,
                detail_comment,
                address,
                detail_address,
                zip_code,
                cs_start_time,
                cs_end_time,
                is_opened_cs
            FROM 
                seller_histories AS sh
            WHERE
                sh.seller_id = %(seller_id)s
                AND sh.Id = %(seller_history_id)s
                AND sh.is_deleted = false
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            return cursor.execute(query, data)
            
