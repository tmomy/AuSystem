#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/9/6 17:32
"""
import time, string, random
from jot import jwt, jws
from app.conf.config import web
from app.framework_api import redis_service

def generate_token(username):
    iat = time.time()
    exp = iat + web['session_timeout']
    payload = {
        'username': username,
        'iat': iat,
        'exp': exp
    }
    key_pix = token_key()
    token = jwt.encode(payload,signer=jws.HmacSha(bits=256, key=web['token_key']+key_pix))
    redis_service.set(token, key_pix)
    return token


def token_key():
    """
    生成秘钥字符串
    :return: 
    """
    base_str = string.digits + string.letters
    key_list = [random.choice(base_str) for i in range(web['key_len'])]
    key_str = "".join(key_list)
    return key_str
