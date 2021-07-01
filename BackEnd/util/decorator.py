import jwt

from functools        import wraps
from flask            import request, g

from model            import AccountDao
from util.exception   import InvalidAccessError, LoginRequiredError
from util.message     import UNAUTHORIZED_TOKEN, LOGIN_REQUIRED
from util.const       import MASTER_ACCOUNT_TYPE, SELLER_ACCOUNT_TYPE
from config           import SECRET_KEY, ALGORITHM
from connection       import connect_db

def login_required(func):
    """로그인 데코레이터
     토큰을 검사하여 접근 권한이 있는지 확인하여 유효한 접근이면
    account_id와 account_type_id를 전역 객체에 담는다.

    Author:
        김현영

    Args:
        func (function): 데코레이터가 필요한 함수 객체

    Raises:
        InvalidAccessError: 삭제된 셀러 계정일 때
        InvalidAccessError: 삭제된 마스터 계정일 때
        InvalidAccessError: 잘못된 토큰이 들어왔을 때
        LoginRequiredError: 요청 헤더에 토큰이 없을 때

    Returns:
        function : 인증 과정을 거친 함수 객체의 결과값
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is None:
            raise LoginRequiredError(LOGIN_REQUIRED, 401) 

        connection = None
        try:
            payload = jwt.decode(access_token, SECRET_KEY['secret'], ALGORITHM)

            data         = {'account_id' : payload['Id']}
            account_dao  = AccountDao()
            connection   = connect_db()
            
            if payload['account_type'] == SELLER_ACCOUNT_TYPE:
                seller_check = account_dao.check_seller(data, connection)
                is_deleted   = seller_check['is_deleted']
                
                if is_deleted:
                    raise InvalidAccessError(UNAUTHORIZED_TOKEN, 401)

            if payload['account_type'] == MASTER_ACCOUNT_TYPE:
                is_deleted = account_dao.check_master(data, connection)['is_deleted']
                if is_deleted:
                    raise InvalidAccessError(UNAUTHORIZED_TOKEN, 401)

            g.account_info = {'account_id'   : payload['Id'], 
                                'account_type' : payload['account_type']}
            
        except jwt.InvalidTokenError:
            raise InvalidAccessError(UNAUTHORIZED_TOKEN, 401)
        
        finally:
            if connection is not None:
                connection.close()
               
        return func(*args, **kwargs)
    return wrapper