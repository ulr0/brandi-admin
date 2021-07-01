from ast import literal_eval

from flask import jsonify, request, g
from flask.views import MethodView
from flask_request_validator import (
    GET,
    Param,
    validate_params,
    Datetime,
    CompositeRule,
    Max,
    Min,
    FORM,
    ValidRequest
)

from service import ProductService, ImageService

from util.decorator import login_required
from util.const import MASTER_ACCOUNT_TYPE, SELLER_ACCOUNT_TYPE
from util.message import UNAUTHORIZED, NOT_EXIST_PRODUCT_ID, INVALID_PRODUCT_ID
from util.exception import UnauthorizedError, InvalidParamError

from connection import connect_db, connect_s3


class ProductView(MethodView):
    @login_required
    @validate_params(
        Param("start_date", GET, str, required=False, rules=[Datetime("%Y-%m-%d")]),
        Param("end_date", GET, str, required=False, rules=[Datetime("%Y-%m-%d")]),
        Param("seller_name", GET, str, required=False),
        Param("product_name", GET, str, required=False),
        Param("product_number", GET, int, required=False),
        Param("is_sold", GET, bool, required=False),
        Param("is_displayed", GET, bool, required=False),
        Param("is_sale", GET, bool, required=False),
        Param("seller_category", GET, list, required=False),
        Param("offset", GET, int, required=False),
        Param("limit", GET, int, required=False, rules=CompositeRule(Min(1), Max(100))),
    )
    def get(self, valid: ValidRequest):
        """어드민 상품 관리 리스트

        Author:
            이서진

        Returns:
            - 200:
                "data": {
                    "count": 상품 리스트 총 개수
                    "products": [
                        {
                            "created_at": 상품 등록 시간,
                            "discount_start_time": 상품 할인 시작 시간,
                            "discount_end_time": 상품 할인 끝 시간,
                            "discount_rate": 상품 할인율,
                            "image_url": 상품 대표 이미지 주소,
                            "is_displayed": 진열 여부,
                            "is_sold": 판매 여부,
                            "name": 상품 이름,
                            "price": 가격,
                            "product_code": 상품 코드,
                            "product_number": 상품 번호,
                            "seller_category": 셀러 속성
                        }
                    ]
                }
            - 400: validate param 오류
        """

        filters = valid.get_params()
        filters["account_id"] = g.account_info.get("account_id")
        filters["account_type"] = g.account_info.get("account_type")

        if filters["account_type"] not in [MASTER_ACCOUNT_TYPE, SELLER_ACCOUNT_TYPE]:
            raise UnauthorizedError(UNAUTHORIZED, 401)

        product_service = ProductService()
        connection = None

        try:
            connection = connect_db()
            result = product_service.get_product_list(connection, filters)
            return jsonify({"data": result})

        except Exception as e:
            raise e

        finally:
            if connection is not None:
                connection.close()

    @login_required
    def patch(*args):
        data = request.json

        for row in data:
            # product_id가 없을 때
            if row.get("product_id") is None:
                raise InvalidParamError(NOT_EXIST_PRODUCT_ID, 400)

            # product_id가 숫자가 아닐 때
            if type(row.get("product_id")) is not int:
                raise InvalidParamError(INVALID_PRODUCT_ID, 400)

        product_service = ProductService()
        connection = None

        try:
            connection = connect_db()
            result = product_service.update_product_list(connection, data)
            return jsonify({"data": result})

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            if connection is not None:
                connection.close()

    @login_required
    @validate_params(
        Param("seller_id", FORM, int, required=False),
        Param("is_sold", FORM, bool, required=True),
        Param("is_displayed", FORM, bool, required=True),
        Param("product_subcategory_id", FORM, int, required=True),
        Param("manufacturer", FORM, str, required=False),
        Param("manufactured_date", FORM, str, required=False, rules=[Datetime("%Y-%m-%d")]),
        Param("origin_id", FORM, int, required=False),
        Param("name", FORM, str, required=True),
        Param("comment", FORM, str, required=False),
        Param("detail_page_html", FORM, str, required=True),
        Param("options", FORM, str, required=True),
        Param("price", FORM, int, required=True),
        Param("discount_rate", FORM, int, required=True, rules=CompositeRule(Min(1), Max(100))),
        Param("discount_start_time", FORM, str, required=True, rules=[Datetime("%Y-%m-%d %H:%M")]),
        Param("discount_end_time", FORM, str, required=True, rules=[Datetime("%Y-%m-%d %H:%M")]),
        Param("minimum_sell_quantity", FORM, int, required=True, rules=CompositeRule(Min(1), Max(20))),
        Param("maximum_sell_quantity", FORM, int, required=True, rules=CompositeRule(Min(1), Max(20)))
    )
    def post(self, valid: ValidRequest):
        data = valid.get_form()
        data["account_id"] = g.account_info.get("account_id")
        data["account_type"] = g.account_info.get("account_type")

        # json 형태로 오는 options 따로 변수 선언 후 제거
        options = literal_eval(data["options"])
        del data["options"]

        main_image_file = request.files.get("main_image_file")
        image_files = request.files.getlist("image_files")

        if data["account_type"] not in [MASTER_ACCOUNT_TYPE, SELLER_ACCOUNT_TYPE]:
            raise UnauthorizedError(UNAUTHORIZED, 401)

        product_service = ProductService()
        image_service = ImageService()
        connection = None
        s3_connection = None
        image_urls = []

        try:
            connection = connect_db()
            s3_connection = connect_s3()

            # 상품 등록
            data = product_service.insert_new_product(connection, data, options)

            # 메인 이미지 S3 등록
            image_urls.append(image_service.image_upload(s3_connection, main_image_file))

            # 다른 이미지 S3 등록
            for image_file in image_files:
                image_urls.append(image_service.image_upload(s3_connection, image_file))

            product_service.insert_new_product_images(connection, data, image_urls)

            connection.commit()
            return jsonify({"message": "success"})

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            if connection is not None:
                connection.close()



