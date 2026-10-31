# Лабораторная работа №8
# Задание №10. Исследование реального текста

import heapq
import math
from collections import Counter
from itertools import count


# Построение дерева Хаффмана
def build_huffman(freq):
    order = count()
    heap = []

    for symbol, weight in freq.items():
        heapq.heappush(
            heap,
            (weight, next(order), symbol)
        )

    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)

        heapq.heappush(
            heap,
            (w1 + w2, next(order), (left, right))
        )

    tree = heap[0][2]
    codes = {}

    def walk(node, prefix=""):
        if isinstance(node, str):
            codes[node] = prefix or "0"
        else:
            walk(node[0], prefix + "0")
            walk(node[1], prefix + "1")

    walk(tree)
    return tree, codes


# Кодирование текста
def encode(text, codes):
    return "".join(codes[s] for s in text)


# Декодирование текста
def decode(bits, tree):
    if isinstance(tree, str):
        return tree * len(bits)

    result = []
    node = tree

    for bit in bits:
        node = node[int(bit)]

        if isinstance(node, str):
            result.append(node)
            node = tree

    return "".join(result)


# Исходный русский текст (более 300 символов)
text = (
    "Информационная безопасность помогает защищать данные "
    "пользователей и организаций. Каждый день люди отправляют "
    "сообщения, используют интернет-магазины, банковские "
    "приложения и электронную почту. Во время передачи и хранения "
    "информации важно сохранять её конфиденциальность и "
    "целостность. Один из способов эффективного хранения данных "
    "— сжатие информации. Алгоритм Хаффмана присваивает часто "
    "встречающимся символам короткие коды, а редким символам "
    "более длинные. Такой метод позволяет уменьшить размер "
    "сообщения без потери исходных данных. После декодирования "
    "пользователь получает точно такой же текст, каким он был "
    "до сжатия."
)


# Проверяем длину текста
assert len(text) >= 300

# Учитываем пробелы, регистр и знаки препинания
# Например, "А" и "а" считаются разными символами

# Подсчёт частот
freq = Counter(text)

# Построение дерева и кодов
tree, codes = build_huffman(freq)

# Количество символов
N = len(text)

# Вероятности символов
probabilities = {
    s: freq[s] / N
    for s in freq
}

# Средняя длина кодового слова
L = sum(
    probabilities[s] * len(codes[s])
    for s in freq
)

# Энтропия Шеннона
H = -sum(
    p * math.log2(p)
    for p in probabilities.values()
)

# Эффективность
eta = H / L * 100

# Избыточность
R = (1 - H / L) * 100


# Исходный объём в UTF-8
original_bytes = len(text.encode("utf-8"))
original_bits = original_bytes * 8


# Кодирование Хаффмана
bits = encode(text, codes)

# Количество бит до выравнивания
compressed_bits = len(bits)

# Выравнивание до целого байта
padding = (8 - compressed_bits % 8) % 8

# Объём упакованного потока
packed_bits = compressed_bits + padding


# Оценка хранения таблицы кодов
# Для каждого символа храним:
# 4 байта Unicode-кода символа,
# 1 байт длины кода,
# само двоичное кодовое слово.

table_bits = sum(
    32 + 8 + len(code)
    for code in codes.values()
)

# Общий объём
total_bits = packed_bits + table_bits


# Коэффициент сжатия
K = original_bits / total_bits

# Процент сокращения
S = (1 - total_bits / original_bits) * 100


# Проверка декодирования
decoded = decode(bits, tree)
assert decoded == text


# Вывод результатов
print("Лабораторная работа №8")
print("Задание №10")
print()

print("Исходный текст:")
print(text)

print("\nКоличество символов:", N)
print("Различных символов:", len(freq))

print("\nТаблица кодов Хаффмана:")

for symbol in sorted(codes):
    name = repr(symbol)

    print(
        name,
        "Частота:", freq[symbol],
        "Код:", codes[symbol],
        "Длина:", len(codes[symbol])
    )


print("\nПОКАЗАТЕЛИ КОДИРОВАНИЯ")

print("Энтропия H(X):", round(H, 4))
print("Средняя длина L:", round(L, 4))
print("Эффективность:", round(eta, 2), "%")
print("Избыточность:", round(R, 2), "%")


print("\nСРАВНЕНИЕ ОБЪЁМОВ")

print("Исходный UTF-8:", original_bits, "бит")
print("После Хаффмана:", compressed_bits, "бит")
print("Выравнивание:", padding, "бит")
print("Упакованный поток:", packed_bits, "бит")
print("Таблица кодов:", table_bits, "бит")
print("Общий объём:", total_bits, "бит")


print("\nРЕЗУЛЬТАТ СЖАТИЯ")

print("Коэффициент K:", round(K, 4))
print("Сокращение S:", round(S, 2), "%")

print("\nПроверка декодирования: PASS")


# Итоговый вывод
print("\nВЫВОД:")

if total_bits < original_bits:
    print("Сжатие выгодно: итоговый объём уменьшился.")
else:
    print("Сжатие невыгодно: итоговый объём не уменьшился.")
