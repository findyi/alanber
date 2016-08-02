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
from flask import Blueprint, request, redirect, url_for
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
    userinfo = api.get_userinfo(code)
    endpoint = REDIRECT_STATE_ENDPOINT_DICT.get(state)
    return redirect(url_for(endpoint))