from flask                   import jsonify
from flask.views             import MethodView
from flask_request_validator import *
                                    
from service                 import AccountService
from connection              import connect_db
from util.validation         import (
    nickname_rule, password_rule, phone_number_rule,
    seller_korean_name_rule, seller_english_name_rule
    )
from util.message            import ACCOUNT_CREATED, LOGIN_SUCCESS
from util.const              import MASTER_ACCOUNT_TYPE, SELLER_ACCOUNT_TYPE


class SellerAccountView(MethodView):
    @validate_params(
        Param('nickname', JSON, str, required=True, rules=[nickname_rule]),
        Param('password', JSON, str, required=True, rules=[password_rule]),
        Param('seller_subcategory_id', JSON, int, required=True),
        Param('seller_phone_number', JSON, str, required=True, rules=[phone_number_rule]),
        Param('korean_name', JSON, str, required=True, rules=[seller_korean_name_rule]),
        Param('english_name', JSON, str, required=True, rules=[seller_english_name_rule]),
        Param('cs_phone_number', JSON, str, required=True, rules=[phone_number_rule]),
        Param('cs_nickname', JSON, str, required=True, rules=[nickname_rule])
    )
    def post(self, valid: ValidRequest):
        account_service = AccountService()

        connection = None
        try:
            data = valid.get_json()
            data['account_type_id'] = SELLER_ACCOUNT_TYPE
            
            connection = connect_db()
            result     = account_service.create_account(data, connection)
            connection.commit()
            
            return jsonify({"message" : ACCOUNT_CREATED, "data" : result}), 201
        
        except Exception as e:
            connection.rollback()
            raise e 
            
        finally:
            if connection is not None:
                connection.close()    

class MasterAccountView(MethodView):
    @validate_params(
        Param('nickname', JSON, str, required=True, rules=[nickname_rule]),
        Param('password', JSON, str, required=True, rules=[password_rule])
    )
    def post(self, valid: ValidRequest):
        account_service = AccountService()

        connection = None
        try:
            data = valid.get_json()
            data['account_type_id'] = MASTER_ACCOUNT_TYPE

            connection = connect_db()
            result     = account_service.create_account(data, connection)
            connection.commit()
            
            return jsonify({"message" : ACCOUNT_CREATED, "data" : result}), 201
        
        except Exception as e:
            connection.rollback()
            raise e 
            
        finally:
            if connection is not None:
                connection.close()    


class LoginView(MethodView):
    @validate_params(
        Param('nickname', JSON, str, required=True, rules=[nickname_rule]),
        Param('password', JSON, str, required=True, rules=[password_rule])
    )
    def post(self, valid: ValidRequest):
        account_service = AccountService()

        connection = None
        try:
            data = valid.get_json()

            connection = connect_db()
            result     = account_service.login(data, connection)
            connection.commit()

            return jsonify({"message" : LOGIN_SUCCESS, "data" : result}), 201
        
        except Exception as e:
            connection.rollback()
            raise e
        
        finally:
            if connection is not None:
                connection.close()