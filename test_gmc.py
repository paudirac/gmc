import unittest
import gmc

class TestConnection(unittest.TestCase):

    def setUp(self):
        self.email = raw_input("email: ")

    def test_connection(self):
        imap = gmc.connect(self.email)
        self.assertIsNotNone(imap)

    # def test_move(self):
    #     imap = gmp.connect(self.email)
    #     gmp.move(imap, 'prova1', 'prova2')

    def test_label_for(self):
        import datetime
        label_today = gmc.label_for(datetime.datetime(2012,8,22))
        self.assertEqual(label_today, "bak_20120822")
        label_tomorrow = gmc.label_for(datetime.datetime(2012,8,23))
        self.assertEqual(label_tomorrow, "bak_20120823")

if __name__ == '__main__':
    unittest.main()

