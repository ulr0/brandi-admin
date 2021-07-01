from flask import request, jsonify
from flask.views import MethodView
from flask_request_validator import validate_params, Param, PATH, GET

from connection import connect_db
from service import ProductService
from util.decorator import login_required


class ProductCategoryView(MethodView):
    @login_required
    @validate_params(
        Param("seller_category_id", PATH, int, required=False),
        Param("product_category_id", PATH, int, required=False),
    )
    def get(*args, seller_category_id, product_category_id=None):
        filters = dict(request.args)
        filters["seller_category_id"] = seller_category_id
        filters["product_category_id"] = product_category_id

        product_service = ProductService()
        connection = None

        try:
            connection = connect_db()
            result = product_service.get_product_category_list(connection, filters)
            return jsonify({"data": result})

        except Exception as e:
            raise e

        finally:
            if connection is not None:
                connection.close()