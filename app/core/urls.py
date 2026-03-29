from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api.views import TodoViewSet, RegisterView, MeView

# Router avtomatik URL larni yaratadi:
#   /api/todos/         -> list, create
#   /api/todos/{id}/    -> retrieve, update, destroy
#   /api/todos/{id}/toggle/ -> toggle_complete
router = DefaultRouter()
router.register(r"todos", TodoViewSet, basename="todo")

urlpatterns = [
    path("admin/", admin.site.urls),
    # DRF built-in login/logout (browser uchun)
    path("api/auth/", include("rest_framework.urls")),
    # Custom auth
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/me/", MeView.as_view(), name="me"),
    # Asosiy API
    path("api/", include(router.urls)),
]
