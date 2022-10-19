import email
import smtp
import imaplib
from imaplib import IMAP4_SSL
import sys
from email.mime.text import MIMEText
from email.parser import HeaderParser
from email.policy import default
from credentials import*

class EmailClient:
    def __init__(self):
        self.server=IMAP4_SSL(IMAP_SERVER, port=IMAP_SERVER_PORT)
        try:
            #smtp.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
            rv, data=self.server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        except imaplib.IMAP4.error as e:
            print(str(e))
            print(f'Cannot login into email: {EMAIL_ACCOUNT}')
            sys.exit(1)
        print('Logged in')
        rv, mailboxes=self.server.list()
        if rv=='OK':
            print('Mailboxes:')
            for mailbox in mailboxes:
                print(str(mailbox))
        rv, data=self.server.select(EMAIL_FOLDER)
        if rv=='OK':
            print('Processing mailbox')
            self.process_mailbox(data)
            self.server.close()
        else:
            print('Cannot open mailbox')
        self.server.logout()
    def process_mailbox(self, mailbox):
        rv, data=self.server.search(None, "(UNSEEN)")
        if rv!='OK':
            print('No unread messages')
            return

        for num in data[0].split():
            rv, data = self.server.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("ERROR getting message", num)
                return

            msg = email.message_from_bytes(data[0][1])
            print(data)
            #print(msg)
            #headers = HeaderParser().parsestr(msg.as_string())
            #sender = ''.join(email.parser.findall(headers['From'])).strip()
            #print('The sender is {}'.format(sender))

if __name__=='__main__':
    client=EmailClient()
