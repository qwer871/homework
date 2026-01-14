# task2/filter_functions.py
def filter_strings(filter_func, string_array):
    return list(filter(filter_func, string_array))


def apply_filters():
    # Тестовые данные
    test_array = [
        "apple", 
        "banana", 
        "a test", 
        "test", 
        "another", 
        "long string", 
        "a",
        "hello world",
        "python",
        "java script"
    ]
    
    # Вызов основной функции с различными lambda-функциями
    results = {}
    
    # 1. Исключение строк, содержащих пробелы
    results['no_spaces'] = filter_strings(
        lambda s: ' ' not in s, 
        test_array
    )
    
    # 2. Исключение строк, начинающихся с буквы "a" (без учета регистра)
    results['no_start_with_a'] = filter_strings(
        lambda s: not s.lower().startswith('a'), 
        test_array
    )
    
    # 3. Исключение строк длиной менее 5 символов
    results['min_length_5'] = filter_strings(
        lambda s: len(s) >= 5, 
        test_array
    )
    
    # 4. Комбинированные условия: исключение строк, начинающихся с 'a' или длиной менее 5 символов
    results['combined'] = filter_strings(
        lambda s: not s.lower().startswith('a') and len(s) >= 5,
        test_array
    )
    
    return results


# Тестовые примеры
if __name__ == "__main__":
    # Вызов функции apply_filters
    all_results = apply_filters()
    
    # Вывод результатов
    print("Оригинальный массив:")
    print(["apple", "banana", "a test", "test", "another", "long string", "a", 
           "hello world", "python", "java script"])
    
    print("\n1. Исключение строк, содержащих пробелы:")
    print(all_results['no_spaces'])
    
    print("\n2. Исключение строк, начинающихся с буквы 'a':")
    print(all_results['no_start_with_a'])
    
    print("\n3. Исключение строк длиной менее 5 символов:")
    print(all_results['min_length_5'])
    
    print("\n4. Комбинированные условия (не начинаются с 'a' и длина ≥5):")
    print(all_results['combined'])