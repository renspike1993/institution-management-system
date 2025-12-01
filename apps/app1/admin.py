from django.contrib import admin
from .models import Folder, Department, Profile, Student
from django.contrib.auth.models import User

# ✅ Folder Admin
@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('folder_name', 'folder_capacity', 'floor_number', 'created_by', 'created_at')
    list_filter = ('floor_number',)
    search_fields = ('folder_name', 'floor_number', 'created_by__username')
    ordering = ('folder_name',)

# ✅ Department Admin
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

# ✅ Profile Admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'bio', 'avatar')
    search_fields = ('user__username', 'department__name', 'bio')
    list_filter = ('department',)

# ✅ Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'gender', 'mobile_number', 'folder', 'user')
    search_fields = ('last_name', 'first_name', 'middle_name', 'user__username', 'folder__folder_name')
    list_filter = ('gender', 'folder', 'user')
    ordering = ('last_name', 'first_name')

# Optional: If you want, you can unregister User and customize it
# admin.site.unregister(User)
# @admin.register(User)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
