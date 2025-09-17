from django.db import models


class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    record_book_number = models.CharField(unique=True, max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField()
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20)
    admission_date = models.DateField()
    group = models.ForeignKey('Group', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    student_type = models.CharField(max_length=20)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'students'

    def __str__(self):
        full_name = f"{self.last_name} {self.first_name}"
        if self.middle_name:
            full_name += f" {self.middle_name}"
        return full_name


class Teachers(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    degree = models.CharField(max_length=50, blank=True, null=True)
    academic_title = models.CharField(max_length=50, blank=True, null=True)
    department = models.ForeignKey('Department', models.DO_NOTHING)
    position = models.CharField(max_length=50)
    employment_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teachers'

    def __str__(self):
        full_name = f"{self.last_name} {self.first_name}"
        if self.middle_name:
            full_name += f" {self.middle_name}"
        if self.academic_title:
            full_name = f"{self.academic_title} {full_name}"
        return full_name


class Program(models.Model):
    program_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    code = models.CharField(unique=True, max_length=10)
    degree_level = models.CharField(max_length=20)
    duration_years = models.IntegerField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'programs'

    def __str__(self):
        return f"{self.code} - {self.name}"


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(unique=True, max_length=10)
    head_teacher_id = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    room = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departments'

    def __str__(self):
        return self.name


class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    academic_year = models.CharField(max_length=9)
    semester_number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'semesters'
        unique_together = (('academic_year', 'semester_number'),)

    def __str__(self):
        semester_name = "Осенний" if self.semester_number == 1 else "Весенний"
        return f"{self.academic_year} - {semester_name}"


class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True, null=True)
    credits = models.IntegerField()
    hours_total = models.IntegerField(blank=True, null=True)
    hours_lectures = models.IntegerField(blank=True, null=True)
    hours_practicals = models.IntegerField(blank=True, null=True)
    hours_labs = models.IntegerField(blank=True, null=True)
    department = models.ForeignKey(Department, models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subjects'

    def __str__(self):
        return self.name


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(unique=True, max_length=20)
    admission_year = models.IntegerField()
    course = models.IntegerField()
    program = models.ForeignKey(Program, models.DO_NOTHING)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'

    def __str__(self):
        return self.group_name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=100)
    password_hash = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    is_active = models.BooleanField()
    last_login = models.DateTimeField(blank=True, null=True)
    failed_login_attempts = models.IntegerField(blank=True, null=True)
    locked_until = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.username