#!/usr/bin/env python
# encoding: utf-8
"""
@author: WL
@time: 2017/6/30 17:39
"""

import uuid
from app.conf.config import R_SMS
from framework.utils import logging
import top


def send_sms_dy(phone_number,template_param):
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo("23582797", "4000cdab7cb17eddcc2d50ced114ae60"))
    req.extend = uuid.uuid1()
    req.sms_type = "normal"
    req.sms_free_sign_name = "点餐么"
    req.sms_param = template_param
    req.rec_num = phone_number
    req.sms_template_code = "SMS_36390243"
    try:
        resp = req.getResponse()
        logging.info('fun_out: [sms_response: %2s]', resp)
        if resp['alibaba_aliqin_fc_sms_num_send_response']['result']['err_code']=="0":
            return True
    except Exception, e:
        logging.info('fun_out: [sms_response: %2s]', e)
# if __name__ == '__main__':
#
#     __business_id = uuid.uuid1()
#     print __business_id
#     params = "{\"num\":\"12345\"}"
#     print send_sms_dy(__business_id, "13247780947", params)


