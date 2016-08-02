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
import base64
from flask import Blueprint, request, redirect, url_for, make_response
from alanber.weixin.corp.api import CorpApi

bp = Blueprint('weixin_corp', __name__)


REDIRECT_STATE_ENDPOINT_DICT = {
    'duckheader': 'duckheader.welcome'
}


@bp.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if state not in REDIRECT_STATE_ENDPOINT_DICT:
        return '未知的请求'

    api = CorpApi()
    user, is_follow = api.get_userinfo(code)

    endpoint = REDIRECT_STATE_ENDPOINT_DICT.get(state)
    response = make_response(redirect(url_for(endpoint)))
    response.set_cookie('user', base64.b64encode(json.dumps(user)))
    response.set_cookie('is_follow', str(is_follow))
    return response