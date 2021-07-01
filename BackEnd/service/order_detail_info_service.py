from model      import OrderDetailInfoDao
from util.const import END_DATE

class OrderDetailInfoService:
    def get_order_detail_info(self, connection, data):
        """주문상세정보 가져오는 service
        Author:
            서득영
        Args:
            connection : pymysql 객체
            data       : 주문상세번호

        Raises:

        Returns:
            {
                "order_detail" : 주문상세정보, 
                "order_log"    : 주문상태 이력 정보
                }   
            """

        order_detail_info = OrderDetailInfoDao()

        data["end_date"] = END_DATE
        
        #주문 정보를 가져온다.
        order_detail = order_detail_info.get_order_detail_info(connection, data)
        
        #이력 정보를 가져온다.
        order_log = order_detail_info.get_order_log(connection, data)

        result = {"order_detail" : order_detail, "order_log" : order_log}
        
        return result