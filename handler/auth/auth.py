#!/usr/bin/env python
# -*- coding: utf-8 -*-
from handler.bases import CommonBaseHandler
from model.db.zd_login_auth import ZdLogin
import operator
from lib import route

@route(r'/auth/login','登录')
class Loginpage(CommonBaseHandler):
	def get(self):
		return self.render('auth/login.html',
						   action='/authuser',)
	

@route(r'/authuser')
class LoginHandler(CommonBaseHandler):
	def post(self):
		self.username = self.get_argument("user")
		self.password = self.get_argument("pass")
		if not isinstance(self.q_user(),ZdLogin):
			self.write('auth failed')
			return
		self.set_secure_cookie("tokyo", self.username, expires_days=None)
		self.redirect("/")
		
	def q_user(self):
		try:
			self.active = ZdLogin.select().where(ZdLogin.uname == self.username).get()
		except ZdLogin.DoesNotExist:
			self.userexist = None
			return self.userexist
			
		try:
			self.userexist = self.active.select().where((ZdLogin.pwd == self.password) & (ZdLogin.uname == self.username)).get()
		except ZdLogin.DoesNotExist:
			self.userexist = None

		return self.userexist
	

@route(r'/logout')
class LoginOut(CommonBaseHandler):
	def get(self):
		if self.current_user:
			self.clear_cookie("tokyo")
			
		self.redirect("/auth/login")
		
