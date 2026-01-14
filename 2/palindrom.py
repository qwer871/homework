# task1/palindrome.py
def is_palindrome(s: str) -> bool:
    # Очистка строки: оставляем только буквы и цифры, преобразуем в нижний регистр
    cleaned = ''.join(ch.lower() for ch in s if ch.isalnum())
    # Проверка на палиндром
    return cleaned == cleaned[::-1]