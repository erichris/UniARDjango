from django.contrib import admin
from .models import UniAR, Profile

#admin.site.register(UniAR)
#admin.site.register(Profile)

# Register your models here.

@admin.register(UniAR)
class UniARAdmin(admin.ModelAdmin):
    list_display = ['children_display', 'name', 'image', 'fileSize']
    
    def children_display(self, obj):
        return ("%s" % (obj.owner.user.username)).upper()
    children_display.short_description = "User"
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'userType', 'image', 'unisAmount']

    def custom_field(self, obj):
        return format_html('<a href={}>URL</a>', obj.url)


admin.site.site_header = 'Panel de control Uniars'