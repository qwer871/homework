# task5/decorator.py
import time
from functools import wraps


def timing_decorator(func):
    """
    Декоратор для измерения времени выполнения функции
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время выполнения функции {func.__name__}: {execution_time:.6f} секунд")
        return result
    return wrapper


# Тестовая функция 1: Вычисление суммы двух чисел
@timing_decorator
def sum_numbers(a, b):
    """Вычисляет сумму двух чисел и выводит результат"""
    result = a + b
    print(f"{a} + {b} = {result}")
    return result


# Тестовая функция 2: Чтение из файла, вычисление и запись результата
@timing_decorator
def process_file(input_file="input.txt", output_file="output.txt"):
    """
    Считывает два числа из файла, вычисляет их сумму и записывает результат
    """
    try:
        # Чтение входного файла
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Разбор чисел (предполагается одно число в строке)
        numbers = []
        for line in lines:
            line = line.strip()
            if line:  # Пропуск пустых строк
                try:
                    numbers.append(float(line))
                except ValueError:
                    print(f"Предупреждение: не удалось разобрать '{line}' как число")
        
        if len(numbers) >= 2:
            a, b = numbers[0], numbers[1]
            result = a + b
            
            # Запись в выходной файл
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"{a} + {b} = {result}\n")
            
            print(f"Результат записан в {output_file}")
            return result
        else:
            print(f"Ошибка: требуется как минимум 2 числа, но найдено только {len(numbers)}")
            return None
            
    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не существует")
        return None


# Создание примера входного файла
def create_example_files():
    """Создание примера входного файла"""
    with open("input.txt", "w", encoding="utf-8") as f:
        f.write("10.5\n")
        f.write("20.3\n")
        f.write("# Комментарий\n")
        f.write("30\n")


# Тестовые примеры
if __name__ == "__main__":
    print("Тестовая функция 1: Вычисление суммы двух чисел")
    sum_numbers(10, 20)
    
    print("\n" + "="*50 + "\n")
    
    print("Тестовая функция 2: Чтение из файла, вычисление и запись результата")
    # Создание примерного файла
    create_example_files()
    
    # Тестирование функции обработки файла
    process_file()
    
    # Отображение содержимого выходного файла
    try:
        with open("output.txt", "r", encoding="utf-8") as f:
            print(f"Содержимое выходного файла: {f.read().strip()}")
    except FileNotFoundError:
        print("Выходной файл не существует")