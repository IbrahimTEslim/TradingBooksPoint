from datetime import datetime
from django.core.exceptions import ValidationError

def validate_university_id(value):
    value_str = str(value)

    if not value_str.isdigit(): raise ValidationError("This is not valid IUG university student ID")
    first_char = value[0]
    year_part = int(value[1:5])
    student_part = int(value[5:])
    current_year = int(datetime.now().year)
    if len(value_str) == 9 and (first_char == '1' or first_char == '2') and (year_part <= current_year and year_part >= current_year - 10):
        return value
    else: raise ValidationError("This is not valid IUG university student ID")