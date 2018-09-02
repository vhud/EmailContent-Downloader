#made to work with outlook
#resilient to network drops and plays catch up once reconnected, keeping records in order

#!/usr/bin/env python3
import email
import imaplib
import os
import sys
import mimetypes
import datetime
import time

mails = []

def mailscheck(msg, setMails, mails):
    '''
    adds m-ID(message-ID) to mails list
    '''
    memory = str(msg['Message-ID'].strip())
    if memory not in setMails:
        mails.append(memory)
        print(memory, '\nadded to mails list')
        mlistadd(memory)
        print('added to mlist file')

def mlistadd(mem):
    '''
    for adding m-ID to NV file mlist
    '''
    with open('emailgrab/mlist', 'a') as f:
        f.write(mem)
        f.write(',')

def mlistloader():
    '''
    for loading message-IDs of read emails from file mlist to memory
    '''
    try:
        with open('emailgrab/mlist') as f:
            reader = f.read()
            m = reader.split(',')
            m = [x for x in m if x != '' and x != '\n']
            return m
    except:
        print("mlist file doesn't exist. create an mlist file.")
        input("press enter to quit...")

def parseit(msg, sender, direct='default', grab='ALL'):
    '''
    parses and breaks up email into files onto local machine at dir 
    set by direct parameter
    '''
    sub = str(msg['Subject']).strip()
    frm = str.casefold(str(msg['From']).strip())
    if sender not in frm:
        return
    if direct == 'default':
        direct = 'emailgrabOutput'
    sub = sub.replace('/','')
    counter = 1
    #walk through message parts
    for part in msg.walk():
        # multipart/* are just containers
        if part.get_content_maintype() == 'multipart':
            continue
        #use file's name if it has one
        filename = part.get_filename()
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                #use a generic extension
                ext = '.bin'
                #use subject of message as beginning of name
            filename = '{}-part-{:03d}{}'.format(sub, counter, ext)
        counter += 1
        #if filename matches the one passed in from main code, write to a 
        #file in direct dir.
        if grab == 'ALL' or filename == grab:
            print(sender, " matches ", frm, "\nsaving file ", filename, \
                " to ", direct)
            try:
                with open(os.path.join(direct, filename), 'wb') as fp:
                    fp.write(part.get_payload(decode=True))
            except:
                continue  
def connection():
    ''' 
    used to connect to the email server
    '''
    u = 'mail.yagoo.com'
    user = 'bob@yagoo.com'
    passy = 'bobsPassWORD'

    server = imaplib.IMAP4(u, 143)
    server.login(user, passy)
    print('logged in to ', user)
    return server

def logReconnect():
    print('\nre-connecting to server...')
    with open('emailgrabOutput/serverdrop.log','a') as f:
        f.write(str(datetime.datetime.now()))
        f.write('\n')
    
def logCorruption(messageDate, fromWho, messageSubject):
    with open('emailgrabOutput/corrupt.log', 'a') as f:
        f.write('email that is located next oldest after: \n')
        f.write(messageDate, fromWho, messageSubject)
        f.write('\ncould not be decoded and is probably corrupt\n')

def main():
    sys.stdout = open('emailgrab.log','w',buffering=1)
    sys.stderr = open('emailgrab.log','w',buffering=1)

    tilt = 0
    m = -1
    check = False
    serverdropcount = 0
    mails = mlistloader()
    setMails = set(mails)
    print(len(mails), ' loaded into mails list')
    server = connection()
    while True:
        try:
            if tilt == 1:
                server = connection()
                serverdropcount += 1
                logReconnect()
                time.sleep(10)
                if server.noop()[0] == 'OK':
                    tilt = 0
                    pass
            if m == 0:
                #if program is caught up, check inbox every 30 seconds
                time.sleep(30)
                m = -1
                check = False
            #try/except in case server drops connection
            a = server.select("INBOX")
            (rv, bmessages) = server.search(None,'ALL')
            #grab newest message from inbox
            if rv == 'OK':
                num = bmessages[0].split()[m]
            else:
                continue
            print("server drops: ", serverdropcount)
            print("\nchecking email #",abs(m),' at ',str(datetime.datetime.now()))
            typ, data = server.fetch(num,'(RFC822)')
            #assign email mimeobject to msg
            try:
                msg = email.message_from_bytes(data[0][1]) 
            except AttributeError:
                print('AttributeError exception, email is most likely corrupted')
                print('logging error location')
                logCorruption(dateRec, recFrom, subRec)
                time.sleep(30)
                m += 1
                continue 
            dateRec = str(msg['Date'].strip())
            mid = str(msg['Message-ID'].strip())
            recFrom = str(msg['From'].strip())
            subRec = str(msg['Subject']).strip()
            print('date on email: ',dateRec, '\n', recFrom)
            if check is True:
                print('checking')
                #insert parseit() with your filter parameters here
                #parseit(msg, '<sender-email>', '<target_dir>','<filename>')
                #parseit(msg, 'bob@example.com', '/targetdir/example', 'file.xls')
                mailscheck(msg, setMails, mails)
                if m < -1:
                    m += 1
                    continue
            if mid != mails[-1]:
                m -= 1
                continue
            if mid == mails[-1]:
                print(mid,'\n is the last entry in mlist')
                m += 1
                check = True
                continue
        except Exception as e:
            print("error - ", str(e))
            print("attempting reconnect in 60 sec")
            time.sleep(60)
            tilt = 1
            continue
if __name__ == '__main__':
    main()
