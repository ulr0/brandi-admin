from flask_request_validator import Pattern

nickname_rule            = Pattern(r'^[a-zA-Z0-9_-]{5,20}$') # 영문,숫자 조합 5~20 글자. 대쉬, 하이픈 허용
password_rule            = Pattern(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,20}$') # 영문,숫자, 특수문자 조합 8~20글자
phone_number_rule        = Pattern(r'^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$')
seller_korean_name_rule  = Pattern(r'^[가-힣\s]+$')
seller_english_name_rule = Pattern(r'^[a-zA-Z\s]+$')
