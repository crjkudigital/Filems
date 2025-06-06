from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    path('profile/create/', UserProfileCreateView.as_view(), name='profile-create'),
    path('profile/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('profile/delete/', UserProfileDeleteView.as_view(), name='profile-delete'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]