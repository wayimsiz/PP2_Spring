file_path = "example.txt"


with open(file_path, "w", encoding="utf-8") as f:
    f.write("Line 1: Hello Python!\nLine 2: Learning files.")


print("--- Чтение целиком ---")
with open(file_path, "r", encoding="utf-8") as f:
    print(f.read())

print("\n--- Построчное чтение ---")
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        print(f"Строка: {line.strip()}")