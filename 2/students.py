# task4/person_classes.py
from abc import ABC, abstractmethod


class Person(ABC):
    """Базовый класс для людей"""
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def print_info(self):
        """Выводит информацию о человеке"""
        print(f"Имя: {self.name}, Возраст: {self.age}")
    
    @abstractmethod
    def scholarship(self) -> int:
        """Рассчитывает сумму стипендии"""
        pass
    
    def scholarship_greater_than(self, other_person) -> bool:
        """Сравнивает стипендию с другой персоной (больше)"""
        return self.scholarship() > other_person.scholarship()
    
    def scholarship_less_than(self, other_person) -> bool:
        """Сравнивает стипендию с другой персоной (меньше)"""
        return self.scholarship() < other_person.scholarship()


class Student(Person):
    """Класс студента"""
    
    def __init__(self, name: str, age: int, group: str, avg_score: float):
        super().__init__(name, age)
        self.group = group
        self.avg_score = avg_score
    
    def print_info(self):
        """Выводит информацию о студенте"""
        super().print_info()
        print(f"Группа: {self.group}, Средний балл: {self.avg_score}")
    
    def scholarship(self) -> int:
        """Рассчитывает стипендию студента"""
        if self.avg_score == 5:
            return 6000
        elif self.avg_score < 5 and self.avg_score >= 4:  # Предполагается диапазон между 4 и 5
            return 4000
        else:
            return 0
    
    def __str__(self):
        return f"Student(name={self.name}, group={self.group}, avg_score={self.avg_score})"


class GraduateStudent(Person):
    """Класс аспиранта"""
    
    def __init__(self, name: str, age: int, group: str, avg_score: float, research_work: str):
        super().__init__(name, age)
        self.group = group
        self.avg_score = avg_score
        self.research_work = research_work
    
    def print_info(self):
        """Выводит информацию об аспиранте"""
        super().print_info()
        print(f"Группа: {self.group}, Средний балл: {self.avg_score}, Научная работа: {self.research_work}")
    
    def scholarship(self) -> int:
        """Рассчитывает стипендию аспиранта"""
        if self.avg_score == 5:
            return 8000
        elif self.avg_score < 5 and self.avg_score >= 4:  # Предполагается диапазон между 4 и 5
            return 6000
        else:
            return 0
    
    def __str__(self):
        return f"GraduateStudent(name={self.name}, group={self.group}, avg_score={self.avg_score}, research_work={self.research_work})"


# Тестовые примеры
if __name__ == "__main__":
    # Создание экземпляров студента и аспиранта
    student1 = Student("Иван Иванов", 20, "Группа 101", 5.0)
    student2 = Student("Петр Петров", 21, "Группа 102", 4.5)
    student3 = Student("Сергей Сергеев", 22, "Группа 103", 3.5)
    
    grad_student1 = GraduateStudent("Анна Аннова", 25, "Группа 201", 5.0, 
                                   "Исследование алгоритмов машинного обучения")
    grad_student2 = GraduateStudent("Мария Мариева", 26, "Группа 202", 4.7,
                                   "Анализ больших данных")
    
    # Вывод информации
    print("Информация о студенте:")
    student1.print_info()
    print(f"Стипендия: {student1.scholarship()}р\n")
    
    print("Информация об аспиранте:")
    grad_student1.print_info()
    print(f"Стипендия: {grad_student1.scholarship()}р\n")
    
    # Сравнение стипендий
    print("Сравнение стипендий:")
    print(f"{student1.name} стипендия больше, чем у {student2.name}: {student1.scholarship_greater_than(student2)}")
    print(f"{grad_student1.name} стипендия больше, чем у {student1.name}: {grad_student1.scholarship_greater_than(student1)}")