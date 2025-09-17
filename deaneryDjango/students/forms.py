from django import forms
from core.models import Students, Group
from datetime import datetime


class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = [
            'first_name', 'last_name', 'middle_name',
            'birth_date', 'email', 'phone', 'status', 'admission_date',
            'group', 'student_type'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'admission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите отчество (необязательно)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
            'status': forms.Select(choices=[
                ('active', 'Активен'),
                ('academic_leave', 'Академический отпуск'),
                ('expelled', 'Отчислен'),
                ('graduated', 'Выпущен')
            ], attrs={'class': 'form-control'}),
            'student_type': forms.Select(choices=[
                ('bachelor', 'Бакалавр'),
                ('master', 'Магистр'),
                ('specialist', 'Специалист'),
                ('postgraduate', 'Аспирант')
            ], attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'birth_date': 'Дата рождения',
            'email': 'Email',
            'phone': 'Телефон',
            'status': 'Статус',
            'admission_date': 'Дата поступления',
            'group': 'Группа',
            'student_type': 'Тип студента',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля необязательными
        self.fields['middle_name'].required = False
        self.fields['phone'].required = False
        self.fields['email'].required = False
        
        # Устанавливаем значения по умолчанию
        self.fields['status'].initial = 'active'
        self.fields['student_type'].initial = 'bachelor'

    def save(self, commit=True):
        student = super().save(commit=False)
        
        if commit:
            # Автоматически генерируем номер зачетки в формате 1YYXXX
            year_suffix = str(student.admission_date.year)[-2:]
            
            # Находим следующий порядковый номер для данного года
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT MAX(CAST(RIGHT(record_book_number, 3) AS INTEGER)) FROM students WHERE record_book_number LIKE %s",
                    [f"1{year_suffix}%"]
                )
                result = cursor.fetchone()
                last_number = result[0] if result[0] else 0
            
            next_number = last_number + 1
            student.record_book_number = f"1{year_suffix}{next_number:03d}"
            student.is_active = True
            
            student.save()
        return student


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = [
            'record_book_number', 'first_name', 'last_name', 'middle_name',
            'birth_date', 'email', 'phone', 'status', 'admission_date',
            'group', 'student_type'
        ]
        widgets = {
            'record_book_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'admission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите отчество (необязательно)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
            'status': forms.Select(choices=[
                ('active', 'Активен'),
                ('academic_leave', 'Академический отпуск'),
                ('expelled', 'Отчислен'),
                ('graduated', 'Выпущен')
            ], attrs={'class': 'form-control'}),
            'student_type': forms.Select(choices=[
                ('bachelor', 'Бакалавр'),
                ('master', 'Магистр'),
                ('specialist', 'Специалист'),
                ('postgraduate', 'Аспирант')
            ], attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'record_book_number': 'Номер зачетной книжки',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'birth_date': 'Дата рождения',
            'email': 'Email',
            'phone': 'Телефон',
            'status': 'Статус',
            'admission_date': 'Дата поступления',
            'group': 'Группа',
            'student_type': 'Тип студента',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля необязательными
        self.fields['middle_name'].required = False
        self.fields['phone'].required = False
        self.fields['email'].required = False
        
        # Номер зачетки только для чтения
        self.fields['record_book_number'].help_text = 'Номер зачетки нельзя изменить'