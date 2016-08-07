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
import requests
import requests.exceptions
from alanber.util import logger


class ApiError(Exception):
    pass


class AccessToken(object):

    def __init__(self, access_token, expires_in):
        self.access_token = access_token
        self.expires_in = expires_in

    @classmethod
    def parse(cls, token_dct):
        assert isinstance(token_dct, dict)
        return AccessToken(token_dct.get('access_token'), token_dct.get('expires_in'))


class WeixinApi(object):

    _access_token = None

    def get_access_token(self):
        raise NotImplementedError

    def access_token_expired(self, r):
        raise NotImplementedError

    def response_ok(self, r):
        raise NotImplementedError

    def _request(self, method, url, **kwargs):
        logger.debug("请求URL: %s" % url)
        if kwargs.has_key('json'):
            logger.debug("请求JSON:%s" % kwargs.get('json'))
        r = requests.request(method, url, **kwargs)
        logger.debug("返回响应: %s" % r.text)
        return r

    def _do_api_request(self, method, url, **kwargs):
        if '?' in url:
            url += '&access_token=%s' % self._access_token
        else:
            url += '?access_token=%s' % self._access_token
        return self._request(method, url, **kwargs)

    def api_request(self, method, url, **kwargs):
        if self._access_token is None:
            self._access_token = self.get_access_token().access_token

        r = self._do_api_request(method, url, **kwargs)
        if self.response_ok(r):
            return r.json()

        if self.access_token_expired(r):
            self._access_token = self.get_access_token().access_token
            r_again = self._do_api_request(method, url, **kwargs)
            if self.response_ok(r_again):
                return r_again.json()
            else:
                raise ApiError("调用微信接口错误:%s" % r.text)
        else:
            raise ApiError("调用微信接口错误:%s" % r.text)

    def api_get(self, url, **kwargs):
        return self.api_request('GET', url, **kwargs)

    def api_post(self, url, **kwargs):
        if kwargs.has_key('headers'):
            headers = kwargs['headers']
        else:
            headers = dict()

        headers['Content-Type'] = "application/json; charset=utf-8"
        kwargs['headers'] = headers
        return self.api_request('POST', url, **kwargs)
