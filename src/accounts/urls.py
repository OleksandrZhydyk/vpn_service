from django.urls import path

from accounts.views import LoginUser, LogoutUser, RegisterUser, ProfileUpdateView, ProfileView

urlpatterns = [
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="user_profile"),
    path("profile/update/<int:pk>/", ProfileUpdateView.as_view(), name="update_user_profile"),
]
