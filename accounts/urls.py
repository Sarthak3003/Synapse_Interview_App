from .views import LoginAPI,RegisterApi,PositionApi,SlotbookApi
from django.urls import path
from . import views
urlpatterns = [
    path('api/register/', RegisterApi.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/position/',PositionApi.as_view(), name='position'),
    path('api/login/', SlotbookApi.as_view(), name='slotbook'),
    #path('signUp/', views.signUp, name="signup"),
    # path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    # path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]