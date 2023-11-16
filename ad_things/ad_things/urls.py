from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bulletin_board/', include('bulletin_board.urls')),
]
