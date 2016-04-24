#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

from peewee import CharField
from peewee import IntegerField
from peewee import SQL

from model.db.base import ZKDASH_DB, EnumField


class ZdLogin(ZKDASH_DB.Model):

    """ZdZnode Model
    """

    id = IntegerField(primary_key=True, constraints=[SQL("AUTO_INCREMENT")])
    uname = CharField(max_length=10, null=False)
    pwd = CharField(max_length=16, null=False)

    class Meta(object):

        """表配置信息
        """
        db_table = "zd_login_auth"
