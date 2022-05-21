from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('register/', register_req, name='register'),
    # path('register_admin/', register_admin_req, name='register_admin'),
    path('login/', login_req, name='login'),
    path('logout/', logout_req, name='logout'),
    # path('delete_user_admin/<int:user_id>', register_admin_req, name='register_admin'),# moze li preko setItem i getItem
    # path('profile/', profile, name='profile'),

    # path('joke/<int:joke_id>', joke, name='joke'),
    # path('add_joke/', add_joke, name='add_joke'),
    # path('delete_joke/<int:joke_id>', delete_joke, name='delete_joke'),

    # path('category/<int:category_id>', category_req, name='category'),
    # path('add_category/', add_category_req, name='add_category'),

    # path('add_comment/', add_comment, name='add_comment'),
    # path('delete_comment/<int:comment_id>', delete_comment, name='delete_comment'),

    # path('accept_joke/<int:joke_id>', accept_joke, name='accept_joke'),
    # path('reject_joke/<int:joke_id>', reject_joke, name='reject_joke'),

    # path('grade_joke/<int:joke_id>/<int:grade>', grade_joke, name='grade_joke'),

    # path('subscribe_to_bilten/', subscribe_to_bilten, name='subscribe_to_bilten'),
    # path('unsubscribe_from_bilten/', unsubscribe_from_bilten, name='unsubscribe_from_bilten'),

    # path('request_mod/', request_mod, name='request_mod'),
    # path('accept_mod_request/<int:request_id>', accept_mod_request, name='accept_mod_request'),
    # path('reject_mod_request/<int:request_id>', reject_mod_request, name='reject_mod_request'),

    # path('change_personal_data/', change_personal_data, name='change_personal_data'),
    # path('remove_mod/<int:user_id>', remove_mod, name='remove_mod'),
]
