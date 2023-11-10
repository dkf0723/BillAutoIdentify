#測試演算法
arr = [3,7,1,84,34,96,5,57]
arr_name = ['b','d','a','g','e','h','c','f'] #讓名字也一起換

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
print(arr)
print(arr_name)

print('heapSort')
print(heapSort(arr, arr_name))