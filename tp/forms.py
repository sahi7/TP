from django import forms 
from django.forms import Form
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import academicSession, Level, Department, Option, School, SchoolDept


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class tpRegisterForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Name","class":"form-control"}))
    matricule = forms.CharField(max_length=8, widget=forms.TextInput(attrs={"placeholder": "Enter your Matricule No.","class":"form-control"}))
    telephone = forms.CharField(max_length=9, widget=forms.TextInput(attrs={"placeholder": "Enter your Phone No.","class":"form-control"}))

    session_year_list = []
    department_list = []
    option_list = []
    level_list = []
    school_list = []
    school_dept_list = []

    # Displaying Academic Session years
    try:
        session_years = academicSession.objects.all()
        for session_year in session_years:
            start_year = session_year.session_start_year.strftime('%Y')
            end_year = session_year.session_end_year.strftime('%Y')
            single_session_year = (session_year.id, str(start_year)+" / "+str(end_year))
            session_year_list.append(single_session_year)
    except:
        session_year_list = []


    # Displaying the various departments
    try:
        departments = Department.objects.all()
        for department in departments:
            single_department = (department.id, department.name)
            department_list.append(single_department)
    except:
        department_list = [] 


    # Display various options
    try:
        options = Option.objects.all()
        for option in options:
            single_option = (option.id, option.name)
            option_list.append(single_option)
    except:
        option_list = []


    # Display various levels
    try:
        levels = Level.objects.all()
        for level in levels:
            single_level = (level.id, level.name)
            level_list.append(single_level)
    except:
        level_list = []


    # Display various tp schools
    try:
        schools = School.objects.all()
        for school in schools:
            single_school = (school.id, school.name)
            school_list.append(single_school)
    except:
        school_list = []


    # Display carious tp school departments
    try:
        schoolDepts = SchoolDept.objects.all()
        for schoolDept in schoolDepts:
            single_school_dept = (schoolDept.id, schoolDept.name)
            school_dept_list.append(single_school_dept)
    except:
        school_dept_list = []

        
    
    department = forms.ChoiceField(label="Department", choices=department_list, widget=forms.Select(attrs={"class":"form-control"}))
    option = forms.ChoiceField(label="Option", choices=option_list, widget=forms.Select(attrs={"class":"form-control"}))
    level = forms.ChoiceField(label="Level", choices=level_list, widget=forms.Select(attrs={"class":"form-control"}))
    school = forms.ChoiceField(label="TP School", choices=school_list, widget=forms.Select(attrs={"class":"form-control"}))
    school_dept = forms.ChoiceField(label="School Department", choices=school_dept_list, widget=forms.Select(attrs={"class":"form-control"}))

    academic_session = forms.ChoiceField(label="Academic Session", choices=session_year_list, disabled = True)




class tpUpdateForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    matricule = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Matricule No'}))
    telephone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Telephone No'}))

    session_year_list = []
    department_list = []
    option_list = []
    level_list = []
    school_list = []
    school_dept_list = []

    # Displaying Academic Session years
    try:
        session_years = academicSession.objects.all()
        for session_year in session_years:
            start_year = session_year.session_start_year.strftime('%Y')
            end_year = session_year.session_end_year.strftime('%Y')
            single_session_year = (session_year.id, str(start_year)+" / "+str(end_year))
            session_year_list.append(single_session_year)
    except:
        session_year_list = []


    # Displaying the various departments
    try:
        departments = Department.objects.all()
        for department in departments:
            single_department = (department.id, department.name)
            department_list.append(single_department)
    except:
        department_list = [] 


    # Display various options
    try:
        options = Option.objects.all()
        for option in options:
            single_option = (option.id, option.name)
            option_list.append(single_option)
    except:
        option_list = []


    # Display various levels
    try:
        levels = Level.objects.all()
        for level in levels:
            single_level = (level.id, level.name)
            level_list.append(single_level)
    except:
        level_list = []


    # Display various tp schools
    try:
        schools = School.objects.all()
        for school in schools:
            single_school = (school.id, school.name)
            school_list.append(single_school)
    except:
        school_list = []


    # Display carious tp school departments
    try:
        schoolDepts = SchoolDept.objects.all()
        for schoolDept in schoolDepts:
            single_school_dept = (schoolDept.id, schoolDept.name)
            school_dept_list.append(single_school_dept)
    except:
        school_dept_list = []

        
    
    department = forms.ChoiceField(label="Department", choices=department_list, widget=forms.Select(attrs={"class":"form-control"}))
    option = forms.ChoiceField(label="Option", choices=option_list, widget=forms.Select(attrs={"class":"form-control"}))
    level = forms.ChoiceField(label="Level", choices=level_list, widget=forms.Select(attrs={"class":"form-control"}))
    school = forms.ChoiceField(label="TP School", choices=school_list, widget=forms.Select(attrs={"class":"form-control"}))
    school_dept = forms.ChoiceField(label="School Department", choices=school_dept_list, widget=forms.Select(attrs={"class":"form-control"}))

    academic_session = forms.ChoiceField(label="Academic Session", choices=session_year_list)