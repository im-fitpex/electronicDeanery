from django.db import models
from core.models import Subject, Semester, Group, User
from teachers.models import Teacher
from students.models import Student


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher, models.DO_NOTHING)
    group = models.ForeignKey(Group, models.DO_NOTHING)
    semester = models.ForeignKey(Semester, models.DO_NOTHING, blank=True, null=True)
    class_type = models.CharField(max_length=20)
    class_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20, blank=True, null=True)
    topic = models.CharField(max_length=200, blank=True, null=True)
    attendance_checked = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classes'

    def __str__(self):
        return f"{self.subject.name} - {self.group.group_name} ({self.class_date})"


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    class_session = models.ForeignKey(Class, models.DO_NOTHING, db_column='class_id')
    student = models.ForeignKey(Student, models.DO_NOTHING)
    is_present = models.BooleanField()
    late_minutes = models.IntegerField(blank=True, null=True)
    excuse = models.CharField(max_length=200, blank=True, null=True)
    recorded_by = models.ForeignKey(User, models.DO_NOTHING, db_column='recorded_by', blank=True, null=True)
    recorded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attendance'
        unique_together = (('class_session', 'student'),)

    def __str__(self):
        status = "Присутствовал" if self.is_present else "Отсутствовал"
        return f"{self.student.full_name} - {self.class_session.subject.name}: {status}"