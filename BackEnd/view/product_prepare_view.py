from datetime import datetime, timedelta
from ast      import literal_eval

from flask                             import jsonify, request, g
from flask.views                       import MethodView

from connection     import connect_db
from service        import ProductPrepareService
from util.exception import InvalidRequest, OffsetOutOfRangeError, LimitOutOfRangeError, ParamRequiredError
from util.message   import *
from util.decorator import login_required
from util.const     import SELLER_ACCOUNT_TYPE

class ProductPrepareView(MethodView):
    @login_required
    def get(self):
        """상품준비 리스트 조회 api
        필터 검색 조건을 쿼리 파라미터로 받아서 조건에 맞는
        상품준비 상태인 주문 목록을 반환한다.

        Author:
            서득영

        Args:
            filter: { 
                "order_id"         : 주문번호,
                "order_product_id" : 주문상세번호,
                "order_name"       : 주문자명,
                "order_phone"      : 주문자 휴대폰번호,
                "start_date"       : 검색시작일,
                "end_date"         : 검색종료일,
                "seller_name"      : 셀러명,
                "product_name"     : 상품명,
                "seller_attribute" : 셀러 속성,
                "order_by"         : 정렬(최신순 = 1, 역순 = 0),
                "offset"           : offset,
                "limit"            : limit
            }

        Raises:
            ParamRequiredError    : 필수 필터 조건이 없을 때
            OffsetOutOfRangeError : offset 값이 0보다 작을 때
            LimitOutOfRangeError  : limit 값이 1보다 작을 때

        Returns:
            200: {
                "count": 상품준비 리스트 총 개수
                "data": [
                    {
                        "created_at"       : 결제 일시,
                        "extra_price"      : 옵션 추가 금액,
                        "order_name"       : 주문자 이름,
                        "order_id"         : 주문번호,
                        "order_product_id" : 주문상세번호,
                        "phone_number"     : 주문자 휴대폰 번호,
                        "price"            : 상품 가격,
                        "product_name"     : 상품명,
                        "quantity"         : 수량,
                        "seller_name"      : 셀러명,
                        "order_status"     : 주문 상태
                        "order_status_id   : 주문 상태 id
                    }
                ]
            }
        """

        product_prepare_service = ProductPrepareService()

        connection = None

        try:
            filter = {
                "order_id"         : request.args.get("order_id", ""),
                "order_product_id" : request.args.get("order_product_id", ""),
                "order_name"       : request.args.get("order_name", ""),
                "order_phone"      : request.args.get("order_phone", ""),
                "start_date"       : request.args.get("start_date", ""),
                "end_date"         : request.args.get("end_date", ""),
                "seller_name"      : request.args.get("seller_name", ""),
                "product_name"     : request.args.get("product_name", ""),
                "seller_attribute" : request.args.get("seller_attribute", ""),
                "order_by"         : int(request.args.get("order_by", 1)),
                "offset"           : int(request.args.get("offset", 0)),
                "limit"            : int(request.args.get("limit", 50)),
            }

            if filter["order_id"] == "" and\
                filter["order_product_id"] == "" and\
                filter["order_name"] == "" and \
                filter["order_phone"] == "" and\
                filter["start_date"] == "" and\
                filter["end_date"] == "":
                raise ParamRequiredError(PARAM_REQUIRED, 400)

            if filter["offset"] < 0:
                raise OffsetOutOfRangeError(OFFSET_OUT_OF_RANGE, 400)
            
            if filter["limit"] < 1:
                raise LimitOutOfRangeError(LIMIT_OUT_OF_RANGE, 400)

            # 셀러 속성 값을 int 또는 tuple 형태로 변환
            if filter["seller_attribute"] != "":
                filter["seller_attribute"] = literal_eval(filter["seller_attribute"])
            
            # 검색 종료일은 날짜만 들어와서 00시를 기준으로 비교하기 때문에
            # 하루를 더해서 마지막 날짜로 들어온 값도 포함되도록 설정
            if filter["end_date"] != "":
                filter["end_date"] = datetime.strptime(filter["end_date"], '%Y-%m-%d') + timedelta(days=1)            
            
            if g.account_info["account_type"] == SELLER_ACCOUNT_TYPE:
                filter["account_id"] = g.account_info["account_id"]

            connection = connect_db()

            if request.path == '/order/product-prepare':
                result =  product_prepare_service.get_product_prepare(connection, filter)

            # 엑셀 다운로드일 경우 limit이나 offset은 사용하지 않기 때문에 삭제
            if request.path == '/order/product-prepare/download':
                if filter["order_product_id"]:
                    filter["order_product_id"] = literal_eval(filter["order_product_id"])
                
                del filter["offset"]
                del filter["limit"]
                
                result = product_prepare_service.excel_download(connection, filter)

            return result

        except Exception as e:
            if connection is not None:
                connection.rollback()
            raise e

        finally:
            if connection is not None:
                connection.close() 

    @login_required
    def patch(self):
        """상품준비 상태인 주문을 배송중으로 변경하는 api
        배송중으로 변경할 주문의 주문상세번호를 request.body로 받아서
        해당 주문을 상품준비 상태에서 배송중으로 변경한다.

        Author:
            서득영

        Args:
            {
                order_products: {
                    [
                        "order_product_id : 주문상세번호
                        ]
                    }
                }

        Raises:
            InvalidRequest : body에 order_products가 없을 때
            InvalidRequest : body에 order_product_id가 없을 때

        Returns:
            200: {
                "failure": [
                    {
                        "order_product_id": 요청 처리에 실패한 상품상세번호
                        }
                    ],
                "success": [
                    {
                        "order_product_id": 요청 처리에 성공한 상품상세번호
                        }
                    ]
                }
        """
        product_prepare_service = ProductPrepareService()
        
        connection = None

        try:
            data = request.json

            if "order_products" not in data:
                raise InvalidRequest(ORDER_PRODUCTS_NEEDED, 400)

            order_products = data["order_products"]

            for order_product in order_products:
                if "order_product_id" not in order_product:
                    raise InvalidRequest(ORDER_PRODUCT_ID_NEEDED, 400)
                if g.account_info["account_type"] == SELLER_ACCOUNT_TYPE:
                    order_product["account_id"] = g.account_info["account_id"]

            connection = connect_db()

            result = product_prepare_service.patch_product_prepare(connection, order_products)
            
            return jsonify(result), 200

        except Exception as e:
                raise e

        finally:
            if connection is not None:
                connection.close()