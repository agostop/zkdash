#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2014,掌阅科技
All rights reserved.

摘    要: init.py
创 建 者: WangLichao
创建日期: 2014-10-13
'''
import os,sys
# tornado
import tornado.httpserver
import tornado.ioloop
# lib
from lib import load
from lib import uimodule, uimethods
from lib.utils import logger
from lib.utils import pyshell
# conf
from conf import log
from conf.settings import (
	LOG_ITEMS,
	OPTIONS,
)


class Application(tornado.web.Application):

	"""应用程序启动初始化
	"""

	def __init__(self):
		routes = load('handler')
		settings = {
			'static_path': os.path.join(os.path.dirname(__file__), "static"),
			'template_path': os.path.join(os.path.dirname(__file__), "tpl"),
			'xsrf_cookies': True,
			'cookie_secret': 'tokyo',
			'site_title': 'zkdash',
			'ui_modules': uimodule,
			'ui_methods': uimethods,
			'debug': OPTIONS.debug,
			'login_url': '/login',
		}
		tornado.web.Application.__init__(self, routes, **settings)

	def log_request(self, handler):
		"""重写tornado request日志
		"""
		status = handler.get_status()
		if status < 400:
			if handler.request.uri[0:7] == '/static':
				return
			log_method = log.info
		elif status < 500:
			log_method = log.warning
		else:
			log_method = log.error
		request_time = 1000.0 * handler.request.request_time()
		if request_time > 30 or OPTIONS.debug or status >= 400:
			log_method("%d %s %.2fms",
					   status,
					   handler._request_summary(),
					   request_time)
			

def daemonize():
	stdin = '/dev/null'
	stderr = '/dev/null'
	stdout = '/dev/null'
	try: 
		pid = os.fork() 
		if pid > 0:
			# exit first parent
				sys.exit(0) 
	except OSError, e: 
		sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
		sys.exit(1)
	
	# decouple from parent environment
	os.chdir(os.path.split(os.path.realpath(__file__))[0]) 
	os.setsid() 
	os.umask(0) 
	
	# do second fork
	try: 
		pid = os.fork() 
		if pid > 0:
			# exit from second parent
			sys.exit(0) 
	except OSError, e: 
		sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
		sys.exit(1) 
	
	# redirect standard file descriptors
	sys.stdout.flush()
	sys.stderr.flush()
	si = file(stdin, 'r')
	so = file(stdout, 'a+')
	se = file(stderr, 'a+', 0)
	os.dup2(si.fileno(), sys.stdin.fileno())
	os.dup2(so.fileno(), sys.stdout.fileno())
	os.dup2(se.fileno(), sys.stderr.fileno())


def make_clean():
	'''清理pyc文件
	'''
	pyshell.shell("find . -name '*.pyc' | xargs rm -rf", debug=True)


def main():
	"""主程序入口
	"""
	logger.init_logger(LOG_ITEMS, suffix=OPTIONS.port)
	application = Application()
	http_server = tornado.httpserver.HTTPServer(application,
												xheaders=True)
	http_server.listen(OPTIONS.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	make_clean()
	main()
