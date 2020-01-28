from django.urls import path
from . import views

urlpatterns = [
    path('settings', views.settings, name='settings'),
    
    # Login Logout
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Branch
    path('branches', views.view_branches, name='branch-viewall'),
    path('change-branch', views.change_branch, name='branch-change'),

    # Course
    path('courses', views.view_courses, name='course-viewall'),

    # Calendar
    path('calendar', views.calendar, name='calendar'),

    # Student
    path('student/all', views.student, name='student-viewall'),
    path('student/add-new', views.student_add_new, name='student-add'),
    # path('student/add-new-gaurdian/<int:pk>',views.student_add_guardian,name='gaurdian-add'),
    path('student/add-guardian/<int:pk>', views.student_guardian, name='student-guardian-add'),
    path('student/add-course/<int:pk>', views.student_courses, name='student-course-add'),
    path('student/handle-payment/<int:pk>', views.student_installments, name='student-payment'),

    # Batch
    path('batch/all', views.batch_view, name='batch-viewall'),
    path('batch/add', views.batch_add, name='batch-add'),
    path('batch/edit/<int:pk>', views.batch_edit, name='batch-edit'),
]
