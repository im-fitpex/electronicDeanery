from django.db import models
from students.models import Student
from teachers.models import Teacher
from core.models import Subject, Semester


class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, models.DO_NOTHING)
    subject = models.ForeignKey(Subject, models.DO_NOTHING)
    semester = models.ForeignKey(Semester, models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher, models.DO_NOTHING, blank=True, null=True)
    value = models.CharField(max_length=10)
    exam_date = models.DateField()
    attempt_number = models.IntegerField(blank=True, null=True)
    control_type = models.CharField(max_length=20)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grades'

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.name}: {self.value}"

    @property
    def is_passing_grade(self):
        """Является ли оценка проходной"""
        return self.value in ['3', '4', '5', 'зачет']

    @property
    def numeric_value(self):
        """Числовое значение оценки для расчета GPA"""
        grade_mapping = {
            '5': 5.0,
            '4': 4.0,
            '3': 3.0,
            '2': 2.0,
            'зачет': None,  # Зачет не участвует в расчете GPA
            'незачет': 2.0,
            'н/я': 2.0,
        }
        return grade_mapping.get(self.value, None)