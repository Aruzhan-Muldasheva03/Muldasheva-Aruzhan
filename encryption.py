text = "NURSULTAN"

# Зашифровка
encrypted = []

for char in text:
    number = ord(char) - 64
    encrypted.append(number * 2 + 1)

print("Зашифровано:", encrypted)


# Расшифровка
decrypted = ""

for number in encrypted:
    original_number = (number - 1) // 2
    char = chr(original_number + 64)
    decrypted = decrypted + char

print("Расшифровано:", decrypted)
