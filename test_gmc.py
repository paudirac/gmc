import unittest
import gmc

class TestGmail(unittest.TestCase):

    def setUp(self):
        self.gmail = gmc.Gmail(ask_email())

    # def test_connection(self):
    #     self.gmail.connect()
    #     self.assertIsNotNone(self.gmail._Gmail__imap)
    #     self.gmail.disconnect()

    # def test_labels(self):
    #     self.gmail.connect()
    #     msgs = self.gmail.get_uids_from_label(ask_label())
    #     print(msgs)
    #     self.gmail.disconnect()

    # def test_move(self):
    #     self.gmail.connect()
    #     self.gmail.move_labels(ask_label("source: "), ask_label("destination: "))

    # def test_create_label(self):
    #     self.gmail.connect()
    #     self.gmail.create_label(gmc.label_for())
    #     self.gmail.disconnect()

    def test_delete_label(self):
        self.gmail.connect()
        self.gmail.create_label('prova')
        self.gmail.delete_label('prova')
        self.gmail.disconnect()

class TestLabels(unittest.TestCase):

    def test_label_for(self):
        import datetime
        label_today = gmc.label_for(datetime.datetime(2012,8,22))
        self.assertEqual(label_today, "bak_20120822")
        label_tomorrow = gmc.label_for(datetime.datetime(2012,8,23))
        self.assertEqual(label_tomorrow, "bak_20120823")

def ask_email():
    return raw_input("email: ")
def ask_label(prompt="label: "):
    return raw_input(prompt)

if __name__ == '__main__':
    unittest.main()


