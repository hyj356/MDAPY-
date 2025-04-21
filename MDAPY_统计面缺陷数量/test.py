import time 

def sum(n:int):
  result = 0
  for i in range(n):
    result += i
  return result

def sum_for():
  st = time.perf_counter()
  for _ in range(20000):
    tmp = sum(n=_)
  ed = time.perf_counter()
  print(f'Cost {ed-st} seconds.')
  return ed-st

def sum_map():
  st = time.perf_counter()
  result = map(sum, range(20000000))
  ed = time.perf_counter()
  print(f'Cost {ed-st} seconds.')
  return ed-st

if __name__ == "__main__":
  t2 = sum_map()
  t1 = sum_for()
  print(f"The acceleration ratio is {round(t1/t2)}.")



