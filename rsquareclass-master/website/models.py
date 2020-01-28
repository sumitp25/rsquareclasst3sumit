from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings

ROLE_CHOICES = (
    ('OWNER', 'Owner'), 
    ('BRANCHMANAGER', 'Branch Manager'),
    ('ACCOUNTANT', 'Accountant'),
    ('TEACHER', 'Teacher'),
    ('STUDENT', 'Student')
)

GENDER_CHOICES = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female')
)

CATEGORY_CHOICES = (
    ('GEN', 'General'),
    ('SC', 'SC'),
    ('ST', 'ST'),
    ('OBC', 'OBC')
)

GUARDIAN_RELATION_CHOICES = (
    ('FAT', 'Father'),
    ('MOT', 'Mother'),
    ('OTH', 'Other')
)

DISCOUNT_TYPES = (
    ('FLT', 'Flat'),
    ('PER', 'Percentage')
)

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class Branch(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    phone_no = models.CharField(max_length=13)

    def __str__(self):
        return self.name


class RsquareUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='OWNER')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    phone_no = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile/', blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='MALE')

    def is_owner(self):
        return self.role == 'OWNER'    
    def is_branch_manager(self):
        return self.role == 'BRANCHMANAGER'
    def is_student(self):
        return self.role == 'STUDENT'
    def is_teacher(self):
        return self.role == 'TEACHER'
    def is_accountant(self):
        return self.role == 'ACCOUNTANT'

    def __str__(self):
        return self.first_name + " " + self.last_name


class StudentProfile(models.Model):
    student = models.OneToOneField(RsquareUser, on_delete=models.CASCADE, related_name='profile', null=True)
    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES, default='GEN')
    aadhar_num = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(verbose_name="Date of Birth")
    address = models.CharField(max_length=200)
    landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    pincode = models.CharField(max_length=8)
    school = models.CharField(max_length=100)
    nationality = models.CharField(max_length=20)

    def __str__(self):
        return str(self.student)

    
class Guardian(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    relation = models.CharField(max_length=3, choices=GUARDIAN_RELATION_CHOICES, default='FAT')
    salutation = models.CharField(max_length=3)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    aadhar_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=17, validators=[phone_regex])
    email = models.EmailField()
    occupation = models.CharField(max_length=30)

    def __str__(self):
        return str(self.student) + ' | ' + self.relation + ' | ' + self.first_name


class SubjectGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    fee = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    duration_type = models.CharField(max_length=20)
    no_of_installments = models.PositiveIntegerField()    
    days_between_two_installments = models.PositiveIntegerField()
    installment_duration_type = models.CharField(max_length=20)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CourseSubject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='rel')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='rel')

    def __str__(self):
        return str(self.course) + " | " + str(self.subject)


class Batch(models.Model):
    name = models.CharField(max_length=40)
    is_course_based = models.BooleanField(default=False)
    subjects = models.ManyToManyField(Subject, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    academic_year = models.CharField(max_length=40)


    def __str__(self):
        return self.name


class StudentCourse(models.Model):
    admission_date = models.DateField()
    discount = models.PositiveIntegerField()
    discount_type = models.CharField(max_length=4, choices=DISCOUNT_TYPES)
    notes = models.CharField(max_length=100)
    student = models.OneToOneField(StudentProfile, on_delete=models.CASCADE, related_name='enrolled')

    def __str__(self):
        return str(self.student.student) + ' Courses'


class ExtraFee(models.Model):
    remark = models.CharField(max_length=50)
    amount = models.PositiveIntegerField()
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student_course.student.student) + ' | ' + self.remark


class CourseTaken(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=30)
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return str(self.course) + ' | ' + str(self.student_course.student.student)
