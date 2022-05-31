from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('login/', login_req, name='login'),
    path('logout/', logout_req, name='logout'),  # vukasin007
    path('register/', register_req, name='register'),
    path('all_categories/', all_categories, name='all_categories'),
    path('register_admin/', register_admin_req, name='register_admin'),
    path('admin_all_users/', admin_all_users, name='admin_all_users'),
    path('delete_user_admin/<int:user_id>', delete_user_admin, name='delete_user_admin'),
    path('profile/', profile, name='profile'),

    path('joke/<int:joke_id>', joke, name='joke'),  # comi
    path('add_joke/', add_joke, name='add_joke'),  # comi
    path('delete_joke/<int:joke_id>', delete_joke, name='delete_joke'),

    path('category/<int:category_id>', category_req, name='category'),  # comi
    path('add_category/', add_category_req, name='add_category'),  # vukasin007

    path('add_comment/<int:joke_id>', add_comment, name='add_comment'),  # comi
    path('delete_comment/<int:comment_id>', delete_comment, name='delete_comment'),  # vukasin007

    path('pending_jokes/', pending_jokes, name='pending_jokes'),  # vukasin007
    path('choose_category/<int:joke_id>', choose_category, name='choose_category'),  # vukasin007
    path('accept_joke/<int:joke_id>', accept_joke, name='accept_joke'),  # vukasin007 #/<int:category_id>
    path('reject_joke/<int:joke_id>', reject_joke, name='reject_joke'),  # vukasin007

    path('grade_joke/<int:joke_id>', grade_joke, name='grade_joke'),  # vukasin007

    path('subscribe_to_bilten/', subscribe_to_bilten, name='subscribe_to_bilten'),  # vukasin007
    path('unsubscribe_from_bilten/', unsubscribe_from_bilten, name='unsubscribe_from_bilten'),  # vukasin007

    path('request_mod/', request_mod, name='request_mod'),  # vukasin007
    path('all_requests_mod/', all_requests_mod, name='all_requests_mod'),  # vukasin007
    path('accept_mod_request/<int:request_id>', accept_mod_request, name='accept_mod_request'),  # vukasin007
    path('reject_mod_request/<int:request_id>', reject_mod_request, name='reject_mod_request'),  # vukasin007

    path('change_personal_data/', change_personal_data, name='change_personal_data'),  # vukasin007

    path('remove_mod/<int:user_id>', remove_mod, name='remove_mod'),  # vukasin007

    # ! NOTE: Za neke od viewova false stranice, potrebno promeniti kada se dodaju.
]
