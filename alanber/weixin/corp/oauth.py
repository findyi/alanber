# coding:utf8

"""
Copyright 2016 Smallpay Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import urllib
from flask import request, redirect
from alanber.weixin.corp import CORPID


def authorize(func):

    def decorator(*args, **kwargs):
        userid = request.args.get('userid')
        openid = request.args.get('openid')
        if userid or openid:
            return func(*args, **kwargs)
        else:
            authorize_uri_base = "https://open.weixin.qq.com/connect/oauth2/authorize"
            authorize_uri_params = {
                'appid': CORPID,
                'redirect_uri': 'http://weixin.duckheader.com/corp/callback',
                'response_type': 'code',
                'scope': 'snsapi_base',
                'state': 'duckheader'
            }
            authorize_uri = "%s?%s#wechat_redirect" % (authorize_uri_base, urllib.urlencode(authorize_uri_params))
            return redirect(authorize_uri)
    return decorator


