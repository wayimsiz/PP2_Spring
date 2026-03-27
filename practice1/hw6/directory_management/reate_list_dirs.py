import os

dir_name = "test_folder"


if not os.path.exists(dir_name):
    os.mkdir(dir_name)
    print(f"Папка {dir_name} создана.")


print("Содержимое текущей директории:")
for item in os.listdir("."):
    print(f"- {item}")