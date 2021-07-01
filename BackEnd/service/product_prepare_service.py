from flask import jsonify

from model                import ProductPrepareDao, OrderDetailInfoDao, UtilDao
from service.util_service import UtilService
from util.const           import END_DATE
from util.exception       import InvalidRequest, ProcessingFailureError
from util.message         import INVALID_REQUEST

class ProductPrepareService:
    def get_product_prepare(self, connection, filter):
        """셀러의 최신 이력 데이터의 PK값 조회.
        Author:
            서득영
        Args:
            connection: pymysql 객체
            filter: 데이터 검색 조건

        Raises:

        Returns:
            { "data" : 조회된 데이터, "count" : 데이터 전체 개수}    
            """
            
        product_prepare_dao = ProductPrepareDao()

        data  = product_prepare_dao.get_product_prepare(connection, filter)
        count = product_prepare_dao.get_product_prepare_count(connection, filter)

        return {"data" : data, "count" : count["count"]}

    def patch_product_prepare(self, connection, order_products):
        """주문상태 변경, 이력관리 service
        Author:
            서득영
        Args:
            connection     : pymysql 객체
            order_products : 주문상태 변경할 주문건의 주문상세번호 리스트

        Raises:

        Returns:
            {
                "success" : 요청 처리 성공한 주문상세번호 리스트, 
                "failure" : 요청 처리 실패한 주문상세번호 리스트
                }   
            """

        product_prepare_dao = ProductPrepareDao()
        select_now_dao      = UtilDao()
        
        # DB의 현재 시간을 불러온다.
        now = select_now_dao.select_now(connection)

        success = []
        failure = []

        for order_product in order_products:
            order_product["now"]      = now
            order_product["end_date"] = END_DATE

            try:
                # 종료할 이력의 pk값을 가져온다.
                primary_key = product_prepare_dao.select_log_primary_key(connection, order_product)
                
                # pk 값이 없을 경우 에러 처리.
                if primary_key is None:
                    raise ProcessingFailureError(InvalidRequest, 400)
                
                # 가져온 pk값을 order_product 리스트에 추가한다.
                order_product["order_product_history_id"] = primary_key["id"]
                
                # 기존 이력을 종료한다.
                if product_prepare_dao.patch_order_log_end(connection, order_product) == 0:
                    raise ProcessingFailureError(INVALID_REQUEST, 400)
                
                # 새로운 이력을 생성한다.
                if product_prepare_dao.patch_order_log_start(connection, order_product) == 0:
                    raise ProcessingFailureError(INVALID_REQUEST, 400)
                
                # 배송정보 테이블의 배송 상태를 수정한다.
                if product_prepare_dao.patch_shipments_info(connection, order_product) == 0:
                    raise ProcessingFailureError(INVALID_REQUEST, 400)
                
                success.append({"order_product_id" : order_product["order_product_id"]})
                connection.commit()

            except Exception as e:
                failure.append({"order_product_id" : order_product["order_product_id"]})
                connection.rollback()

        return {"success" : success, "failure" : failure}

    def excel_download(self, connection, filter):
        """엑셀 파일에 입력될 데이터를 가져오고, 컬럼제목 리스트를 만드는 service
        Author:
            서득영
        Args:
            connection : pymysql 객체
            filter     : 데이터 검색 조건

        Raises:

        Returns:
            엑셀 파일 만든 후 전송
            """

        get_data_dao = ProductPrepareDao()
        excel_download_service = UtilService()

        try:
            data = get_data_dao.get_product_prepare(connection, filter)

            titles = [
                "결제일자", 
                "주문번호", 
                "주문상세번호", 
                "셀러명", 
                "상품명", 
                "옵션정보", 
                "옵션추가금액",
                "수량", 
                "주문자명", 
                "핸드폰번호", 
                "결제금액", 
                "주문상태"
                ]

            result = excel_download_service.excel_download(titles, data)

            return result

        except Exception as e:
            raise e