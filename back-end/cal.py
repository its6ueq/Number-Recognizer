
def calcu(s):
    print("Đang tính toán: ", end = "")

    arr = list(map(int, s.split()))
    for i in range(len(arr)):
        if(arr[i] == 11):
            print(" + ", end = "")
        elif(arr[i] == 12):
            print(" - ", end = "")
        elif(arr[i] == 13):
            print(" x ", end = "")
        elif(arr[i] == 14):
            print(" : ", end = "")
        else:
            print(arr[i], end = "")

    i = 0
    symbol = []
    while i < len(arr):
        if arr[i] == 13 or arr[i] == 14:

            tmp = 0
            while i + 1 < len(arr) and arr[i + 1] <= 9:
                tmp = tmp * 10 + arr[i + 1]
                arr.pop(i + 1)

            if arr[i] == 13:
                arr[i - 1] *= tmp
            else:
                arr[i - 1] /= tmp
            
            arr.pop(i)
        elif arr[i] == 11 or arr[i] == 12:
            symbol.append(i)
            i += 1
        else:
            while i + 1 < len(arr) and arr[i + 1] <= 9:
                arr[i] = arr[i] * 10 + arr[i + 1]
                arr.pop(i + 1)
            i += 1

    res = 0
    if len(symbol) == 0 or symbol[0] > 0:
        res = arr[0]

    for i in symbol:
        if arr[i] == 11:
            res += arr[i + 1]
        if arr[i] == 12:
            res -= arr[i + 1]


    
    print("\nResult = " + str(res))
    return str(res)

print(calcu("3 1 11 2 13 1 2 12 2 0 14 2 14 1 0"))