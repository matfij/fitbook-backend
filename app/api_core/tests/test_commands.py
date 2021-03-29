from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    connection_handler = 'django.db.utils.ConnectionHandler.__getitem__'

    def test_wait_for_db_ready(self):
        '''Happy path'''
        with patch(self.connection_handler) as get_item:
            get_item.return_value = True
            call_command('wait_for_db')

            self.assertEqual(get_item.call_count, 1)

    @patch('time.sleep', return_value=True)
    def est_wait_for_db_ready(self, ts):
        '''Wait for db for 5 + 1 cycles'''
        with patch(self.connection_handler) as get_item:
            get_item.side_effect = [OperationalError]*5 + [True]
            call_command('wait_for_db')

            self.assert_(get_item.call_count, 6)
