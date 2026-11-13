# 1. НАСЛЕДОВАНИЕ
# ==========================================

from functools import total_ordering

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
        self.grades = {}

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


# ==========================================
# 2. КЛАСС LECTURER
# ==========================================

@total_ordering
class Lecturer(Mentor):

    @property
    def average_rating(self):
        all_grades = [
            grade
            for grades in self.grades.values()
            for grade in grades
        ]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {self.average_rating}'
        )

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_rating == other.average_rating

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_rating < other.average_rating


# ==========================================
# 3. КЛАСС REVIEWER
# ==========================================

class Reviewer(Mentor):

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}'
        )

    def rate_hw(self, student, course, grade):
        if not isinstance(student, Student):
            raise TypeError('Оценивать можно только студентов')

        if (
            course in self.courses_attached
            and course in student.courses_in_progress
        ):
            if 1 <= grade <= 10:
                student.grades.setdefault(course, []).append(grade)
            else:
                raise ValueError('Оценка должна быть от 1 до 10')
        else:
            raise ValueError(
                'Проверяющий или студент не относятся к этому курсу'
            )


# ==========================================
# 4. КЛАСС STUDENT
# ==========================================

@total_ordering
class Student:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    @property
    def average_rating(self):
        all_grades = [
            grade
            for grades in self.grades.values()
            for grade in grades
        ]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):
            raise TypeError('Оценивать можно только лекторов')

        if (
            course in self.courses_in_progress
            and course in lecturer.courses_attached
        ):
            if 1 <= grade <= 10:
                lecturer.grades.setdefault(course, []).append(grade)
            else:
                raise ValueError('Оценка должна быть от 1 до 10')
        else:
            raise ValueError(
                'Студент или лектор не относятся к этому курсу'
            )

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {self.average_rating}\n'
            f'Курсы в процессе изучения: '
            f'{", ".join(self.courses_in_progress)}\n'
            f'Завершенные курсы: {", ".join(self.finished_courses)}'
        )

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_rating == other.average_rating

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_rating < other.average_rating


# ==========================================
# 5. ФУНКЦИИ ПОДСЧЁТА СРЕДНИХ ОЦЕНОК
# ==========================================

def calculate_average_homework(students, course):
    grades = []

    for student in students:
        if course in student.grades:
            grades.extend(student.grades[course])

    return sum(grades) / len(grades) if grades else 0


def calculate_average_lecture(lecturers, course):
    grades = []

    for lecturer in lecturers:
        if course in lecturer.grades:
            grades.extend(lecturer.grades[course])

    return sum(grades) / len(grades) if grades else 0


# ==========================================
# 6. СОЗДАНИЕ ЭКЗЕМПЛЯРОВ КЛАССОВ
# ==========================================

reviewer1 = Reviewer('Иван', 'Иванов')
reviewer2 = Reviewer('Петр', 'Петров')

lecturer1 = Lecturer('Анна', 'Смирнова')
lecturer2 = Lecturer('Олег', 'Сидоров')

student1 = Student('Мария', 'Иванова')
student2 = Student('Алексей', 'Петров')


# ==========================================
# 7. ДОБАВЛЕНИЕ КУРСОВ
# ==========================================

reviewer1.courses_attached.append('Python')
reviewer2.courses_attached.append('Python')

lecturer1.courses_attached.append('Python')
lecturer2.courses_attached.append('Python')

student1.courses_in_progress.append('Python')
student2.courses_in_progress.append('Python')


# ==========================================
# 8. ПОЛЕВЫЕ ИСПЫТАНИЯ
# ==========================================

# Проверяющие оценивают домашние задания

reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)

reviewer2.rate_hw(student2, 'Python', 8)
reviewer2.rate_hw(student2, 'Python', 10)


# Студенты оценивают лекции

student1.rate_lecture(lecturer1, 'Python', 10)
student1.rate_lecture(lecturer1, 'Python', 9)

student2.rate_lecture(lecturer2, 'Python', 8)
student2.rate_lecture(lecturer2, 'Python', 10)


# ==========================================
# 9. ПРОВЕРКА НАСЛЕДОВАНИЯ
# ==========================================

print('ПРОВЕРКА НАСЛЕДОВАНИЯ')

print(isinstance(lecturer1, Mentor))
print(isinstance(reviewer1, Mentor))

print(lecturer1.courses_attached)
print(reviewer1.courses_attached)


# ==========================================
# 10. ПРОВЕРКА СТРОКОВОГО ПРЕДСТАВЛЕНИЯ
# ==========================================

print('\nПРОВЕРКА REVIEWER')

print(reviewer1)
print()
print(reviewer2)

print('\nПРОВЕРКА LECTURER')

print(lecturer1)
print()
print(lecturer2)

print('\nПРОВЕРКА STUDENT')

print(student1)
print()
print(student2)


# ==========================================
# 11. ПРОВЕРКА ОПЕРАТОРОВ СРАВНЕНИЯ
# ==========================================

print('\nСРАВНЕНИЕ ЛЕКТОРОВ')

print(lecturer1 > lecturer2)
print(lecturer1 < lecturer2)
print(lecturer1 == lecturer2)

print('\nСРАВНЕНИЕ СТУДЕНТОВ')

print(student1 > student2)
print(student1 < student2)
print(student1 == student2)


# ==========================================
# 12. ПРОВЕРКА ФУНКЦИЙ ПОДСЧЁТА ОЦЕНОК
# ==========================================

reviewers = [reviewer1, reviewer2]
lecturers = [lecturer1, lecturer2]
students = [student1, student2]

print('\nСРЕДНИЕ ОЦЕНКИ')

print(
    'Средняя оценка студентов:',
    calculate_average_homework(students, 'Python')
)

print(
    'Средняя оценка лекторов:',
    calculate_average_lecture(lecturers, 'Python')
)


# ==========================================
# 13. ПРОВЕРКА ОБРАБОТКИ ОШИБОК
# ==========================================

print('\nПРОВЕРКА ОБРАБОТКИ ОШИБОК')

try:
    student1.rate_lecture(reviewer1, 'Python', 10)
except TypeError as error:
    print(error)

try:
    student1.rate_lecture(lecturer1, 'Python', 11)
except ValueError as error:
    print(error)

try:
    reviewer1.rate_hw(lecturer1, 'Python', 10)
except TypeError as error:
    print(error)













































