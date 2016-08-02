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
from flask import Blueprint, render_template, request
from alanber.weixin.corp.oauth import authorize


bp = Blueprint('duckheader', __name__)


@bp.route('/welcome', endpoint='welcome')
@authorize
def welcome():
    user = request.cookies.get('user')
    is_follow = request.cookies.get('is_follow')
    return render_template('welcome.html', user=user, is_follow=is_follow)