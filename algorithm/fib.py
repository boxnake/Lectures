import time

def fibDAC(n):
  if n<=2:
    return 1
  else:
    return fibDAC(n-1) + fibDAC(n-2)

def fibDP(n):
  fib_arr = []
  fib_arr.append(0)
  if n>0:
    fib_arr.append(1)
    for i in range(2,n+1):
      fib_arr.append(fib_arr[i-2] + fib_arr[i-1])
  return fib_arr[n]

def testAlgo(algo, start, end):
  if algo == fibDAC:
    print("="*20+"Divide And Conquer"+"="*20)
  elif algo == fibDP:
    print("="*20+"Dynamic Programming"+"="*20)
  for i in range(start,end):
    start_time = time.time()
    result = algo(i)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("{0}번째 피보나치 수열: {1}, 걸린 시간: {2:.3f}초".format(i, result, elapsed_time))

# testAlgo(fibDP, 36, 46)
# testAlgo(fibDAC, 36, 46)
testAlgo(fibDP, 100000,100001)
