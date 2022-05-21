from django.contrib import admin

from .models import *


admin.site.register(User)
admin.site.register(BelongsTo)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Request)
admin.site.register(Joke)
admin.site.register(Grade)
