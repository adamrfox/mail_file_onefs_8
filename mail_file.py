#!/usr/bin/python

import smtplib
import sys
import getopt
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

#
# DEFINE YOUR VARIABLES HERE
#
SERVER = "mymailhost.com"
PORT = 587
USER = "mailhost_user@xx.com"		# Comment out if no auth needed
PASSWD = "password"			# Comment out if no auth needed
FROM = "xx@xx.com"
#
attach_flag = False
mime_type1 = "application"
mime_type2 = "octet-stream"
optlist, args = getopt.getopt (sys.argv[1:], 't:s:an:m:', ['to=', 'subject=','attach', 'name=', "mimetype="])
for opt, a in optlist:
  if opt in ('-t', '--to'):
    TO = a
    to_list = TO.split(",")
  if opt in ('-s', '--subject'):
    SUBJECT = a
  if opt in ('-a', '--attach'):
    attach_flag = True
  if opt in ('-n', '--name'):
    file_name = a
  if opt in ('-m', '--mimetype'):
    mt = a.split ('/')
    mime_type1 = mt[0]
    mime_type2 = mt[1]

try:
  TO
except NameError:
  sys.stderr.write ("A Reciepient must be defined.  Use -t or --to=")
  exit (1)
try:
  SUBJECT
except NameError:
  sys.stderr.write ("A Subject must be defined.  Use -s or --subject=")
  exit (1)
AUTH = True
try:
  USER
except NameError:
  AUTH = False
if AUTH == True:
  try:
    PASSWD
  except NameError:
    AUTH = False
FILE_FLAG = True
try:
  args[0]
except:
  FILE_FLAG = False
if FILE_FLAG == True:
  FILE = args[0]
  with open (FILE, "rb") as email_file:
    TEXT = email_file.read()
else:
  TEXT = sys.stdin.read()
if attach_flag == False:
  message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, TO, SUBJECT, TEXT)
  try:
    server = smtplib.SMTP(SERVER,PORT)
    server.ehlo()
    server.starttls()
    if AUTH == True:
      server.login(USER, PASSWD)
    server.sendmail (FROM, to_list, message)
    server.close()
    print "Message Sent"
  except:
    sys.stderr.write ("Message Failed to Send")
else:
  if FILE_FLAG == True:
    file_name = FILE
  fnf = file_name.split('/')
  short_name = fnf.pop()
  msg = MIMEMultipart()
  msg['From'] = FROM
  msg['To'] = TO
  msg['Date'] = formatdate(localtime = True)
  msg['Subject'] = SUBJECT
  part = MIMEBase(mime_type1,mime_type2)
  part.set_payload (TEXT)
  encoders.encode_base64(part)
  part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(short_name))
  msg.attach(part)
  try:
    server = smtplib.SMTP(SERVER, PORT)
    server.ehlo()
    server.starttls()
    if AUTH == True:
      server.login (USER, PASSWD)
    server.sendmail (FROM, to_list, msg.as_string())
    server.quit()
    print "Message Sent"
  except:

    sys.stderr.write ("Message Failed to Send")
