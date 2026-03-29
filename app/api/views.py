from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .models import Todo
from .serializers import TodoSerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Yangi foydalanuvchi yaratish. Hech qanday autentifikatsiya shart emas.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    """
    GET /api/auth/me/
    Hozirgi foydalanuvchi ma'lumotlarini qaytaradi.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class TodoViewSet(viewsets.ModelViewSet):
    """
    Barcha CRUD operatsiyalari:
      GET    /api/todos/        - ro'yxat
      POST   /api/todos/        - yangi yaratish
      GET    /api/todos/{id}/   - bitta olish
      PUT    /api/todos/{id}/   - to'liq yangilash
      PATCH  /api/todos/{id}/   - qisman yangilash
      DELETE /api/todos/{id}/   - o'chirish

    Qo'shimcha endpoint:
      POST   /api/todos/{id}/toggle/ - bajarildi/bajarilmadi almashish
    """

    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Filterlash va qidirish
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_completed", "priority"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "due_date", "priority"]

    def get_queryset(self):
        """Faqat o'z todolarini ko'radi."""
        return Todo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Yaratayotganda owner avtomatik qo'shiladi."""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"], url_path="toggle")
    def toggle_complete(self, request, pk=None):
        """
        POST /api/todos/{id}/toggle/
        Todonikni is_completed ni teskari qiladi.
        """
        todo = self.get_object()
        todo.is_completed = not todo.is_completed
        todo.save()
        return Response(
            {"id": todo.id, "is_completed": todo.is_completed},
            status=status.HTTP_200_OK,
        )
