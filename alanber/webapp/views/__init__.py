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
USER_WXCORP_MAP = {
    'cn_birthday': '农历生日',
    'gr_birthday': '公历生日',
    '农历生日': 'cn_birthday',
    '公历生日': 'gr_birthday',
}


class UserCache(object):

    _cache = dict()

    @classmethod
    def put(cls, user):
        cls._cache[user.get("userid")] = user

    @classmethod
    def get(cls, userid):
        return cls._cache.get(userid)

    @classmethod
    def delete(cls, userid):
        del cls._cache[userid]