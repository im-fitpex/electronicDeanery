from django.db import models
from core.models import Group, User


class Student(models.Model):
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
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    student_type = models.CharField(max_length=20)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'students'

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.record_book_number})"

    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    def get_status_display(self):
        status_choices = {
            'active': 'Активен',
            'academic_leave': 'Академический отпуск',
            'expelled': 'Отчислен',
            'graduated': 'Выпущен'
        }
        return status_choices.get(self.status, self.status)


class Bachelor(models.Model):
    student_id = models.AutoField(primary_key=True)
    record_book_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField()
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20)
    admission_date = models.DateField()
    group_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    student_type = models.CharField(max_length=20)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    specialty_field = models.CharField(max_length=100, blank=True, null=True)
    thesis_topic = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bachelors'


class Master(models.Model):
    student_id = models.AutoField(primary_key=True)
    record_book_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField()
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20)
    admission_date = models.DateField()
    group_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    student_type = models.CharField(max_length=20)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    thesis_topic = models.CharField(max_length=200, blank=True, null=True)
    research_supervisor_id = models.IntegerField(blank=True, null=True)
    thesis_defense_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'masters'


class Specialist(models.Model):
    student_id = models.AutoField(primary_key=True)
    record_book_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField()
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20)
    admission_date = models.DateField()
    group_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    student_type = models.CharField(max_length=20)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    specialty_field = models.CharField(max_length=100, blank=True, null=True)
    diploma_topic = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'specialists'


class Postgraduate(models.Model):
    student_id = models.AutoField(primary_key=True)
    record_book_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField()
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20)
    admission_date = models.DateField()
    group_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    student_type = models.CharField(max_length=20)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    research_field = models.CharField(max_length=200, blank=True, null=True)
    supervisor_id = models.IntegerField(blank=True, null=True)
    dissertation_topic = models.CharField(max_length=300, blank=True, null=True)
    expected_defense_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'postgraduates'