from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Guardian,StudentProfile,RsquareUser
from . import models


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    messages = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_owner():
                request.session["curr_branch"] = models.Branch.objects.all()[0].name
            elif user.is_branch_manager():
                request.session['curr_branch'] = request.user.branch.name
            return redirect('dashboard')
        messages['alert'] = 'Failed to authenticate!'
    return render(request, 'login/login.html', {'messages': messages})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def change_branch(request):
    if request.method == 'POST':
        branch_name = request.POST['branch']
        request.session["curr_branch"] = branch_name
        print(request.session['curr_branch'])
        return redirect('dashboard')
    else:
        return redirect('dashboard')


@login_required
def view_branches(request):
    branches = models.Branch.objects.all()
    return render(request, 'branch/branch_viewall.html', {'branches': branches})


@login_required
def view_courses(request):
    courses = models.Course.objects.filter(branch__name=request.session['curr_branch'])
    if not (request.user.is_owner() or request.user.is_branch_manager()):
        return redirect('dashboard')
    subject_groups = models.SubjectGroup.objects.all()
    if request.method == 'GET':
        return render(request, 'course/course_viewall.html', {
            'courses': courses,
            'subject_groups': subject_groups
        })
    else:
        name = request.POST['name']
        fee = request.POST['fee']
        duration = request.POST['duration']
        duration_type = request.POST['duration_type']
        no_of_installments = request.POST['no_of_installments']
        installments_duration_type = request.POST['installments_duration_type']
        days_between_two_installments = request.POST['days_between_two_installments']
        if  request.user.is_owner():
            add_to_all = request.POST['add_to_all'];
            if add_to_all=='true':
                for branch in models.Branch.objects.all():
                    course = models.Course.objects.create(name=name, fee=fee,
                    duration=duration, no_of_installments=no_of_installments,
                    days_between_two_installments=days_between_two_installments,
                    duration_type=duration_type, installment_duration_type=installment_duration_type,
                    branch=branch)
                    for subject_id in request.POST.getlist('subjects[]'):
                        courseSubject = models.CourseSubject.objects.create(course=course, subject_id=subject_id)
            else:
                course = models.Course.objects.create(name=name, fee=fee,
                duration=duration, no_of_installments=no_of_installments,
                days_between_two_installments=days_between_two_installments,
                duration_type=duration_type, installment_duration_type=installment_duration_type,
                branch=models.Branch.objects.get(name=request.session['curr_branch']))
                for subject_id in request.POST.getlist('subjects[]'):
                    courseSubject = models.CourseSubject.objects.create(course=course, subject_id=subject_id)
        elif request.user.is_branch_manager():
            course = models.Course.objects.create(name=name, fee=fee, duration=duration, no_of_installments=no_of_installments, days_between_two_installments=days_between_two_installments, branch=request.user.branch
            , duration_type=duration_type, installment_duration_type=installment_duration_type)
            for subject_id in request.POST.getlist('subjects[]'):
                courseSubject = models.CourseSubject.objects.create(course=course, subject_id=subject_id)
        
        return redirect('course-viewall')

@login_required
def calendar(request):
    return render(request, 'calendar/calendar.html')


@login_required
def student(request):
    if not (request.user.is_owner() or request.user.is_branch_manager()):
        return redirect('dashboard')
    students = models.RsquareUser.objects.filter(role='STUDENT')
    courses = models.Course.objects.filter(branch__name=request.session['curr_branch'])
    return render(request, 'student/student_viewall.html', {'students': students, 'courses': courses})



@login_required
def student_add_new(request):
    if not (request.user.is_owner() or request.user.is_branch_manager()):
        return redirect('dashboard')
    if request.method =='POST':
        curr_branch = models.Branch.objects.get(name=request.session['curr_branch'])
        student = models.RsquareUser.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],
            role='STUDENT', branch_id=curr_branch.id, phone_no=request.POST['phone_no'],
            gender=request.POST['gender']
        )
        student.username = 'S'+str(student.id).zfill(6)
        student.set_password('test')
        student.save()
        profile = models.StudentProfile.objects.create(
            student=student, category=request.POST['category'], aadhar_num=request.POST['aadhar'], 
            dob=request.POST['dob'], address=request.POST['address'], landmark=request.POST['landmark'],
            city=request.POST['city'], state=request.POST['state'], pincode=request.POST['pincode'],
            school=request.POST['school'], nationality=request.POST['nationality']
        )
        print(request.POST)
        return redirect('student-guardian-add', pk=student.id)
        # return redirect('gaurdian-add', pk=student.id)
    else:
        return render(request, 'student/student_add_new.html')


# @login_required
# def student_add_guardian(request, pk):
#     student = get_object_or_404(models.RsquareUser, pk=pk, role='STUDENT')
#     if not (request.user.is_owner() or request.user.is_branch_manager()):
#         return redirect('dashboard')
#     if request.method == 'POST':
#         guardian = models.Guardian.objects.create(student_id=student.profile.pk, relation=request.POST['relation'], salutation=request.POST['salutation'],
#         first_name=request.POST['first_name'], last_name=request.POST['last_name'], aadhar_number=request.POST['aadhar_number'],
#         phone=request.POST['phone'], email=request.POST['email'], occupation=request.POST['occupation'])
#         print(request.Post)
#         return redirect('gaurdian-add', pk = student.id)
#     else:
#         guardians = Guardian.objects.filter(student_id = student.profile.pk)
#         context = {
#                 'gaurdians':guardians,
#                 'sid': student.id
#         }
#         return render(request, 'student/add_gaurdian.html', context)



