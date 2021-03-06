# encoding: utf-8

"""
@version: 1.0
@author: dawning
@contact: dawning7670@gmail.com
@time: 2017/3/24 11:44
"""

"""
系统全局配置文件
"""
db_type = {
    "mongodb": "mongodb",
    "mysql": "mysql",
    "redis": "redis"
}

# web
web = {
    "url_pre": "/api/tiptop",
    "api_version": ["v1"],
    "ip": "0.0.0.0",
    "enable_rule": False,
    "enable_admin": True,
    "role": "admin",
    "opr": ["add","modify","delete","search"],
    "rule_redis_pix": "sys_rule_id_",
    "port": 1111,
    "session_timeout": 60 * 60 * 24 * 30,
    "push_time":60 * 30,
    "token_key": "zhong_lv_YLKJ",
    "log_pix":"E:\\Work\\dgg\\",
    "key_len":20,
    "pwd_err_code": 3,
    "pwd_err_freeze": 8,
    "account_freeze_time": 60*10,
    "debug": True,
    "frontend_port": 8899,
    "upload_path": "./app/static_file/uploads/",
    "pic_pix": "/static_file/",
    # 开关延期时间
    "switch_delay_time": 2
}

dbs = {
    "mongodb": {
        "type": db_type["mongodb"],
        "host": "10.10.51.30",
        "port": 27017,
        "pool_size": 5,  # 0表示不使用连接池 最小连接数
        "user_name": "",
        "password": "",
        "db_name": "greenDB_test"
    },
    "redis": {
        "type": db_type["redis"],
        "host": "10.10.51.30",
        "port": 6379,
        "pool_size": 5,  # 0表示不使用连接池 最大连接数
        "user_name": "",
        "password": "",
        "db_name": "tiptop"
    }
}

mysql_pool_configs = {
    "url": "mysql+pymysql://root:qwe1234567@10.10.51.30:3306/tip?charset=utf8",
    "pool_timeout": 5

}
# mysql_pool_configs = {
#     "url": "mysql+pymysql://tiptop:youlu_tip_666666@192.168.171.100:6603/tiptop_dev?charset=utf8",
#     "pool_timeout": 5
#
# }

mongo_pool_config = {
}
mysql_pool_config = {}

# connection_class
redis_pool_config = {
}

# 日志配置
log = {
    "name": "myapp",
    "level": "debug",
    "console": False,
    "format": "%(thread)d:%(asctime)s %(funcName)s:%(lineno)d %(filename)s - %(name)s %(levelname)s - %(message)s",
    "file": {
        "enable": True,
        "path": web["log_pix"] + "app\\logs\\myapp.log"
    },
    "syslog": {
        "enable": False,
        "ip": "10.10.0.100",
        "port": 514,
        "facility": "local2"
    }
}

sqltime_log_config = {
    "name": "sqltime",
    "level": "debug",
    "console": True,
    "format": "%(asctime)s %(funcName)s:%(lineno)d %(filename)s - %(name)s %(levelname)s - %(message)s",
    "file": {
        "enable": True,
        "path": web["log_pix"] + "app\\logs\\sql_time.log"
    },
    "syslog": {
        "enable": False,
        "ip": "10.10.0.100",
        "port": 514,
        "facility": "local2"
    }
}

pool_log_config = {
    "name": "sqlalchemy.pool",
    "level": "debug",
    "console": False,
    "format": "%(asctime)s %(funcName)s:%(lineno)d %(filename)s - %(name)s %(levelname)s - %(message)s",
    "file": {
        "enable": True,
        "path": web["log_pix"] + "app\\logs\\pool.log"
    },
    "syslog": {
        "enable": False,
        "ip": "10.10.0.100",
        "port": 514,
        "facility": "local2"
    }
}

# 邮件
email = {
    "smtp_addr": "smtp.qq.com",
    "from_email": "446330342@qq.com",
    "from_email_pwd": "vibwzctxgecpbhba",
    "subject": "邮箱验证"
}


# 注册短信验证码配置参数
R_SMS = {
    # 秘钥ID
    "ACCESS_KEY_ID": "LTAI5vSq44KwqrIl",
    "ACCESS_KEY_SECRET": "dxIxZutE2JqRg3hqWqkfnYx5y54Rci",
    "template_code": "SMS_75850036",
    "sign_name": "中绿平台",
    "template_string": "num",
    "redis_timeout": 60*60
}

# redis 各模块存储前缀
red_pre = {
    # 修改绑定手机号验证码
    "sms_lock_pix": "tel_pix_",
    # 用户激活码(code -> email)
    "code": "c_a_",
    # 用户对应的平台的ssid(email + platform + placeholder -> ssid )
    "acc_plat_ssid": "a_pp_s_",
    # 账户详细信息(ssid -> account)
    "ssid_acc": "s_a_",
    # 验证码（uuid -> captcha）
    "captcha": "u_cp_",
    # 用户密码输入错误次数统计（email -> counts）
    "acc_login_err": "e_c_"
}




