"""Constants used by Dao"""

# 이력 종료 시점
END_DATE = '9999-12-31 23:59:59'

# Seller Action Status
OPEN_STORE     = 1  # 입점
STAND_BY       = 2  # 입점대기
CLOSE_DOWN     = 3  # 퇴점
CLOSE_STAND_BY = 4  # 퇴점대기
BREAK          = 5  # 휴점
REJECTED       = 6  # 입점거절

# Master Action
DENY               = 1  # 입점거절
APPROVE            = 2  # 입점승인
SET_BREAK          = 3  # 휴점처리
REMOVE_BREAK       = 4  # 휴점해제
SET_CLOSE_STAND_BY = 5  # 퇴점대기처리
SET_CLOSE_DOWN     = 6  # 퇴점확정처리
REMOVE_CLOSE_DOWN  = 7  # 퇴점철회


# 유저 타입
MASTER_ACCOUNT_TYPE = 1
SELLER_ACCOUNT_TYPE = 2
USER_ACCOUNT_TYPE = 3

# shipments_status
SHIPMENT_STATUS_BEFORE_DELIVERY = 1 # 배송준비중
SHIPMENT_STATUS_SHIPPING = 2 # 배송중

# order_status 
ORDER_STATUS_ORDER_COMPLETED = 1 # 주문완료
ORDER_STATUS_PRODUCT_PREPARE = 2 # 상품준비
ORDER_STATUS_SHIPPING = 3 # 배송중


# shipments_status, order_status 배송 완료
DELIVERY_COMPLETED = 3