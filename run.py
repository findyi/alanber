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
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop
import alanber.webapp.app

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    app = alanber.webapp.app.create_app()
    app.run('0.0.0.0', 8000, debug=True)


def tornado_main():
    wsgi_applicaton = alanber.webapp.app.create_app()
    wsgi_container = tornado.wsgi.WSGIContainer(wsgi_applicaton)
    http_server = tornado.httpserver.HTTPServer(wsgi_container)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
