import unittest

try:
    import tests.utils as test_utils
except ImportError:
    import utils as test_utils

class TestConnection(unittest.TestCase):
    
    def runTest(self):
        connection = test_utils.get_test_connection()

        with connection:
            result = connection.execute_scalar('SELECT 1 + 1')
            self.assertEqual(result, 2)
