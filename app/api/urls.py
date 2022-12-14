from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import ProductViewSet

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet)
print(router.urls)

urlpatterns = [
    path('', include(router.urls))
]