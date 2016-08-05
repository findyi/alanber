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
    userinfo = api.get_userinfo(code)

    response = make_response(redirect(url_for(state)))
    response.set_cookie('userinfo', base64.b64encode(json.dumps(userinfo)))
    return response
