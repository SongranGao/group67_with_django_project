from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import UserProfile, EmailVerifyRecord
from users.forms import (
    LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm,
    UserForm, UserProfileForm
)
from django.contrib.auth.hashers import check_password, make_password
from datetime import date


### TESTING MODELS ###
class UserProfileTestCase(TestCase):

    def setUp(self):
        self.user, created = User.objects.get_or_create(username="testuser", defaults={
            "email": "test@example.com",
            "password": "password123"
        })
        self.profile = UserProfile.objects.get_or_create(
            owner=self.user,
            nike_name="Test Nickname",
            desc="This is a test user profile.",
            character_signature="Live, Laugh, Code.",
            birthday=date(2000, 1, 1),
            gender="male",
            address="123 Test Street",
            image="images/test_user.png"
        )

    def test_profile_creation(self):
        profile = UserProfile.objects.get(owner=self.user)
        self.assertEqual(profile.nike_name, "Test Nickname")
        self.assertEqual(profile.gender, "male")
        self.assertEqual(profile.address, "123 Test Street")
        self.assertTrue(profile.image.url.endswith("test_user.png"))

    def test_str_method(self):
        profile = UserProfile.objects.get(owner=self.user)
        self.assertEqual(str(profile), self.user.username)


class EmailVerifyRecordTestCase(TestCase):

    def setUp(self):
        self.email_record = EmailVerifyRecord.objects.create(
            code="123456",
            email="test@example.com",
            send_type="register"
        )

    def test_email_record_creation(self):
        record = EmailVerifyRecord.objects.get(code="123456")
        self.assertEqual(record.email, "test@example.com")
        self.assertEqual(record.send_type, "register")

    def test_str_method(self):
        record = EmailVerifyRecord.objects.get(code="123456")
        self.assertEqual(str(record), "123456")


### TESTING FORMS ###
class UserFormsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.user_profile = UserProfile.objects.create(owner=self.user, nike_name="Test Nickname")

    def test_login_form_valid(self):
        form_data = {'username': 'testuser', 'password': 'password123'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_valid(self):
        form_data = {
            'email': 'newuser@example.com',
            'password': 'password123',
            'password_1': 'password123'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_email_exists(self):
        form_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'password_1': 'password123'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_register_form_password_mismatch(self):
        form_data = {
            'email': 'newuser@example.com',
            'password': 'password123',
            'password_1': 'password456'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password_1', form.errors)


### TESTING VIEWS ###
class UserViewsTestCase(TestCase):

    def setUp(self):
        """Create a test user"""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        self.profile = UserProfile.objects.create(owner=self.user, nike_name="Test Nickname")

    def test_register_user(self):
        """ Test user registration """
        response = self.client.post(reverse('users:register'), {
            "email": "newuser@example.com",
            "password": "testpassword123",
            "password_1": "testpassword123"
        })


        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_login_view_success(self):
        """Test login success"""
        response = self.client.post(reverse('users:login'), {
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:user_profile'))

    def test_login_view_failure(self):
        response = self.client.post(reverse('users:login'), {
            "username": "testuser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The account or password is incorrect")

    def test_logout_view(self):
        """Test user logout"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('users:login'))

    def test_user_profile_unauthorized(self):
        response = self.client.get(reverse('users:user_profile'))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_authorized(self):
        """Login to access user profile page, return 200"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('users:user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_profile.html")

    def test_editor_users(self):
        """ Test user profile edit """
        self.client.login(username="testuser", password="password123")

        response = self.client.post(reverse('users:editor_users'), {
            "email": "test@example.com",
            "nike_name": "Updated Name",
            "desc": "New description",
            "gender": "male",
            "birthday": "2000-01-01",
            "address": "New Test Address",
        })

        self.assertRedirects(response, reverse('users:user_profile'))

    def test_forget_password(self):
        """Test forgot password, send verification code"""
        response = self.client.post(reverse('users:forget_pwd'), {
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(EmailVerifyRecord.objects.filter(email="test@example.com").exists())

    def test_forget_password_reset(self):
        """Test users reset their passwords via email """
        email_record = EmailVerifyRecord.objects.create(email="test@example.com", code="123456")
        response = self.client.post(reverse('users:forget_pwd_url', args=[email_record.code]), {
            "password": "newpassword123",
            "password_confirm": "newpassword123"
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(check_password("newpassword123", self.user.password))

    def test_activate_user(self):
        """Test user activation"""
        email_record = EmailVerifyRecord.objects.create(email="test@example.com", code="activate123")
        response = self.client.get(reverse('users:active_user', args=[email_record.code]))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_staff)




