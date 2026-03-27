
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Первая запись.\n")


with open("output.txt", "a", encoding="utf-8") as f:
    f.write("Эта строка добавлена в конец.\n")

print("Данные успешно записаны в output.txt")