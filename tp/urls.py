#tp/urls.py
from django.urls import path
from django.urls import re_path as url

from wkhtmltopdf.views import PDFTemplateView

from . import views
from . import pdfviews
from .views import SignupPageView


urlpatterns = [
	#path("", HomePageView.as_view(), name="home"),
	path("signup/", SignupPageView.as_view(), name="signup"),

	path('', views.add_student, name="home"),
	path('add_student/', views.add_student, name="add_student"),
    path('add_student_save/', views.add_student_save, name="add_student_save"),
    path('check_matricule_exist/', views.check_matricule_exist, name="check_matricule_exist"),
    path('validate_telephone/', views.validate_telephone, name="validate_telephone"),

	path('edit_student/<student_id>', views.edit_student, name="edit_student"),
    path('edit_student_save/', views.edit_student_save, name="edit_student_save"),
    path('manage_student/', views.manage_student, name="manage_student"),
    path('delete_student/<student_id>/', views.delete_student, name="delete_student"),

    path('add_department/', views.add_department, name="add_department"),
    path('add_department_save/', views.add_department_save, name="add_department_save"),
    path('manage_department/', views.manage_department, name="manage_department"),
    path('edit_department/<department_id>/', views.edit_department, name="edit_department"),
    path('edit_department_save/', views.edit_department_save, name="edit_department_save"),
    path('delete_department/<department_id>/', views.delete_department, name="delete_department"),

    path('add_option/', views.add_option, name="add_option"),
    path('add_option_save/', views.add_option_save, name="add_option_save"),
    path('manage_option/', views.manage_option, name="manage_option"),
    path('edit_option/<option_id>/', views.edit_option, name="edit_option"),
    path('edit_option_save/', views.edit_option_save, name="edit_option_save"),
    path('delete_option/<option_id>/', views.delete_option, name="delete_option"),
    
    path('manage_session/', views.manage_session, name="manage_session"),
    path('add_session/', views.add_session, name="add_session"),
    path('add_session_save/', views.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', views.edit_session, name="edit_session"),
    path('edit_session_save/', views.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', views.delete_session, name="delete_session"),

    path('add_town/', views.add_town, name="add_town"),
    path('add_town_save/', views.add_town_save, name="add_town_save"),
    path('manage_town/', views.manage_town, name="manage_town"),
    path('edit_town/<town_id>/', views.edit_town, name="edit_town"),
    path('edit_town_save/', views.edit_town_save, name="edit_town_save"),
    path('delete_town/<town_id>/', views.delete_town, name="delete_town"),

    path('manage_school/', views.manage_school, name="manage_school"),
    path('add_school/', views.add_school, name="add_school"),
    path('add_school_save/', views.add_school_save, name="add_school_save"),
    path('edit_school/<school_id>', views.edit_school, name="edit_school"),
    path('edit_school_save/', views.edit_school_save, name="edit_school_save"),
    path('delete_school/<school_id>/', views.delete_school, name="delete_school"),

    path('add_school_dept/', views.add_school_dept, name="add_school_dept"),
    path('add_school_dept_save/', views.add_school_dept_save, name="add_school_dept_save"),
    path('manage_school_dept/', views.manage_school_dept, name="manage_school_dept"),
    path('edit_school_dept/<school_dept_id>/', views.edit_school_dept, name="edit_school_dept"),
    path('edit_school_dept_save/', views.edit_school_dept_save, name="edit_school_dept_save"),
    path('delete_school_dept/<school_dept_id>/', views.delete_school_dept, name="delete_school_dept"),
    
    path('admin_home/', views.admin_home, name="admin_home"),
    path('admin_profile/', views.admin_profile, name="admin_profile"),
    path('admin_profile_update/', views.admin_profile_update, name="admin_profile_update"),

    path('student_pdf_generate/(?P<student_id>.*)/$', pdfviews.student_pdf_generate, name="student_pdf_generate"),
    path('student/', pdfviews.student, name="student")

]