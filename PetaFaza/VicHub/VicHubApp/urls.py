from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    # path('login/', login_req, name='login'),
    # path('logout/', logout_req, name='logout'),
    # path('profile/<int:user_id>', profile_req, name='profile'),
    # path('addjoke/', add_joke, name='add_joke'),

]
