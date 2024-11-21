from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, CustomLoginView, admin_dashboard, worker_dashboard

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('worker/dashboard/', worker_dashboard, name='worker_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
