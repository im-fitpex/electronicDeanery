from django import forms
from core.models import Teachers, Department


class TeacherCreateForm(forms.ModelForm):
    class Meta:
        model = Teachers
        fields = [
            'first_name', 'last_name', 'middle_name', 'email', 'phone',
            'degree', 'academic_title', 'department', 'position',
            'employment_date'
        ]
        widgets = {
            'employment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите отчество (необязательно)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'к.т.н., д.т.н., и т.д.'}),
            'academic_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'доцент, профессор, и т.д.'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ассистент, старший преподаватель, и т.д.'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'email': 'Email',
            'phone': 'Телефон',
            'degree': 'Ученая степень',
            'academic_title': 'Ученое звание',
            'department': 'Кафедра',
            'position': 'Должность',
            'employment_date': 'Дата трудоустройства',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля необязательными
        self.fields['middle_name'].required = False
        self.fields['phone'].required = False
        self.fields['degree'].required = False
        self.fields['academic_title'].required = False
        self.fields['employment_date'].required = False

    def save(self, commit=True):
        teacher = super().save(commit=False)
        teacher.is_active = True  # Автоматически активный
        
        if commit:
            teacher.save()
        return teacher


class TeacherEditForm(forms.ModelForm):
    class Meta:
        model = Teachers
        fields = [
            'first_name', 'last_name', 'middle_name', 'email', 'phone',
            'degree', 'academic_title', 'department', 'position',
            'employment_date', 'is_active'
        ]
        widgets = {
            'employment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите отчество (необязательно)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (XXX) XXX-XX-XX'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'к.т.н., д.т.н., и т.д.'}),
            'academic_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'доцент, профессор, и т.д.'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ассистент, старший преподаватель, и т.д.'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'email': 'Email',
            'phone': 'Телефон',
            'degree': 'Ученая степень',
            'academic_title': 'Ученое звание',
            'department': 'Кафедра',
            'position': 'Должность',
            'employment_date': 'Дата трудоустройства',
            'is_active': 'Активен'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля необязательными
        self.fields['middle_name'].required = False
        self.fields['phone'].required = False
        self.fields['degree'].required = False
        self.fields['academic_title'].required = False
        self.fields['employment_date'].required = False