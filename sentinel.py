#!/usr/bin/env python
'''
Copyright 2015 Yash Chitalia

This file is part of Sentinel.

Sentinel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sentinel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sentinel.  If not, see <http://www.gnu.org/licenses/>.
'''
import os, sys
import datetime
from time import sleep
# Import smtplib for the actual sending function
import smtplib
import ConfigParser
import pickle as pkl
# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

current_intrusion_datetime = datetime.datetime.now()
MAX_PICS_BEFORE_EMAIL = 5
config = ConfigParser.RawConfigParser()
config.read('/etc/sentinel/sentinel_configure.cfg')

destination_email = config.get('Email_configure', 'd_email')
senders_email = config.get('Email_configure', 's_email')
smtp_server = config.get('Email_configure', 'smtp_server')
smtp_port = config.getint('Email_configure', 'smtp_port')
username = senders_email
password = config.get('Email_configure', 'password')
archive_directory = config.get('General_configure', 'archive_dir')
motion_directory = config.get('General_configure', 'motion_dir')


def owner_at_home():
    '''Performs an arp-scan and returns a string. We will scan the string
    and search for our network address'''
    return pkl.load(open("/home/pi/sentinel/at_home.p", "rb" ))


def pic_mover():
    ''' Will move the number of pics indicated by MAX_PICS_BEFORE_EMAIL
    and will store them in an archive directory with the name being 
    equal to the current date and time. These pics are stored by motion in the 
    directory indicated'''
    while len(os.listdir(motion_directory)) < (MAX_PICS_BEFORE_EMAIL+3):
        pass
    #Make a directory in the Motion archives folder 
    #with the current date and time name
    os.mkdir(archive_directory+'/'+str(current_intrusion_datetime))
    #Add the present pics to this archived folder
    pics = [f for f in os.listdir(motion_directory) if f.endswith('.jpg')]
    print pics
    for p in range(MAX_PICS_BEFORE_EMAIL):
        os.rename(motion_directory+'/'+pics[p], archive_directory+'/'+str(current_intrusion_datetime)+'/image_'+str(p)+'.jpg')
    print "Finished transferring images into archives"


def email_sender():
    ''' Sends the pics clicked in the folder stored in the archives
    directory'''
    pics = [f for f in os.listdir(archive_directory+'/'+str(current_intrusion_datetime)) if f.endswith('.jpg')]
    image_count = len(pics)
    print "Number of pics we plan to upload:{}".format(image_count)
    # Create the container (outer) email message.
    msg = MIMEMultipart('mixed')
    msg['Subject'] = ('[SENTINEL MSG]['+str(current_intrusion_datetime)+']'
    'The sentinel has spotted an intruder!')
    msg['From'] = senders_email
    msg['To'] = destination_email
    msg.preamble = 'Pics of the intruder:'
    for p in pics:
        try:
            fp = open(archive_directory+'/'+str(current_intrusion_datetime)+'/'+p, 'rb')
            print "File opened Successfully"
            img = MIMEImage(fp.read())
            fp.close()
            msg.attach(img)
            print "Image {} attached to email".format(p)
        except:
            print ("[ERROR]: Couldn't attach picture "+p+". "
            "Exiting this pass.")
            continue
    try:
        # Send the email via gmail's SMTP server.
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        try:
            server.login(username, password)
            print "Login Successful"
        except:
            print ("[ERROR]: Could not log in."
            "Are your login details correct?")
            return
        server.sendmail(senders_email, [destination_email], msg.as_string())
        server.close()
        print "Email Sent Successfully!"
    except:
        print ("[ERROR] Sendmail function may not be getting the right "
        "objects. Email not sent.")
        return


def main():
    '''If owner is not at home, click pics of intruder on event'''
    if (not owner_at_home()): 
        #Click pics
        pic_mover()
        #Send email
        email_sender()
    else:
        print "Owner is home. Sorry, false alarm.."
        return


if __name__ == '__main__':
    main()
