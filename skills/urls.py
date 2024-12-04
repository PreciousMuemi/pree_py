from django.urls import path
from .views import SkillSwapLoginView, SkillSwapLogoutView, UserRegistrationView, ProfileCompletionView, match_skills

urlpatterns = [
    path('login/', SkillSwapLoginView.as_view(), name='login'),
    path('logout/', SkillSwapLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/complete/', ProfileCompletionView.as_view(), name='profile_complete'),
    path('match/', match_skills, name='match_skills'),
]