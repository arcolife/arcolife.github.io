#!/usr/bin/python2.7
# coding: utf-8
from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

DT = '1991-09-03T19:42:00'
birthdate = parse(DT)
current = datetime.now()
age = relativedelta(current, birthdate)
if current.month < 9 or (current.day <= 3 and current.month == 9):
    DT2 = str(current.year) + '-09-03T19:42:00'
else:
    DT2 = str(current.year+1) + '-09-03T19:42:00'
nextdate = parse(DT2)
age_next = relativedelta(nextdate, current)

print "="*70
print "Hi There! Something you should know about the owner of this instance:"
print "\nArchit Sharma was born on: %s." % \
    (birthdate.strftime("%A,%erd %B %G at %r"))
print "-"*70
print """He is currently: %s years %s months %s days 
%s hours %s minutes and %s seconds old.""" % \
    (age.years, age.months, age.days, age.hours,
     age.minutes, age.seconds)

print "-"*70
print """He would become %s years old in %s months %s days 
%s hours %s minutes and %s seconds from now, \nprecisely, %s\n""" % \
    (age.years+1, age_next.months, age_next.days, 
     age_next.hours, age_next.minutes, age_next.seconds,
    nextdate.strftime("at %r on %A,%erd %B %G"))
print "="*70

wishlist = [#"Rubik's Cube", 
            #"Das Mechanical Keyboard",
            #"A 1 Tb SSD Drive", 
            #"A mobile power charger for his Nexus 4",
            #"Amazone Kindle Paperwhite", 
            "A Skateboard", 
            "Ibanez XF350 Electric Guitar Solid Body - Red Iron Oxide Xiphos", 
            "Trek Bicycles: Session 9.9 / Superfly FS / Fuel EX / Remedy", 
            "Google Glass", 
            "Oculus Rift"]

print "PS: Just in case..\n"
for i, e in enumerate(wishlist): print i+1, e
print "-"*70
print "\t\tHave a Nice Day!! :D  -- arcolife"
print "="*70
