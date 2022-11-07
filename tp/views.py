from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from .models import Student, Department, academicSession, Option, Level, School, SchoolDept, Town
import re




#1 instance = MyModel.objects.values('description')[0]
#1 description = instance['description']
#2 instance = MyModel.objects.values_list('description')[0]
#2 description = instance[0]
#description = MyModel.objects.values_list('description', flat=True)[0]

class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("admin_home") #login
    template_name = "account/signup.html"


def admin_home(request):
    all_student_count = Student.objects.all().count()
    option_count = Option.objects.all().count()
    department_count = Department.objects.all().count()
    school_count = School.objects.all().count()
    school_depts_count = SchoolDept.objects.all().count()

    # Total Option and students in Each Department
    department_all = Department.objects.all()
    department_name_list = []
    option_count_list = []
    student_count_list_in_department = []

    for department in department_all:
        options = Option.objects.filter(department_id=department.id).count()
        students = Student.objects.filter(department_id=department.id).count()
        department_name_list.append(department.code)
        option_count_list.append(options)
        student_count_list_in_department.append(students)
    
    option_all = Option.objects.all()
    option_list = []
    student_count_list_in_option = []
    for option in option_all:
        department = Department.objects.get(id=option.department_id)
        student_count = Student.objects.filter(department_id=department.id).count()
        option_list.append(option.code)
        student_count_list_in_option.append(student_count)

    student_name_list=[]
    students = Student.objects.all()
    for student in students:
        student_name_list.append(student.name)
    



    context = {
        "all_student_count": all_student_count,
        "option_count": option_count,
        "department_count": department_count,
        "school_count": school_count,
        "school_depts_count": school_depts_count,
        "department_name_list": department_name_list,
        "option_count_list": option_count_list,
        "student_count_list_in_department": student_count_list_in_department,
        "option_list": option_list,
        "student_count_list_in_option": student_count_list_in_option,
        "student_name_list": student_name_list,
    }
    return render(request, "tp_admin/home_content.html", context)


def add_department(request):
    levels = Level.objects.all()
    context = {
        "levels":levels
    }
    return render(request, "tp_admin/add_department.html", context)


def add_department_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_department')
    else:
        department = request.POST.get('department')
        department_code = request.POST.get('code')
        department_level = request.POST.get('level')
        try:
            department_model = Department(name=department, code=department_code, level_id=department_level)
            department_model.save()
            messages.success(request, "Department Added Successfully!")
            return redirect('add_department')
        except:
            messages.error(request, "Failed to Add Department!")
            return redirect('add_department')


def manage_department(request):
    departments = Department.objects.all()
    context = {
        "departments": departments
    }
    return render(request, 'tp_admin/manage_department.html', context)


def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)
    levels = Level.objects.all()
    context = {
        "department": department,
        "id": department_id,
        "levels":levels
    }
    return render(request, 'tp_admin/edit_department.html', context)


def edit_department_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('department')
        department_code = request.POST.get('code')
        department_level = request.POST.get('level')

        try:
            department = Department.objects.get(id=department_id)
            department.name = department_name
            department.code = department_code
            department.level_id = department_level
            department.save()

            messages.success(request, "Department Updated Successfully.")
            return redirect('/edit_department/'+department_id)

        except:
            messages.error(request, "Failed to Update Department.")
            return redirect('/edit_department/'+department_id)


def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    try:
        department.delete()
        messages.success(request, "Department Deleted Successfully.")
        return redirect('manage_department')
    except:
        messages.error(request, "Failed to Delete Department.")
        return redirect('manage_department')


def add_student(request):
    departments = Department.objects.all()
    options = Option.objects.all()
    levels = Level.objects.all()
    schools = School.objects.all()
    school_depts = SchoolDept.objects.all()
    academic_sessions = academicSession.objects.all()

    context = {
        "departments":departments,
        "options":options,
        "levels":levels,
        "schools":schools,
        "school_depts":school_depts,
        "academic_sessions":academic_sessions,
    }
    return render(request, 'home.html', context)




