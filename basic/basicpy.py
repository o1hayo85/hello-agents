a = 'ABC'.encode('ascii')
print(a)

print(len(b'avc'))

# function
def simple_abs(num):
  if num >= 0:
    return num
  else:
    return -num
  
print(simple_abs(-5))