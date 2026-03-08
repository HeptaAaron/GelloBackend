"""
URL configuration for DjangoBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from DjangoBackend.views.auth_views import LoginView, RegisterView, LogoutView, UserDataView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from DjangoBackend.views.entry_views import EntryCreateView, EntryListView, EntryReadView, EntryUpdateView, \
    EntryDeleteView
from DjangoBackend.views.project_views import ProjectCreateView, ProjectListView, ProjectReadView, ProjectUpdateView, \
    ProjectDeleteView

from DjangoBackend.views.gel_views import GelAnalyzeView

urlpatterns = [
    # user
    path('api/auth/login', LoginView.as_view(), name='auth-login'),
    path('api/auth/refresh', TokenRefreshView.as_view(), name='auth-refresh'),
    path('api/auth/register', RegisterView.as_view(), name='auth-register'),
    path('api/auth/logout', LogoutView.as_view(), name='auth-logout'),
    path('api/auth/user', UserDataView.as_view(), name='user-data'),

    # project
    path('api/project/create', ProjectCreateView.as_view(), name='project-create'),
    path('api/project', ProjectListView.as_view(), name='project-list'),
    path('api/project/read/<int:id>', ProjectReadView.as_view(), name='project-read'),
    path('api/project/update/<int:id>', ProjectUpdateView.as_view(), name='project-update'),
    path('api/project/delete/<int:id>', ProjectDeleteView.as_view(), name='project-delete'),

    # entry
    path('api/project/<int:project_id>/create', EntryCreateView.as_view(), name='entry-create'),
    path('api/project/<int:project_id>/', EntryListView.as_view(), name='entry-list'),
    path('api/project/<int:project_id>/read/<int:entry_id>', EntryReadView.as_view(), name='entry-read'),
    path('api/project/<int:project_id>/update/<int:entry_id>', EntryUpdateView.as_view(), name='entry-update'),
    path('api/project/<int:project_id>/delete/<int:entry_id>', EntryDeleteView.as_view(), name='entry-delete'),

    # gel image
    path('api/gel/', GelAnalyzeView.as_view(), name='gel-analyze')
]
