 # -*- coding: utf-8 -*-
from time import *
from calendar import timegm
import calendar

mktime = lambda time_tuple: calendar.timegm(time_tuple) + timezone