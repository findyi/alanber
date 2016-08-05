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
import json
from alanber.weixin import WeixinApi, AccessToken, ApiError
from alanber.weixin.corp import CORPID, SECRET


class CorpApi(WeixinApi):

    GET_ACCESS_TOKEN_URL = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"

    def get_access_token(self):
        params = dict(corpid=CORPID, corpsecret=SECRET)
        resp = self._request('GET', self.GET_ACCESS_TOKEN_URL, params=params)
        return AccessToken.parse(resp.json())

    def access_token_expired(self, r):
        return r.status_code == 200 and r.json().get('errcode') in (40001, 42001)

    def response_ok(self, r):
        return r.status_code == 200 and not r.json().get('errcode')

    def create_user(self, userid, name, departments, position=None, mobile=None,
                    gender=None, email=None, weixinid=None, avatar_mediaid=None, extattrs=None):
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/create"
        req_body = dict(
            userid=userid,
            name=name,
            department=departments,
            position=position,
            mobile=mobile,
            gender=gender,
            email=email,
            weixinid=weixinid,
            avatar_mediaid=avatar_mediaid,
        )
        if isinstance(extattrs, list):
            req_body['extattr'] = {
                'attrs': extattrs
            }
        return self.api_post(url, body=json.dumps(req_body))

    def update_user(self, userid, name=None, departments=None, position=None, mobile=None,
                    gender=None, email=None, weixinid=None, avatar_mediaid=None, extattrs=None):
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/update"
        req_body = dict(
            userid=userid,
            name=name,
            department=departments,
            position=position,
            mobile=mobile,
            gender=gender,
            email=email,
            weixinid=weixinid,
            avatar_mediaid=avatar_mediaid,
        )
        if isinstance(extattrs, list):
            req_body['extattr'] = {
                'attrs': extattrs
            }
        return self.api_post(url, body=json.dumps(req_body))

    def get_user(self, userid):
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/get?userid=%s" % userid
        return self.api_get(url)

    def _get_userinfo(self, code):
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?code=%s" % code
        data = self.api_get(url)
        userinfo = dict(userid=data.get('UserId'),
                        openid=data.get('OpenId'),
                        deviceid=data.get('DeviceId'))
        return userinfo

    def get_userinfo(self, code):
        userinfo = self._get_userinfo(code)
        userid = userinfo.get('userid')
        openid = userinfo.get('openid')
        is_follow = False
        if userid:
            is_follow = True
            return self.get_user(userid), is_follow
        elif openid:
            return self.get_mp_user(openid), is_follow
        else:
            raise ApiError("未能取到用户的userid或者openid")

    def get_mp_user(self, openid):
        url = "https://api.weixin.qq.com/cgi-bin/user/info?openid=%s" % openid
        return self.api_get(url)
