# -*- coding: utf-8 -*-

# Based on http://stackoverflow.com/questions/3527933/move-an-email-in-gmail-with-python-and-imaplib

import imaplib, getpass, re, datetime

class Gmail(object):
    """
    Connection and operations to gmail inbox.
    """

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

    def get_uids_from_label(self, label):

        def get_ids_from_label(label):
            self.__imap.select(mailbox=label, readonly=False)
            resp, items = self.__imap.search(None, 'All')
            if resp == 'OK':
                return items[0].split()
            else:
                return []

        def parse_uid(data):
            pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')
            match = pattern_uid.match(data)
            return match.group('uid')

        def get_message_uid(m_id):
            resp, data = self.__imap.fetch(m_id, "(UID)")
            if resp == 'OK':
                return parse_uid(data[0])
        return map(get_message_uid, get_ids_from_label(label))

    def _delete(self, uid):
        mov, data = self.__imap.uid('STORE', uid, '+FLAGS', '(\Deleted)')
        return mov == 'OK'

    def _copy(self, uid, to_label):
        resp, data = self.__imap.uid('COPY', uid, to_label)
        return resp == 'OK'

    def move_labels(self, from_label, to_label=''):
        uids = self.get_uids_from_label(from_label)
        self.create_label(to_label)

        def try_copy(uid, to_label):
            if self._copy(uid, to_label):
                self._delete(uid)
                return True
            else:
                return False

        while len(uids) > 0:
            uid = uids.pop()
            while not try_copy(uid, to_label):
                pass
        self.__imap.expunge()

    def label_exists(self, label):
        def pattern(label):
            return re.compile(".*\"%(label)s\"$" % locals())

        res, mailboxes = self.__imap.list()
        if res == 'OK':
            return any(pattern(label).match(mailbox) for
                       mailbox in mailboxes)
        else:
            raise "Connection error"

    def create_label(self, label):
        if not self.label_exists(label):
            self.__imap.create(label)

    def delete_label(self, label):
        if self.label_exists(label):
            uids = self.get_uids_from_label(label)
            while len(uids) > 0:
                uid = uids.pop()
                while not self._delete(uid):
                    pass
            self.__imap.expunge()
            self.__imap.delete(label)

def label_for(date=datetime.datetime.today()):
    return date.strftime("bak_%Y%m%d")

def main(email,backup_labels,delete_previous=False):
    gmail = Gmail(email)
    new_label = label_for()
    gmail.connect()
    gmail.create_label(new_label)
    for label in backup_labels:
        gmail.move_labels(label, new_label)
    # if delete_previous:
    #     pattern = ''
    #     prvious_labels = gmail.find_labels(pattern)
    #     for label in previous_labels:
    #         gmail.delete_label(label)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Clean your mailbox')
    parser.add_argument('email', type=str,
                        help="email address you want to clean")

    parser.add_argument('backup_labels',
                        type=str,
                        nargs='*',
                        help="a list of labels to be backuped",
                        default=False)

    args = parser.parse_args()
    main(args.email, args.backup_labels)

