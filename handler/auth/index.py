#!/usr/bin/env python
# -*- coding: utf-8 -*-
from handler.bases import CommonBaseHandler
from lib import route

@route(r'/')
class IndexHandler(CommonBaseHandler):

	'''配置管理系统页面入口
	'''

	def response(self):
		return self.render('index.html')


@route(r'/auth/index/main', '首页')
class IndexMainHandler(CommonBaseHandler):

	'''首页
	'''

	def response(self):
		self.finish()
