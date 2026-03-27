import os
import shutil

source = "output.txt"
destination = "output_copy.txt"


if os.path.exists(source):
    shutil.copy(source, destination)
    print(f"Файл {source} скопирован в {destination}")


if os.path.exists(destination):
    os.remove(destination)
    print(f"Копия {destination} удалена.")