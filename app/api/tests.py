"""
Test fayllari - CI/CD da avtomatik ishga tushadi.
python manage.py test  yoki  pytest
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from app.api.models import Todo


class TodoAPITestCase(TestCase):
    """Todo API ni to'liq test qilish."""

    def setUp(self):
        """Har bir test oldidan ishga tushadi."""
        self.client = APIClient()

        # Test foydalanuvchi yaratish
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpass123",
        )
        # Foydalanuvchini tizimga kirgazish
        self.client.force_authenticate(user=self.user)

        # Test todo yaratish
        self.todo = Todo.objects.create(
            owner=self.user,
            title="Test vazifasi",
            description="Bu test uchun",
            priority=Todo.Priority.HIGH,
        )

    # ---- CRUD testlar ----

    def test_todo_list(self):
        """GET /api/todos/ - faqat o'z todoları keladi."""
        # Boshqa foydalanuvchi todosi
        Todo.objects.create(owner=self.other_user, title="Boshqaning todo")

        response = self.client.get("/api/todos/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Faqat bitta (o'ziniki) qaytadi
        self.assertEqual(response.data["count"], 1)

    def test_todo_create(self):
        """POST /api/todos/ - yangi todo yaratish."""
        data = {
            "title": "Yangi vazifa",
            "description": "Tavsif",
            "priority": "low",
        }
        response = self.client.post("/api/todos/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Yangi vazifa")
        self.assertEqual(response.data["owner"]["username"], "testuser")

    def test_todo_detail(self):
        """GET /api/todos/{id}/ - bitta todo."""
        response = self.client.get(f"/api/todos/{self.todo.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test vazifasi")

    def test_todo_update(self):
        """PATCH /api/todos/{id}/ - qisman yangilash."""
        response = self.client.patch(
            f"/api/todos/{self.todo.id}/",
            {"title": "Yangilangan sarlavha"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Yangilangan sarlavha")

    def test_todo_delete(self):
        """DELETE /api/todos/{id}/ - o'chirish."""
        response = self.client.delete(f"/api/todos/{self.todo.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())

    def test_toggle_complete(self):
        """POST /api/todos/{id}/toggle/ - bajarildi belgisi."""
        self.assertFalse(self.todo.is_completed)

        response = self.client.post(f"/api/todos/{self.todo.id}/toggle/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_completed"])

    # ---- Xavfsizlik testlari ----

    def test_unauthenticated_user_cannot_access(self):
        """Login qilmagan foydalanuvchi ruxsat olmaydi."""
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/todos/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_access_others_todo(self):
        """Boshqaning todosiniga kira olmaydi."""
        other_todo = Todo.objects.create(
            owner=self.other_user,
            title="Boshqaning sir vazifasi",
        )
        response = self.client.get(f"/api/todos/{other_todo.id}/")
        # 404 qaytadi (o'zining querysetida yo'q)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_completed(self):
        """?is_completed=true filtri ishlaydi."""
        Todo.objects.create(owner=self.user, title="Bajarilgan", is_completed=True)

        response = self.client.get("/api/todos/?is_completed=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_search(self):
        """?search= qidirish ishlaydi."""
        Todo.objects.create(owner=self.user, title="Python o'rganish")

        response = self.client.get("/api/todos/?search=Python")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)


class RegisterTestCase(TestCase):
    """Ro'yxatdan o'tish testi."""

    def setUp(self):
        self.client = APIClient()

    def test_register_success(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "strongpass123",
            "password2": "strongpass123",
        }
        response = self.client.post("/api/auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_password_mismatch(self):
        data = {
            "username": "newuser",
            "password": "pass1",
            "password2": "pass2",
        }
        response = self.client.post("/api/auth/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
