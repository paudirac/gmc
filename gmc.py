# -*- coding: utf-8 -*-

# Based on http://stackoverflow.com/questions/3527933/move-an-email-in-gmail-with-python-and-imaplib

# 1. Mirar etiquetes anteriors i borrar-les
# 2. Crear etiqueta d'avui
# 3. Mirar etiquetes_a_moure i exclude
# 4. Moure tot allò que no sigui exclude de les etiquetes_a_moure a
# avui
# 5. Ja està

import imaplib, getpass, re, datetime
pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')

class Gmail(object):
    """Connection and operations to gmail inbox.
    """

    pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')
    def __init__(self, email):
        """Initializes a gmail connection to email account.

        Arguments:
        - `email`:
        """
        self.__email = email

    def connect(self):
        try:
            self.__imap = imaplib.IMAP4_SSL('imap.gmail.com')
            password = getpass.getpass("Enter your password: ")
            self.__imap.login(self.__email, password)
        except Exception, e:
            print("No ha sigut possible connectar")
            raise e

    def disconnect(self):
        self.__imap.logout()

    def get_from_label(self, label):
        """
        Returns a list of id's of messages of the mailbox label
        Arguments:
        - `label`:
        """
        self.__imap.select(mailbox=label, readonly=False)
        resp, items = self.__imap.search(None, 'All')
        if resp == 'OK':
            return items[0].split()
        else:
            return []

    def get_uids_from_label(self, label):
        def get_message_uid(m_id):
            resp, data = self.__imap.fetch(m_id, "(UID)")
            if resp == 'OK':
                return parse_uid(data[0])
        return map(get_message_uid, self.get_from_label(label))

def get_all_from(imap, label):
    """Returns a list of id's of messages of the mailbox label"""
    imap.select(mailbox=label, readonly=False)
    resp, items = imap.search(None, 'All')
    if resp == 'OK':
        return items[0].split()
    else:
        return []


def connect(email):
    try:
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        password = getpass.getpass("Enter your password: ")
        imap.login(email, password)
        return imap
    except Exception, e:
        print("No ha sigut possible connectar")
        print(e)
        raise e

def disconnect(imap):
    imap.logout()

def parse_uid(data):
    match = pattern_uid.match(data)
    return match.group('uid')

def get_all_from(imap, label):
    """Returns a list of id's of messages of the mailbox label"""
    imap.select(mailbox=label, readonly=False)
    resp, items = imap.search(None, 'All')
    if resp == 'OK':
        return items[0].split()
    else:
        return []

def get_message_uid(imap, m_id):
    resp, data = imap.fetch(m_id, "(UID)")
    if resp == 'OK':
        return parse_uid(data[0])

def move_to(imap, msg_uid, destination):
    resp, data = imap.uid('COPY', msg_uid, destination)
    if resp == 'OK':
        mov, data = imap.uid('STORE', msg_uid, '+FLAGS', '(\Deleted)')
        return True
    else:
        return False

def move(imap, label1, label2):
    msgs = get_all_from(imap, label1)
    while len(msgs) > 0:
        msg = msgs.pop()
        msg_uid = get_message_uid(imap, msg)
        while not move_to(imap, msg_uid, label2):
            pass
    imap.expunge()

def main(email, reverse=False):
    imap = connect(email)
    a, b = 'etiqueta-u', 'etiqueta-dos'
    if reverse:
        a, b = b, a
        imap.delete(label_for())
    move(imap, a, b)
    if not reverse:
        imap.create(label_for())
    disconnect(imap)

def label_for(date=datetime.datetime.today()):
    return date.strftime("bak_%Y%m%d")

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Clean your mailbox')
    parser.add_argument('email', type=str,
                        help="email address you want to clean")

    parser.add_argument('-r', '--reverse', metavar='reverse',
                        action='store_const',
                        const=True,
                        default=False,
                        help="changes reversely")

    args = parser.parse_args()
    main(args.email, reverse=args.reverse)

