names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]


print("--- Enumerate ---")
for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")


print("\n--- Zip ---")
for name, score in zip(names, scores):
    print(f"Ученик {name} получил {score}")