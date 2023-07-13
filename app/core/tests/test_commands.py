from unittest.mock import patch


from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

# @patch('core.management.commands.wait_for_db.Command.check')


@patch('django.db.connection.cursor')
class CommandTests(TestCase):
    """ Test Commands """

    def test_wait_for_db_ready(self, patched_cursor):
        """ Test waiting for database if database is ready """
        patched_cursor.return_value = True

        call_command('wait_for_db')

        patched_cursor.assert_called()

    # @patch('core.management.commands.wait_for_db.Command.handle.db_conn.cursor')
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_time, patched_cursor):
        """ Test waiting for database if database is ready """
        patched_cursor.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_cursor.call_count, 6)
        patched_cursor.assert_called()
