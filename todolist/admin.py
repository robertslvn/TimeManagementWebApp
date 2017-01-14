from django.contrib import admin #Import the admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from todolist.models import ExtendUser
 


# Define an inline admin descriptor to extend the base User model
class ExtendUserInline(admin.StackedInline):
    model = ExtendUser
    can_delete = False
    verbose_name_plural = 'extendUser'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ExtendUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)