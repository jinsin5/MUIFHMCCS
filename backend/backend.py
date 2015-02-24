import smtplib
from email.mime.text import MIMEText
#from sql import *
#from sql.aggregate import *
#from sql.conditionals import *

USERNAME = 'm.jansen.555@gmail.com'
PASSWORD = 'password'

PARSABLE_FIELDS = ['flow', 'alarm', 'sash']
KNOWN_FILENAMES = ['abb.txt', 'bsb.txt']
PATH_TO_FILE = r"/home/michael/Dropbox/School Work/capstone/backend/fumehooddata/"

#data = {'abb': {'a201': {'flow': 66.7, 'alarm': 0, 'sash': 0},'a202': {'flow': 55.7, 'alarm': 0, 'sash': 0}, '301': {'flow': 0, 'alarm': 1, 'sash': 0}}

def send_email():
    # Send the message through gmail
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(USERNAME, PASSWORD)

    headers = "\r\n".join(["from: " + USERNAME,
                           "subject: " + 'Test email from email server',
                           "to: " + USERNAME,
                           "mime-version: 1.0",
                           "content-type: text/html"])

    # body_of_email can be plaintext or html!
    content = headers + "\r\n\r\n" + 'Hello Garrett, send a reply if you are reading this.'
    s.sendmail(USERNAME, 'patriqga@mcmaster.ca', content)

def main():
    files_dict = {}
    building_dict = {}
    room_dict = {}
    field_position = 0

    #open and store all files
    for file_name in KNOWN_FILENAMES:
        files_dict.update({file_name.split('.')[0]:PATH_TO_FILE+file_name})

    while(1):
        for building, file_name in files_dict.iteritems():
            fd = open(file_name, 'rw')
            #iterate through each line
            for line in fd:
                field_position = 0
                data = line.split(' | ')

                # iterate through each data field
                for item in data:
                    for field in PARSABLE_FIELDS:
                        if field in item:
                            room = item.split(field)[0]
                            if room not in room_dict:
                                room_dict[room] = {field:field_position}
                            else:
                                for k, v in room_dict.iteritems():
                                    if room == k:
                                        v[field] = field_position
                                        break
                    field_position += 1

                #move to next line and add in values for each field
                line = fd.next()
                data = line.split(' | ')
                for k, v in room_dict.iteritems():
                    for key, field in v.iteritems():
                        v[key] = data[field].rstrip()

                # reset index
                field_position = 0

            building_dict[building]=room_dict

        #delete all contents in files
        print building_dict
        #sleep(900)
        break
    sql(building_dict)

def sql(building_dict):
    for building, rooms_dict in building_dict.iteritems():
        for rooms, parameters in rooms_dict.iteritems():
            #fill in ID, value, and times
            #sql.add(ID, parameters['sash'], value, parameters[flow], time, created, updated, parameters[alarm])

if __name__ == '__main__':
    main()