@login_required
def student_guardian(request, pk):
    student = get_object_or_404(models.RsquareUser, pk=pk, role='STUDENT')
    if not (request.user.is_owner() or request.user.is_branch_manager()):
        return redirect('dashboard')
    if request.method == 'POST':
        guardian = models.Guardian.objects.create(student_id=student.profile.pk, relation=request.POST['relation'], salutation=request.POST['salutation'],
        first_name=request.POST['first_name'], last_name=request.POST['last_name'], aadhar_number=request.POST['aadhar_number'],
        phone=request.POST['phone'], email=request.POST['email'], occupation=request.POST['occupation'])
        return redirect('student-guardian-add', pk = student.id)
    else:
        guardians = Guardian.objects.filter(student_id=student.profile.pk)
        context = {
            'gaurdians': guardians,
            'sid': student.id
        }
        return render(request, 'student/add_gaurdian.html', context)


@login_required
def student_courses(request, pk):
    if not (request.user.is_owner() or request.user.is_branch_manager()):
        return redirect('dashboard')
    student = get_object_or_404(models.RsquareUser, pk=pk, role='STUDENT')
    if request.method == 'POST':
        print(request.POST)
        course_years = request.POST.getlist('course_academic_year')
        course_taken = request.POST.getlist('course-taken')
        course_count = request.POST.getlist('course_count')
        student_course = models.StudentCourse.objects.create(admission_date=request.POST['admission_date'],
        discount=request.POST['discount'], discount_type=request.POST['discount_type'], notes=request.POST['notes'],
        student=student.profile
        )
        for i in range(0, len(course_years)):
            models.CourseTaken.objects.create(course_id=course_taken[i], quantity=course_count[i],
            academic_year=course_years[i], student_course=student_course)
        extra_fee_remarks = request.POST.getlist('extra_fee_remarks')
        extra_fee = request.POST.getlist('extra_fee')
        for i in range(0, len(extra_fee)):
            models.ExtraFee.objects.create(remark=extra_fee_remarks[i], amount=extra_fee[i],
            student_course=student_course
            )
        return redirect('student-payment', pk=student.id)
    else:
        courses = models.Course.objects.filter(branch__name=request.session['curr_branch'])
        return render(request, 'student/course_form.html', {'courses': courses})


@login_required
def student_installments(request, pk):
    if not (request.user.is_owner() or request.user.is_branch_manager()):
        return redirect('dashboard')
    if request.method == 'POST':
        pass
    else:
        return render(request, 'student/installments_form.html')


@login_required
def dark_mode(request):
    if request.session.get("dark", None):
        request.session["dark"] = False
    else:
        request.session["dark"] = True
    return redirect('dashboard')


@login_required
def settings(request):
    if request.method == 'POST':
        if request.POST.get('dark-mode-switch', 'off') == 'on':
            request.session["dark"] = True;
        else:
            request.session["dark"] = False;
        return redirect('settings')
    return render(request, 'settings.html')


@login_required
def batch_view(request):
    batches = models.Batch.objects.all()
    return render(request, 'batch/batch_viewall.html', {'batches': batches})


@login_required
def batch_add(request):
    if request.method == 'POST':
        print(request.POST)
        batch = models.Batch()
        batch.name = request.POST['name']
        batch.academic_year = request.POST['academic_year']
        batch.save()
        if request.POST.get('is_course_based', 'off')=='on':
            batch.is_course_based = True
            batch.course_id = request.POST['course']            
        else:
            batch.is_course_based = False
            batch.subjects.add(*request.POST.getlist('subjects'))
        batch.save()
        return redirect('batch-viewall')
    courses = models.Course.objects.filter(branch__name=request.session['curr_branch'])
    subject_groups = models.SubjectGroup.objects.all()
    return render(request, 'batch/batch_add.html', {'courses':courses, 'subject_groups': subject_groups})


@login_required
def batch_edit(request, pk):
    batch = get_object_or_404(models.Batch, pk=pk)
    if request.method=='POST':
        batch.name = request.POST['name']
        batch.academic_year = request.POST['academic_year']
        batch.save()
        if request.POST.get('is_course_based', 'off')=='on':
            batch.is_course_based = True
            batch.course_id = request.POST['course']            
        else:
            batch.is_course_based = False
            batch.subjects.add(*request.POST.getlist('subjects'))
        batch.save()
        return redirect('batch-viewall')
    courses = models.Course.objects.filter(branch__name=request.session['curr_branch'])
    subject_groups = models.SubjectGroup.objects.all()
    return render(request, 'batch/batch_add.html', {'courses':courses, 'subject_groups': subject_groups, 'batch': batch})
