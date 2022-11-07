from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Student, Level, School, SchoolDept, Option,  academicSession, Town, Department
from .forms import CustomUserCreationForm, CustomUserChangeForm

admin.site.register(Student)
admin.site.register(Level)
admin.site.register(School)
admin.site.register(SchoolDept)
admin.site.register(Option)
admin.site.register(academicSession)
admin.site.register(Town)
admin.site.register(Department)

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = [
		"email",
		"username",
		"is_superuser",
	]
