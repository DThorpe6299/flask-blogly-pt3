from unittest import TestCase
from models import db, User, Post
from app import app

class TestBloglyApp(TestCase):
    def setUp(self):
        """Set up the test app."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'  # Use a different database for testing
        self.client = app.test_client()

        # Create a test user and post for testing specific routes
        with app.app_context():
            db.create_all()
            user = User(first_name='Test', last_name='User', image_url='test.jpg')
            db.session.add(user)
            db.session.commit()
            post = Post(title='Test Post', content='This is a test post', user_id=user.id)
            db.session.add(post)
            db.session.commit()

    def tearDown(self):
        """Clean up after testing."""
        with app.app_context():
            db.drop_all()

    def test_home_redirect(self):
        """Test if '/' redirects to '/users'."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/users')

    def test_list_users(self):
        """Test if '/users' returns a status code 200."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        """Test if adding a user redirects to '/users'."""
        data = {'first_name': 'John', 'last_name': 'Doe', 'image_url': 'john.jpg'}
        response = self.client.post('/users/new', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 302)  # Check for successful redirect

    def test_user_details(self):
        """Test if user details page returns a status code 200."""
        response = self.client.get('/user/1')
        self.assertEqual(response.status_code, 200)

    def test_edit_user(self):
        """Test if editing a user redirects to '/users'."""
        data = {'first_name': 'Jane', 'last_name': 'Smith', 'image_url': 'jane.jpg'}
        response = self.client.post('/user/1/edit', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 302)