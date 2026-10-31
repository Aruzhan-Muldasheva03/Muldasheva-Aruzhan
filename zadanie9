# Лабораторная работа №8
# Задание №9. Программная реализация Хаффмана

import heapq
import math
from collections import Counter
from itertools import count


# Построение дерева Хаффмана
def build_huffman(freq):
    if not freq:
        raise ValueError("Пустой алфавит")

    order = count()
    heap = []

    for symbol, weight in freq.items():
        if weight > 0:
            heapq.heappush(heap, (weight, next(order), symbol))

    if not heap:
        raise ValueError("Все частоты равны нулю")

    # Объединяем два узла с минимальными частотами
    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)

        new_node = (left, right)

        heapq.heappush(
            heap,
            (w1 + w2, next(order), new_node)
        )

    tree = heap[0][2]
    codes = {}

    # Создание кодов по дереву
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
    # Если в сообщении один уникальный символ
    if isinstance(tree, str):
        if any(bit != "0" for bit in bits):
            raise ValueError("Неверный битовый поток")
        return tree * len(bits)

    result = []
    node = tree

    for bit in bits:
        if bit not in "01":
            raise ValueError("Недопустимый бит")

        node = node[int(bit)]

        if isinstance(node, str):
            result.append(node)
            node = tree

    if node is not tree:
        raise ValueError("Неполное кодовое слово")

    return "".join(result)


# Исходное сообщение
text = "ABCADE"

# Подсчёт частот символов
freq = Counter(text)

# Построение дерева и кодов
tree, codes = build_huffman(freq)

# Общее количество символов
total = sum(freq.values())

# Вероятности символов
probabilities = {
    symbol: frequency / total
    for symbol, frequency in freq.items()
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

# Эффективность кодирования
eta = H / L * 100

# Кодирование и декодирование
bits = encode(text, codes)
decoded = decode(bits, tree)


# Вывод результатов
print("Лабораторная работа №8")
print("Задание №9")
print()

print("Исходное сообщение:", text)
print("Частоты:", dict(freq))

print("\nТаблица кодов Хаффмана:")

for symbol in sorted(codes):
    print(
        symbol,
        "Вероятность:", round(probabilities[symbol], 3),
        "Код:", codes[symbol],
        "Длина:", len(codes[symbol])
    )

print("\nСредняя длина L:", round(L, 4))
print("Энтропия H(X):", round(H, 4))
print("Эффективность:", round(eta, 2), "%")

print("\nЗакодированное сообщение:", bits)
print("Декодированное сообщение:", decoded)

# Проверка правильности
assert decoded == text
print("Проверка кодирования и декодирования: PASS")


# Проверка одного уникального символа
print("\nПроверка одного уникального символа:")

single_text = "AAAAAA"
single_freq = Counter(single_text)

single_tree, single_codes = build_huffman(single_freq)

single_bits = encode(single_text, single_codes)
single_decoded = decode(single_bits, single_tree)

print("Исходный текст:", single_text)
print("Код символа A:", single_codes["A"])
print("Закодированный текст:", single_bits)
print("Декодированный текст:", single_decoded)

assert single_codes["A"] == "0"
assert single_decoded == single_text

print("Проверка одного символа: PASS")
