from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
	fields = ('email','created_at','first_name','last_name','middle_name','phone','username','is_staff','is_active','facebook_id','profile_image','gender')
	list_display = ('first_name', 'last_name', 'email', 'created_at')
	read_only_fields = ['facebook_id']


admin.site.register(User, UserAdmin)