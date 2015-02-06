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
# Import smtplib for the actual sending function
import smtplib
import ConfigParser
import pickle as pkl
import subprocess as sp
# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


config = ConfigParser.RawConfigParser()
config.read('/etc/sentinel/sentinel_configure.cfg')

destination_email = config.get('Email_configure', 'd_email')
senders_email = config.get('Email_configure', 's_email')
smtp_server = config.get('Email_configure', 'smtp_server')
smtp_port = config.getint('Email_configure', 'smtp_port')
username = senders_email
password = config.get('Email_configure', 'password')
archive_directory = config.get('General_configure', 'archive_dir')
pics_directory = config.get('General_configure', 'motion_dir')
ip_address = config.get('Network', 'ip_address')
previous_intrusion_datetime = pkl.load(open("last_intrusion.p", "rb" ))
current_intrusion_datetime = datetime.datetime.now()
intrusion_time_delta = current_intrusion_datetime - previous_intrusion_datetime 
MAX_PICS_BEFORE_EMAIL = 5


def owner_at_home():
    '''Performs an arp-scan and returns a string. We will scan the string
    and search for our network address'''
    networks = ' '
    for i in range(5):
        networks = networks+sp.check_output(['sudo', 'arp-scan' ,'-interface', 'wlan0', '--localnet'])
        if ip_address in networks:
            return True
        else:
            continue
    return False


def email_sender():
    ''' Counts the number of pictures in the /tmp/motion' folder and if the 
    number of pics is  geq 5, then we first send an email to the user with 
    those pics attached, and we will move those pics to an archive folder, 
    with the date and time of intrusion. We will also store the current date 
    and time in a pickle file, and will click more pics only if 
    current time is greater than 5 mins of the last intrusion'''
    if not owner_at_home():
        pics = [f for f in os.listdir(pics_directory) if f.endswith('.jpg')]
        image_count = len(pics)

        if image_count >= MAX_PICS_BEFORE_EMAIL and (intrusion_time_delta >= 
                        datetime.timedelta(minutes=1)): 
            # Create the container (outer) email message.
            msg = MIMEMultipart('mixed')
            msg['Subject'] = ('[SENTINEL MSG]['+str(current_intrusion_datetime)+']'
            'The sentinel has spotted an intruder!')
            msg['From'] = senders_email
            msg['To'] = destination_email
            msg.preamble = 'Pics of the intruder:'
           
            for p in pics:
                try:
                    fp = open(pics_directory+'/'+p, 'rb')
                    print "File opened Successfully"
                    img = MIMEImage(fp.read())
                    fp.close()
                    msg.attach(img)
                    print "Image attached to email"
                except:
                    print ("[ERROR]: Couldn't attach picture "+p+". "
                    "Exiting this pass.")
                    return
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

            pkl.dump((current_intrusion_datetime, 
                open("/home/pi/sentinel/last_intrusion.p", "wb")))
            #Make a directory in the Motion archives folder 
            #with the current date and time name
            os.mkdir(archive_directory+'/'+str(current_intrusion_datetime))
            #Add the present pics to this archived folder
            for p in pics:
                os.rename((pics_directory+'/'+p,  
                    archive_directory+'/'+str(current_intrusion_datetime)+'/'+p))

        else:
            print "Secretly snapping the intruder."
    else:
        print "Owner is home. Sorry, false alarm, deleting clicked pics now..."
        if os.listdir(pics_directory) == []:
            return 
        else:
            sp.check_output(['sudo', 'rm' , pics_directory+'/*.jpg'])
            sp.check_output(['sudo', 'rm', pics_directory+'/*.swf'])

def main():
    #Simply call the Email Sender function for now
    email_sender()


if __name__ == '__main__':
    main()
