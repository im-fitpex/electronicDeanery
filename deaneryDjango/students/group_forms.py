from django import forms
from core.models import Group, Program
from django.db import connection


class GroupCreateForm(forms.ModelForm):
    direction_code = forms.ChoiceField(
        choices=[
            ('09.03.01', 'Информатика и вычислительная техника (бакалавриат)'),
            ('09.03.02', 'Информационные системы и технологии (бакалавриат)'),
            ('09.03.03', 'Прикладная информатика (бакалавриат)'),
            ('09.03.04', 'Программная инженерия (бакалавриат)'),
            ('15.05.01', 'Проектирование технологических машин и комплексов (специалитет)'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Направление'
    )
    
    group_number = forms.IntegerField(
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер группы'}),
        label='Номер группы',
        help_text='Номер группы в рамках направления (1-20)'
    )

    class Meta:
        model = Group
        fields = ['admission_year', 'course']
        widgets = {
            'admission_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год поступления (например, 2024)',
                'min': 2020,
                'max': 2030
            }),
            'course': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Курс (1-6)',
                'min': 1,
                'max': 6
            }),
        }
        labels = {
            'admission_year': 'Год поступления',
            'course': 'Курс',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем значения по умолчанию
        from datetime import datetime
        current_year = datetime.now().year
        self.fields['admission_year'].initial = current_year
        self.fields['course'].initial = 1

    def clean(self):
        cleaned_data = super().clean()
        direction_code = cleaned_data.get('direction_code')
        admission_year = cleaned_data.get('admission_year')
        group_number = cleaned_data.get('group_number')
        
        if direction_code and admission_year and group_number:
            # Проверяем, что номер группы соответствует диапазону направления
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT group_range_start, group_range_end FROM directions WHERE code = %s",
                    [direction_code]
                )
                result = cursor.fetchone()
                if result:
                    start, end = result
                    if not (start <= group_number <= end):
                        raise forms.ValidationError(
                            f'Номер группы для направления {direction_code} должен быть от {start} до {end}'
                        )
            
            # Генерируем название группы
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT generate_group_name(%s, %s, %s)",
                    [direction_code, admission_year, group_number]
                )
                group_name = cursor.fetchone()[0]
                
                # Проверяем уникальность названия группы
                if Group.objects.filter(group_name=group_name).exists():
                    raise forms.ValidationError(
                        f'Группа с названием {group_name} уже существует'
                    )
                
                cleaned_data['group_name'] = group_name
        
        return cleaned_data

    def save(self, commit=True):
        group = super().save(commit=False)
        direction_code = self.cleaned_data['direction_code']
        group_number = self.cleaned_data['group_number']
        
        # Устанавливаем название группы
        group.group_name = self.cleaned_data['group_name']
        
        # Устанавливаем тип студента на основе направления
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT degree_level FROM directions WHERE code = %s",
                [direction_code]
            )
            result = cursor.fetchone()
            if result:
                degree_level = result[0]
                group.student_type = degree_level
            else:
                group.student_type = 'bachelor'  # по умолчанию
        
        group.is_active = True
        
        if commit:
            group.save()
        return group