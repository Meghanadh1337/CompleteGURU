from django.contrib import admin
# Register your models here.]
from django.contrib.auth.admin import UserAdmin
from .models import Topic , Post , Comment ,Event , Poll , PollOption , Resume , User


admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Event)
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(Resume)
admin.site.register(User, UserAdmin)  # Use Django's default UserAdmin


