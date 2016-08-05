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

from alanber.webapp.views import USER_WXCORP_MAP
from alanber.weixin.corp.api import CorpApi

bp = Blueprint('weixin', __name__)


@bp.route('/corp_callback')
def corp_callback():
    code = request.args.get('code')
    state = request.args.get('state')

    api = CorpApi()
    user, is_follow = api.get_userinfo(code)
    if is_follow and user.has_key('extattr'):
        extattrs = user['extattr']
        for attr in extattrs:
            if attr['name'] == USER_WXCORP_MAP.get('cn_birthday'):
                user['cn_birthday'] = attr['value']
        for attr in extattrs:
            if attr['name'] == USER_WXCORP_MAP.get('gr_birthday'):
                user['gr_birthday'] = attr['value']

    response = make_response(redirect(url_for(state)))
    response.set_cookie('user', base64.b64encode(json.dumps(user)))
    response.set_cookie('is_follow', str(is_follow))
    return response
