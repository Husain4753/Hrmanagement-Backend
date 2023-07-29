from django.contrib import admin
from .models import User,Leave,Resume,Announcement
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class UserModelAdmin(BaseUserAdmin):
    list_display = ('id','username','email' ,'contact', 'profile_image','department','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email','contact','profile_image')}),
        ('Permissions', {'fields': ('is_admin','department')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email' ,'contact','profile_image','department', 'password1', 'password2'),
        }), 
    )
    search_fields = ('username','email')
    ordering = ('username','id')
    filter_horizontal = ()

admin.site.register(User, UserModelAdmin)
@admin.register(Leave)
class LeaaveAdmin(admin.ModelAdmin):
    list_display=['id','user','date_from','date_to','status','reason','remarks','app_date']

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display=['unique_id','name','email','dob','address','gender','pimage','rdocs','created_by']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display=['id','user','announcement','date']