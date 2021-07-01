from flask                             import jsonify
from flask.views                       import MethodView
from flask_request_validator           import validate_params, Param, GET
from flask_request_validator.validator import ValidRequest

from service        import OrderDetailInfoService
from util.decorator import login_required
from connection     import connect_db

class OrderDetailInfoView(MethodView):
    @login_required
    @validate_params(
        Param("order_product_id", GET, int, required=True)
    )
    def get(self, valid: ValidRequest):
        """주문 상세 정보 조회 api
        주문상세번호를 쿼리 파라미터로 받아서
        해당 상품의 주문 상세 정보를 반환한다.

        Author:
            서득영

        Args:
            order_product_id : {
                주문상세번호
                    }
                    
        Raises:
            
        Returns:
            200: {
                "order_detail": 
                    {
                        "address"            : 주소,
                        "additional_address" : 상세 주소,
                        "zip_code"           : 우편번호,
                        "option_info"        : 옵션 정보,
                        "extra_price"        : 옵션 추가 금액
                        "shipment_message"   : 선택 배송요청사항,
                        "discount_rate"      : 할인율,
                        "sale_price"         : 할인된 상품 가격
                        "product_id"         : 상품 id,
                        "seller_name"        : 셀러명,
                        "message"            : 배송요청사항 직접입력,
                        "product_name"       : 상품명,
                        "order_created_at"   : 주문일시,
                        "order_id"           : 주문번호,
                        "order_name"         : 주문자명,
                        "order_phone"        : 주문자 휴대폰번호,
                        "order_product_id"   : 주문상세번호,
                        "order_status"       : 주문상태,
                        "order_status_id"    : 주문상태 id,
                        "paid_at"            : 결제일시,
                        "price"              : 상품 금액,
                        "quantity"           : 상품 수량,
                        "receive_name"       : 받는사람 이름,
                        "receive_phone"      : 받는사람 휴대폰번호,
                        "total_price"        : 총 주문금액,
                        "user_id"            : 주문자 id
                        },
                "order_log": [
                    {
                        "order_status" : 주문상태,
                        "start_time"   : 해당 주문상태 시작 일시,
                        "end_time"     : 해당 주문상태 종료 일시
                        }
                    ]
                }
        """
        order_detail_info = OrderDetailInfoService()

        connection = None
        try:
            data = valid.get_params()

            connection = connect_db()
            
            result = order_detail_info.get_order_detail_info(connection, data)
            
            return jsonify(result), 200

        except Exception as e:
            if connection is not None:
                connection.rollback()
            raise e
        
        finally:
            if connection is not None:
                connection.close()
