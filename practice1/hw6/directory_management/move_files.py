import os
import shutil


open("move_me.txt", "a").close()


if os.path.exists("move_me.txt"):
    shutil.move("move_me.txt", "moved_and_renamed.txt")
    print("Файл перемещен/переименован.")