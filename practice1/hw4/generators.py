#iterator
mystr = "banana"
myit = iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
#generator
def my_generator():
  yield 1
  yield 2
  yield 3

for value in my_generator():
  print(value)