def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_option')
    else:
        name = request.POST.get('name')
        matricule = request.POST.get('matricule')
        telephone = request.POST.get('telephone')
        level_id = request.POST.get('level')
        department_id = request.POST.get('department')
        option_id = request.POST.get('option')
        tp_school_id = request.POST.get('school')
        tp_school_dept_id = request.POST.get('school_dept')
        academic_session_id = request.POST.get('academic_session')
            
        # Then Update Students Table
        try:
            student_data = Student(name=name, matricule=matricule, telephone=telephone, department_id=department_id, option_id=option_id, 
                level_id=level_id, school_id=tp_school_id, school_dept_id=tp_school_dept_id, academic_session_id=academic_session_id)
            student_data.save()

            # Get the current School id and decrement the num_of_sudent
            get_school = School.objects.get(id=tp_school_id)
            num_of_sudent = get_school.num_of_sudent
            student_count = num_of_sudent - 1

            student, created = School.objects.update_or_create(
            id=tp_school_id,
            defaults={"num_of_sudent":student_count}
            )

            student_id = Student.objects.get(id=student_data.id)

            messages.success(request, "You have been Registered Successfully!")

            return render(request, 'pdf/studentpdf.html', {"student":student_id})
            #return HttpResponseRedirect(reverse("gen_student_pdf"))
        except:
            messages.error(request, "Failed to Register Student.")
            return HttpResponseRedirect(reverse("home"))



def manage_student(request):
    students = Student.objects.all()
    context = {
        "students": students
    }
    return render(request, 'tp_admin/manage_student.html', context)


def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)
    departments = Department.objects.all()
    options = Option.objects.all()
    levels = Level.objects.all()
    schools = School.objects.all()
    school_depts = SchoolDept.objects.all()
    academic_sessions = academicSession.objects.all()

    context = {
        "student": student,
        "departments":departments,
        "options":options,
        "levels":levels,
        "schools":schools,
        "school_depts":school_depts,
        "academic_sessions":academic_sessions
        }
    return render(request, "tp_admin/edit_student.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('name')
        student_matricule = request.POST.get('matricule')
        student_telephone = request.POST.get('telephone')
        level_id = request.POST.get('level')
        department_id = request.POST.get('department')
        option_id = request.POST.get('option')
        tp_school_id = request.POST.get('school')
        tp_school_dept_id = request.POST.get('school_dept')

        # Then Update Students Table
        try:
            student = Student.objects.get(id=student_id)
            student.name = student_name
            student.matricule = student_matricule
            student.telephone = student_telephone

            department = Department.objects.get(id=department_id)
            student.department_id = department

            option = Option.objects.get(id=option_id)
            student.option_id = option

            level = Level.objects.get(id=level_id)
            student.level_id = level

            tp_school = School.objects.get(id=tp_school_id)
            student.school_id = tp_school

            
            student.school_dept_id = tp_school_dept_id

            student.save()
            messages.success(request, "Student Updated Successfully.")
            return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id":student_id}))

        except:
            messages.error(request, "Failed to Update Student.")
            return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id":student_id}))
            


def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


@csrf_exempt
def check_matricule_exist(request):
    matricule = request.POST.get("matricule").upper()
    mat_obj = Student.objects.filter(matricule=matricule).exists()
    if mat_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt    
def validate_telephone(request):
    telephone = request.POST.get("telephone")
    rule = re.compile("[6-7][0-9]{8}")
    #rule = True
    if rule.match(telephone):
        return HttpResponse(True)
    else:
        return HttpResponse(False)



# View for Option
def add_option(request):
    departments = Department.objects.all()
    context = {
        "departments": departments,
    }
    return render(request, 'tp_admin/add_option.html', context)



def add_option_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_option')
    else:
        option_name = request.POST.get('option')
        option_code = request.POST.get('code')

        department_id = request.POST.get('department')
        #department = Department.objects.get(id=department_id)
        

        try:
            option = Option(name=option_name, code=option_code, department_id=department_id)
            option.save()
            messages.success(request, "Option Added Successfully!")
            return redirect('add_option')
        except:
            messages.error(request, "Failed to Add Option!")
            return redirect('add_option')


def manage_option(request):
    options = Option.objects.all()
    departments = Department.objects.all()
    context = {
        "options": options,
        "departments": departments
    }
    return render(request, 'tp_admin/manage_option.html', context)


def edit_option(request, option_id):
    option = Option.objects.get(id=option_id)
    departments = Department.objects.all()
    context = {
        "option": option,
        "departments": departments,
        "id": option_id
    }
    return render(request, 'tp_admin/edit_option.html', context)


def edit_option_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        option_id = request.POST.get('option_id')
        option_name = request.POST.get('option')
        option_code = request.POST.get('code')
        department_id = request.POST.get('department')

        try:
            option = Option.objects.get(id=option_id)
            option.name = option_name
            option.code = option_code

            department = Department.objects.get(id=department_id)
            option.department_id = department
            
            option.save()

            messages.success(request, "Option Updated Successfully.")
            # return redirect('/edit_option/'+option_id)
            return HttpResponseRedirect(reverse("edit_option", kwargs={"option_id":option_id}))

        except:
            messages.error(request, "Failed to Update Option.")
            return HttpResponseRedirect(reverse("edit_option", kwargs={"option_id":option_id}))
            # return redirect('/edit_option/'+option_id)



def delete_option(request, option_id):
    option = Option.objects.get(id=option_id)
    try:
        option.delete()
        messages.success(request, "Option Deleted Successfully.")
        return redirect('manage_option')
    except:
        messages.error(request, "Failed to Delete Option.")
        return redirect('manage_option')

# View for academic session
def manage_session(request):
    session_years = academicSession.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "tp_admin/manage_session.html", context)


