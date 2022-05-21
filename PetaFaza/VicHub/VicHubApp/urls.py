from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('login/', login_req, name='login'),
    path('logout/', logout_req, name='logout'),  # vukasin007
    path('register/', register_req, name='register'),
    path('all_categories/', all_categories, name='all_categories'),
    # path('register_admin/', register_admin_req, name='register_admin'),
    # path('delete_user_admin/<int:user_id>', register_admin_req, name='register_admin'),# moze li preko setItem i getItem
    # path('profile/', profile, name='profile'),

    # path('joke/<int:joke_id>', joke, name='joke'), #comi
    # path('add_joke/', add_joke, name='add_joke'), #comi
    # path('delete_joke/<int:joke_id>', delete_joke, name='delete_joke'),

    # path('category/<int:category_id>', category_req, name='category'), #comi
    # path('add_category/', add_category_req, name='add_category'),

    # path('add_comment/', add_comment, name='add_comment'),
    # path('delete_comment/<int:comment_id>', delete_comment, name='delete_comment'),

    # path('accept_joke/<int:joke_id>', accept_joke, name='accept_joke'),
    # path('reject_joke/<int:joke_id>', reject_joke, name='reject_joke'),

    # path('grade_joke/<int:joke_id>/<int:grade>', grade_joke, name='grade_joke'),

    # url,      view,       url_name
    path('subscribe_to_bilten/', subscribe_to_bilten, name='subscribe_to_bilten'),  # vukasin007
    path('unsubscribe_from_bilten/', unsubscribe_from_bilten, name='unsubscribe_from_bilten'),  # vukasin007

    path('request_mod/', request_mod, name='request_mod'),  # vukasin007
    path('accept_mod_request/<int:request_id>', accept_mod_request, name='accept_mod_request'),  # vukasin007
    path('reject_mod_request/<int:request_id>', reject_mod_request, name='reject_mod_request'),  # vukasin007

    # path('change_personal_data/', change_personal_data, name='change_personal_data'),  # vukasin007
    path('remove_mod/<int:user_id>', remove_mod, name='remove_mod'),  # vukasin007
]
