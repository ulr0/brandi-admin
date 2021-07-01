from flask import request, jsonify
from flask.views import MethodView
from flask_request_validator import validate_params, Param, GET, CompositeRule, Min, Max

from connection import connect_db
from service.search_service import SearchService


class SearchSellerView(MethodView):
    @validate_params(
        Param("search_word", GET, str, required=True),
        Param("limit", GET, int, required=True, rules=CompositeRule(Min(1), Max(100))),
    )
    def get(*args):
        filters = dict(request.args)

        search_service = SearchService()
        connection = None

        try:
            connection = connect_db()
            result = search_service.get_seller_name_search_list(connection, filters)
            return jsonify({"data": result})

        except Exception as e:
            raise e

        finally:
            if connection is not None:
                connection.close()