def add_session(request):
    return render(request, "tp_admin/add_session.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('manage_session')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = academicSession(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Academic session added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Academic session")
            return redirect("add_session")


def edit_session(request, session_id):
    session_year = academicSession.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "tp_admin/edit_session.html", context)


def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = academicSession.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Academic session Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Academic session.")
            return redirect('/edit_session/'+session_id)


def delete_session(request, session_id):
    session = academicSession.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')


# View for Town
def add_town(request):
    towns = Town.objects.all()
    context = {
        "towns": towns,
    }
    return render(request, 'tp_admin/add_town.html', context)



def add_town_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_town')
    else:
        town_name = request.POST.get('town')
        
        try:
            town = Town(name=town_name)
            town.save()
            messages.success(request, "Town Added Successfully!")
            return redirect('add_town')
        except:
            messages.error(request, "Failed to Add Town!")
            return redirect('add_town')


def manage_town(request):
    towns = Town.objects.all()
    context = {
        "towns": towns,
    }
    return render(request, 'tp_admin/manage_town.html', context)


def edit_town(request, town_id):
    town = Town.objects.get(id=town_id)
    context = {
        "town": town,
        "id": town_id
    }
    return render(request, 'tp_admin/edit_town.html', context)


def edit_town_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        town_id = request.POST.get('town_id')
        town_name = request.POST.get('town')

        try:
            town = Town.objects.get(id=town_id)
            town.name = town_name
            
            town.save()

            messages.success(request, "Town Updated Successfully.")
            # return redirect('/edit_town/'+town_id)
            return HttpResponseRedirect(reverse("edit_town", kwargs={"town_id":town_id}))

        except:
            messages.error(request, "Failed to Update Town.")
            return HttpResponseRedirect(reverse("edit_town", kwargs={"town_id":town_id}))
            # return redirect('/edit_town/'+town_id)



def delete_town(request, town_id):
    town = Town.objects.get(id=town_id)
    try:
        town.delete()
        messages.success(request, "Town Deleted Successfully.")
        return redirect('manage_town')
    except:
        messages.error(request, "Failed to Delete Town.")
        return redirect('manage_town')


# View for School
def add_school(request):
    towns = Town.objects.all()
    context = {
        "towns": towns,
    }
    return render(request, 'tp_admin/add_school.html', context)



def add_school_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_school')
    else:
        school_name = request.POST.get('school')
        num_of_sudent = request.POST.get('num_of_sudent')

        town_id = request.POST.get('town')
        #town = Town.objects.get(id=town_id)
        

        try:
            school = School(name=school_name, num_of_sudent=num_of_sudent, town_id=town_id)
            school.save()
            messages.success(request, "School Added Successfully!")
            return redirect('add_school')
        except:
            messages.error(request, "Failed to Add School!")
            return redirect('add_school')


def manage_school(request):
    schools = School.objects.all()
    towns = Town.objects.all()
    context = {
        "schools": schools,
        "towns": towns,
    }
    return render(request, 'tp_admin/manage_school.html', context)


