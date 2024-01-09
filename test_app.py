import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Unit Test: Test the home page loads correctly
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200, "Homepage should return 200 OK")

    # Unit Test: Test adding an item
    def test_add_item(self):
        response = self.app.post('/add', data=dict(item="Test Item"), follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Response should be 200 OK")
        self.assertIn("Test Item", response.data.decode(), "Added item should be visible on the page")

    # Integration Test: Test adding, updating, and deleting an item
    def test_integration_add_update_delete(self):
        # Add an item
        self.app.post('/add', data=dict(item="Integration Test Item"), follow_redirects=True)
        
        # Update the added item
        self.app.post('/update/0', data=dict(new_item="Updated Integration Test Item"), follow_redirects=True)

        # Delete the updated item
        delete_response = self.app.get('/delete/0', follow_redirects=True)
        self.assertEqual(delete_response.status_code, 200, "Deleting item should be successful")

        # Verify the item is deleted
        final_response = self.app.get('/')
        self.assertNotIn("Updated Integration Test Item", final_response.data.decode(), "Deleted item should no longer be visible")

if __name__ == '__main__':
    unittest.main()
