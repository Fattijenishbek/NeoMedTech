"""medtech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_url
from patches import routers
from checklist.urls import checklist_router
from schedule.urls import schedule_router
from handbook.urls import handbook_router
from users.urls import user_router
router = routers.DefaultRouter()

router.extend(checklist_router)
router.extend(schedule_router)
router.extend(handbook_router)
router.extend(user_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('api/', include(router.urls))
]

urlpatterns += doc_url