def edit_school(request, school_id):
    school = School.objects.get(id=school_id)
    towns = Town.objects.all()
    context = {
        "school": school,
        "towns": towns,
        "id": school_id
    }
    return render(request, 'tp_admin/edit_school.html', context)


def edit_school_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        school_id = request.POST.get('school_id')
        school_name = request.POST.get('school')
        num_of_sudent = request.POST.get('num_of_sudent')
        town_id = request.POST.get('town')

        try:
            school = School.objects.get(id=school_id)
            school.name = school_name
            school.num_of_sudent = num_of_sudent

            town = Town.objects.get(id=town_id)
            school.town_id = town
            
            school.save()

            messages.success(request, "School Updated Successfully.")
            # return redirect('/edit_school/'+school_id)
            return HttpResponseRedirect(reverse("edit_school", kwargs={"school_id":school_id}))

        except:
            messages.error(request, "Failed to Update School.")
            return HttpResponseRedirect(reverse("edit_school", kwargs={"school_id":school_id}))
            # return redirect('/edit_school/'+school_id)



def delete_school(request, school_id):
    school = School.objects.get(id=school_id)
    try:
        school.delete()
        messages.success(request, "School Deleted Successfully.")
        return redirect('manage_school')
    except:
        messages.error(request, "Failed to Delete School.")
        return redirect('manage_school')


# View for TP School Department
def add_school_dept(request):
    schools = School.objects.all()
    context = {
        "schools": schools,
    }
    return render(request, 'tp_admin/add_school_dept.html', context)



def add_school_dept_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_school_dept')
    else:
        school_dept_name = request.POST.get('school_dept')

        school_id = request.POST.get('school')

        try:
            school_dept = SchoolDept(name=school_dept_name, school_id=school_id)
            school_dept.save()
            messages.success(request, "TP School Department Successfully!")
            return redirect('add_school_dept')
        except:
            messages.error(request, "Failed to Add TP School Department!")
            return redirect('add_school_dept')


def manage_school_dept(request):
    school_depts = SchoolDept.objects.all()
    schools = School.objects.all()
    context = {
        "school_depts": school_depts,
        "schools": schools
    }
    return render(request, 'tp_admin/manage_school_dept.html', context)


def edit_school_dept(request, school_dept_id):
    school_dept = SchoolDept.objects.get(id=school_dept_id)
    schools = School.objects.all()
    context = {
        "school_dept": school_dept,
        "schools": schools,
        "id": school_dept_id
    }
    return render(request, 'tp_admin/edit_school_dept.html', context)


def edit_school_dept_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        school_dept_id = request.POST.get('school_dept_id')
        school_dept_name = request.POST.get('school_dept')
        school_id = request.POST.get('school')

        try:
            school_dept = SchoolDept.objects.get(id=school_dept_id)
            school_dept.name = school_dept_name

            school = School.objects.get(id=school_id)
            school_dept.school_id = school
            
            school_dept.save()

            messages.success(request, "TP School Department Updated Successfully.")
            # return redirect('/edit_school_dept/'+school_dept_id)
            return HttpResponseRedirect(reverse("edit_school_dept", kwargs={"school_dept_id":school_dept_id}))

        except:
            messages.error(request, "Failed to Update TP School Department.")
            return HttpResponseRedirect(reverse("edit_school_dept", kwargs={"school_dept_id":school_dept_id}))
            # return redirect('/edit_school_dept/'+school_dept_id)



def delete_school_dept(request, school_dept_id):
    school_dept = SchoolDept.objects.get(id=school_dept_id)
    try:
        school_dept.delete()
        messages.success(request, "TP School Department Deleted Successfully.")
        return redirect('manage_school_dept')
    except:
        messages.error(request, "Failed to Delete TP School Department.")
        return redirect('manage_school_dept')



def admin_profile(request):
    try:
        user = get_user_model().objects.get(id=request.user.id)

        context={
            "user": user
        }
        return render(request, 'tp_admin/admin_profile.html', context)
    except:
        return redirect('account_login')


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user1 = get_user_model().objects.get(id=request.user.id)
        print("First name:", first_name, "\n", "last name:", last_name, "Username:", username, "\n", "password:", password)

        try:
            user = get_user_model().objects.get(id=request.user.id)
            
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            if password != None and password != "":
                user.set_password(password)
            user.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')




