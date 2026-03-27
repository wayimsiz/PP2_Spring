from functools import reduce

nums = [1, 2, 3, 4, 5, 6]


squared = list(map(lambda x: x**2, nums)) # [1, 4, 9, 16, 25, 36]


evens = list(filter(lambda x: x % 2 == 0, nums)) # [2, 4, 6]


total_sum = reduce(lambda x, y: x + y, nums) # 21

print(f"Original: {nums}")
print(f"Squared: {squared}")
print(f"Evens: {evens}")
print(f"Sum: {total_sum}")