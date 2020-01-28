from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

# Rsquare User
class RsquareAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('role', 'branch')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'branch', 'phone_no', 'gender')}),
    )
    add_fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'branch', 'phone_no', 'gender')}),
    )
    pass
admin.site.register(models.RsquareUser, RsquareAdmin)
admin.site.register(models.StudentProfile)
admin.site.register(models.Guardian)

# Branch
admin.site.register(models.Branch)

# Subject and Course
admin.site.register(models.SubjectGroup)
admin.site.register(models.Subject)
admin.site.register(models.Course)
admin.site.register(models.CourseSubject)

# Batch
admin.site.register(models.Batch)

#Course registration and stuff
admin.site.register(models.StudentCourse)
admin.site.register(models.CourseTaken)
admin.site.register(models.ExtraFee)