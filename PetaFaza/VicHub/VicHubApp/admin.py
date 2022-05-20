from django.contrib import admin

# Register your models here.
from VicHubApp.models import *

admin.site.register(User)
admin.site.register(BelongsTo)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Request)
admin.site.register(Joke)
admin.site.register(Grade)