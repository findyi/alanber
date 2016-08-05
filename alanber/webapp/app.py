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
from flask import Flask
from alanber.webapp.views import user, weixin


def jinja_filter_gender_translate(gender):
    gender = str(gender)
    gender_translate_map = {
        '1': '男',
        '2': '女',
    }
    if gender_translate_map.has_key(gender):
        return gender_translate_map.get(gender)
    else:
        return '未知'


def register_jinja_filter(app):
    env = app.jinja_env
    env['gender_translate'] = jinja_filter_gender_translate


def create_app():
    application = Flask(__name__)
    application.config.from_object('alanber.webapp.config')

    application.register_blueprint(user.bp, url_prefix='/user')
    application.register_blueprint(weixin.bp, url_prefix='/weixin')

    register_jinja_filter(application)

    return application
