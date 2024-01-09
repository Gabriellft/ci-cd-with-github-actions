import unittest
from app import app,items

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    # Unit test for add_item function
    def test_add_item(self):
        initial_count = len(items)
        response = self.app.post('/add', data={'item': 'Test Item'})
        self.assertEqual(response.status_code, 302)  # redirect status code
        self.assertEqual(len(items), initial_count + 1)
        self.assertIn('Test Item', items)

    # Unit test for delete_item function
    def test_delete_item(self):
        items.append('Delete Me')
        delete_index = len(items) - 1
        response = self.app.get(f'/delete/{delete_index}')
        self.assertEqual(response.status_code, 302)  # redirect status code
        self.assertNotIn('Delete Me', items)

    # Integration test
    def test_add_and_delete_integration(self):
        # Add an item
        add_response = self.app.post('/add', data={'item': 'Integration Test'})
        self.assertIn('Integration Test', items)

        # Delete the same item
        delete_index = items.index('Integration Test')
        delete_response = self.app.get(f'/delete/{delete_index}')
        self.assertNotIn('Integration Test', items)

if __name__ == '__main__':
    unittest.main()
