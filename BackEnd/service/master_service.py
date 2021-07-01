from pymysql import connect
from model import master_dao
from model import util_dao

from model.master_dao     import MasterDao
from model.util_dao       import UtilDao
from service.util_service import UtilService
from util.const           import *

class MasterService:
    def get_seller_list(self, connection, filter):
        """셀러 계정 정보를 조회.

        마스터가 셀러 계정 관리페이지에서 조회할 셀러 계정들의 정보를
        DB로부터 가져온다.

        Author:
            김현영

        Args:
            connection (객체): pymysql 객체
            filter (dict): {
                "seller_id"          : 셀러 번호,
                "seller_nickname"    : 셀러 아이디,
                "english_name"       : 셀러 상호 영문이름,
                "korean_name"        : 셀러 상호 한글이름,
                "seller_type"        : 셀러 구분,
                "clerk_name"         : 담당자 이름,
                "clerk_phone_number" : 담당자 연락처,
                "clerk_email"        : 담당자 이메일,
                "start_date"         : 조회 시작 일자,
                "end_date"           : 조회 종료 일자,
                "action_status_id"   : 셀러 상태 아이디,
                "action_status"      : 셀러 상태,
                "offset"             : 보여줄 데이터 시작,
                "limit"              : 보여줄 데이터 개수
            } 

        Raises:
            e: [description]

        Returns:
            dict : {
                    "count": 총 셀러 계정수,
                    "data": [
                        {
                        "Id": 셀러번호,
                        "action_status_id"   : 셀러 상태 아이디,
                        "actions": [
                            {
                            "action"         : 마스터 액션,
                            "action_id"      : 마스터 액션 아이디
                            }
                        ],
                        "clerk_email"        : 담당자 이메일,
                        "clerk_name"         : 담당자 이름,
                        "clerk_phone_number" : 담당자 연락처,
                        "created_at"         : 셀러 계정 생성날짜,
                        "english_name"       : 셀러상호 영문명,
                        "korean_name"        : 셀러상호 한글명,
                        "product_count"      : 보유 상품 개수,
                        "seller_attribute"   : 셀러 카테고리명,
                        "seller_id"          : 셀러 아이디,
                        "seller_type"        : 셀러 구분,
                        "status"             : 셀러 상태
                        }
                            ]
                    }

        """
        master_dao = MasterDao()    
        util_service = UtilService()
        try:
            sellers     = master_dao.get_seller_list(connection, filter)
            action_dict = util_service.get_action_dict(connection)

            result = []   
            for seller in sellers:
                seller["actions"] = action_dict[seller["action_status_id"]]
                result.append(seller)

            count = master_dao.get_seller_list_count(connection, filter)["count"]

            return result, count

        except Exception as e:
            raise e

    def to_xlsx(self, connection, filter):
        """셀러 계정 정보를 xlsx파일로 다운로드.

        마스터가 셀러계정관리 페이지에서 셀러 계정 정보를 xlsx파일로
        다운로드한다.

        Author:
            김현영

        Args:
            connection (객체): pymysql 객체
            filter (dict): {
                "seller_id"          : 셀러 번호,
                "seller_nickname"    : 셀러 아이디,
                "english_name"       : 셀러 상호 영문이름,
                "korean_name"        : 셀러 상호 한글이름,
                "seller_type"        : 셀러 구분,
                "clerk_name"         : 담당자 이름,
                "clerk_phone_number" : 담당자 연락처,
                "clerk_email"        : 담당자 이메일,
                "start_date"         : 조회 시작 일자,
                "end_date"           : 조회 종료 일자,
                "action_status"      : 셀러 상태,
                "offset"             : 보여줄 데이터 시작,
                "limit"              : 보여줄 데이터 개수
            }   

        Raises:
            e: [description]

        Returns:
            1
        """
        get_data_dao = MasterDao()
        to_xlsx_service = UtilService()

        try:
            data = get_data_dao.get_seller_list(connection, filter)

            titles = [
                "번호",
                "셀러아이디",
                "영문이름",
                "한글이름",
                "셀러구분",
                "담당자이름",
                "셀러상태",
                "담당자연락처",
                "담당자이메일",
                "셀러속성",
                "상품개수",
                "등록일시"
            ]

            result = to_xlsx_service.excel_download(titles, data)

            return result

        except Exception as e:
            raise e
    
    def change_seller_status(self, connection, data):
        """셀러의 상태를 변경.

        마스터가 셀러계정관리 페이지에서 셀러의 상태를 변경하여
        상태이력을 남긴다.

        Author:
            김현영

        Args:
            connection (객체): pymysql 객체
            data (dict): {
                "account_id"       : 이력을 수정한 계정 번호,
                "seller_id"        : 셀러 번호,
                "master_action_id" : 마스터가 실행한 action번호
            }   

        Raises:
            e: [description]

        Returns:
            int : 갱신된 row 개수
        """
        master_dao = MasterDao()
        util_dao   = UtilDao()

        try:
            master_action = data['master_action_id']

            data["seller_history_id"] = master_dao.get_seller_history_id(connection, data)['Id']

            now = util_dao.select_now(connection)
            master_dao.update_seller_history_end_time(connection, data, now)
            
            if master_action in [APPROVE, REMOVE_BREAK, REMOVE_CLOSE_DOWN]:
                data["action_status_id"] = OPEN_STORE
            
            if master_action == DENY:
                data["action_status_id"] = REJECTED
            
            if master_action == SET_BREAK:
                data["action_status_id"] = BREAK
                        
            if master_action == SET_CLOSE_STAND_BY:
                data["action_status_id"] = CLOSE_STAND_BY
            
            if master_action == SET_CLOSE_DOWN:
                data["action_status_id"] = CLOSE_DOWN

            return master_dao.change_action_status_and_insert(connection, data, now)

        except Exception as e:
            raise e
    