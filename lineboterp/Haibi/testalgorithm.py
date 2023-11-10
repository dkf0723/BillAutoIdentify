#測試演算法
arr = [3,7,1,84,34,96,5,57]
arr_name = ['b','d','a','g','e','h','c','f'] #讓名字也一起換
arr_len = len(arr)-4
def bubbleSort(arr, arr_name):
    for i in range(1, len(arr)):
        for j in range(0, len(arr)-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                arr_name[j], arr_name[j + 1] = arr_name[j + 1], arr_name[j]
    return arr, arr_name

def buildMaxHeap(arr, arr_name):
    import math
    for i in range(math.floor(len(arr)/2),-1,-1):
        heapify(arr, arr_name,i)
def heapify(arr, arr_name, i): 
    left = 2*i+1
    right = 2*i+2
    largest = i
    if left < arrLen and arr[left] > arr[largest]:
        largest = left
    if right < arrLen and arr[right] > arr[largest]:
        largest = right

    if largest != i:
            swap(arr, arr_name, i, largest)
            heapify(arr, arr_name, largest)

def swap(arr, arr_name, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    arr_name[i], arr_name[j] = arr_name[j], arr_name[i]
def heapSort(arr, arr_name):
    global arrLen
    arrLen = len(arr)
    buildMaxHeap(arr, arr_name)
    for i in range(len(arr)-1,0,-1):
        swap(arr, arr_name,0,i)
        arrLen -=1
        heapify(arr, arr_name, 0)
    return arr, arr_name
print('原始數據')    
print(arr)
print(arr_name)
# print('bubbleSort')
# print(bubbleSort(arr))
print('heapSort')
heapsort_result = heapSort(arr, arr_name)

heapsort_result_name = heapsort_result[1]
heapsort_result_figure = heapsort_result[0]
print(heapsort_result_name)
print(heapsort_result_figure)

heapsort_result_name_limited = heapsort_result_name[arr_len:] #取前四的商品
heapsort_result_figure_limited = heapsort_result_figure[arr_len:] #取前四商品的成本
remaining_total_cost = 0 #取剩餘的成本
for i in range(arr_len):
  remaining_total_cost +=  int(heapsort_result_figure_limited[i])

print('取排名')
print(heapsort_result_name_limited)
print(heapsort_result_figure_limited)
print(remaining_total_cost)