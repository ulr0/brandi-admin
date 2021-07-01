import jwt
import bcrypt

from model            import AccountDao
from util.exception   import AlreadyExistError, InvalidUserError
from util.message     import ACCESS_DENIED, ALREADY_EXISTS, INVALID_USER, UNPERMITTED_USER
from util.const       import STAND_BY, MASTER_ACCOUNT_TYPE, SELLER_ACCOUNT_TYPE, USER_ACCOUNT_TYPE
from config           import SECRET_KEY, ALGORITHM


class AccountService:
    """
    어드민 계정 가입과 로그인과 관련된 서비스 클래스
    """
    def create_account(self, data, connection):    
        
        account_dao = AccountDao()
        is_existed  = account_dao.is_existed_account(data, connection)
        
        if is_existed:
            raise AlreadyExistError(ALREADY_EXISTS, 409)

        account_id         = account_dao.join(data,connection)
    
        data['Id']         = account_id
        data['account_id'] = account_id
        account_type       = data['account_type_id']
            
        hashed_password  = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        data['password'] = hashed_password

        if account_type == SELLER_ACCOUNT_TYPE:
            account_dao.seller_join_info(data, connection)
            data['seller_id']        = account_id
            data['action_status_id'] = STAND_BY
            return account_dao.seller_join_history(data, connection)
        
        if account_type == MASTER_ACCOUNT_TYPE:
            account_dao.master_join_info(data, connection) 
            data['master_id'] = account_id
            return account_dao.master_join_history(data, connection)

    def login(self, data, connection):
        """어드민 로그인 서비스 로직

        어드민이 로그인했을때 계정 타입을 확인하고 마스터 또는 셀러이면
        account_id 와 account_type을 토큰화하여 토큰을 발급한다.

        Author:
            김현영

        Args:
            data (dict): 사용자가 입력한 nickname, password 값을 가지는 dictionary
            connection (객체): pymysql 객체

        Raises:
            InvalidUserError: 해당 nickname를 가진 계정이 없을때
            InvalidUserError: 해당 seller 계정이 삭제된 계정일 때
            InvalidUserError: 해당 master 계정이 삭제된 계정일 때
            InvalidUserError: 해당 계정의 계정 타입이 일반 유저일 때
            InvalidUserError: 패스워드가 일치하지 않을 때

        Returns:
            {
                "access_token" : "token"
            }
        """
        account_dao = AccountDao()
        
        account_info    = account_dao.get_account_id(data, connection)
        
        if account_info is None:
            raise InvalidUserError(INVALID_USER, 401)

        data['account_id'] = account_info['Id']
        account_type       = account_info['account_type_id']
        
        if account_type == SELLER_ACCOUNT_TYPE:
            result        = account_dao.check_seller(data, connection)
            is_deleted    = result['is_deleted']
            action_status = result['action_status_id']
            if is_deleted:
                raise InvalidUserError(INVALID_USER, 401)
            if action_status == STAND_BY:
                raise InvalidUserError(UNPERMITTED_USER, 401)
            password = result['password']
        
        if account_type == MASTER_ACCOUNT_TYPE:
            result = account_dao.check_master(data, connection)
            is_deleted = result['is_deleted']
            if is_deleted:
                raise InvalidUserError(INVALID_USER, 401)
            password = result['password']
        
        if account_type == USER_ACCOUNT_TYPE:
            raise InvalidUserError(ACCESS_DENIED, 401)
        
        if not bcrypt.checkpw(data['password'].encode('utf-8'), password.encode('utf-8')):
            raise InvalidUserError(INVALID_USER, 401)
        
        access_token = jwt.encode(
            {'Id'           : data['account_id'], 
             'account_type' : account_type},
              SECRET_KEY['secret'],
              ALGORITHM
        )
        
        return access_token      