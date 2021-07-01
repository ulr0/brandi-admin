import pymysql

from util.const import END_DATE


class AccountDao:
    # 어드민 회원가입 시 accounts 테이블에 삽입
    def join(self, data, connection): 
        query = """
            INSERT INTO accounts(
                nickname, 
                created_at,
                account_type_id
            )
            VALUES(
                %(nickname)s,
                NOW(),
                %(account_type_id)s
            )    
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            return cursor.lastrowid

    # 데이터베이스에 존재하는 닉네임인지 확인
    def is_existed_account(self, data, connection):
        query = """
            SELECT
                Id
            FROM
                accounts
            WHERE
                nickname = %(nickname)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            return cursor.execute(query, data)
            
            

    # 어드민 계정의 타입을 확인     
    def get_account_type(self, data, connection):
        query = """
            SELECT
                account_type
            FROM
                account_type
            WHERE
                Id = %(account_type_id)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            return cursor.fetchone()

    def get_account_id(self, data, connection):
        query = """
            SELECT
                Id,
                account_type_id
            FROM
                accounts 
            WHERE
                nickname = %(nickname)s
        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            return cursor.fetchone()

    # 셀러 회원가입 시 seller 테이블에 삽입
    def seller_join_info(self, data, connection):
        query = """
            INSERT INTO sellers(
                Id,
                seller_subcategory_id
            )
            VALUES(
                %(Id)s,
                %(seller_subcategory_id)s
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            return cursor.lastrowid
    
    # 마스터 회원가입 시 master 테이블에 삽입
    def master_join_info(self, data, connection):
        query = """
            INSERT INTO masters(
                Id
            )
            VALUES(
                %(Id)s
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            return cursor.lastrowid
    
    # 셀러 회원가입 시 seller 정보 삽입
    def seller_join_history(self, data, connection):
        data['END_DATE'] = END_DATE
        query = """
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
                is_deleted
            )
            VALUES(
                %(account_id)s,
                %(action_status_id)s,
                %(seller_id)s,
                %(password)s,
                %(seller_phone_number)s,
                %(korean_name)s,
                %(english_name)s,
                %(cs_phone_number)s,
                %(cs_nickname)s,
                NOW(),
                %(END_DATE)s,
                false
            )
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            return cursor.lastrowid

    # 마스터 회원가입 시 master_histories 테이블에 삽입
    def master_join_history(self, data, connection):
        data['END_DATE'] = END_DATE
        query = """
           INSERT INTO master_histories(
                master_id,
                password,
                start_time,
                end_time,
                is_deleted
            )
            VALUES(
                %(master_id)s,
                %(password)s,
                NOW(),
                %(END_DATE)s,
                false
            ) 
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            return cursor.lastrowid    

    
    def check_seller(self, data, connection):
        data['END_DATE'] = END_DATE
        query = """
            SELECT
                a.account_type_id,
                sh.password,
                sh.action_status_id,
                sh.is_deleted
            FROM
                accounts as a
            INNER JOIN sellers AS s
                    ON a.Id = s.Id
            INNER JOIN seller_histories AS sh
                    ON s.Id = sh.seller_id
            WHERE 
                a.Id = %(account_id)s
            AND 
                sh.end_time = %(END_DATE)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            return cursor.fetchone()

    def check_master(self, data, connection):
        data['END_DATE'] = END_DATE
        query = """
            SELECT
                a.account_type_id,
                mh.password,
                mh.is_deleted
            FROM
                accounts as a
            INNER JOIN masters AS m
                    ON a.Id = m.Id
            INNER JOIN master_histories AS mh
                    ON m.Id = mh.master_id
            WHERE 
                a.Id = %(account_id)s
            AND 
                mh.end_time = %(END_DATE)s
        """

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query, data)
            return cursor.fetchone()