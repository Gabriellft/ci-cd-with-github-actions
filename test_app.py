import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
       
        self.app = app.test_client()
        self.app.testing = True

    def test_read_page(self):
        # check if the page is loaded
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200, "Homepage should return 200 OK")
        

    def test_add_item(self):
        # Test adding an item to the list
        response = self.app.post('/add', data=dict(item="Test Item"), follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Response should be 200 OK")
        self.assertIn("Test Item", response.data.decode(), "Added item should be visible on the page")

    def test_delete_item(self):
        # Delete is a Get instead of Post
        # Add an item first
        self.app.post('/add', data=dict(item="Delete Me"), follow_redirects=True)
        
        # Debug print
        #response = self.app.get('/')
        #print("Before deletion:", response.data.decode())

        # Attempt to delete the first item
        response = self.app.get('/delete/1', follow_redirects=True)
        
        # Debug print
        response_after_delete = self.app.get('/')
        #print("After deletion:", response_after_delete.data.decode())

        self.assertNotIn("Delete Me", response_after_delete.data.decode(), "Deleted item should no longer be visible")


    def test_update_item(self):
        # Add an item first, then attempt to update it
        self.app.post('/add', data=dict(item="Old Item"), follow_redirects=True)
        response = self.app.post('/update/1', data=dict(new_item="Updated Item"), follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Response should be 200 OK")
        self.assertIn("Updated Item", response.data.decode(), "Updated item should display the new value")

if __name__ == '__main__':
    unittest.main()
