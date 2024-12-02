
def calcu(s):
    print("Đang tính toán: ", end = "")
    arr = list(map(int, s.split()))
    summ = 0
    temp = 0
    neg = 1
    for i in range(len(arr)):
        if(arr[i] == 11):
            print(" + ", end = "")
        elif(arr[i] == 12):
            print(" - ", end = "")
        else:
            print(arr[i], end = "")
        if arr[i] == 11:
            summ = summ + neg * temp
            neg = 1
            temp = 0
        elif arr[i] == 12:
            summ = summ + neg * temp
            neg = -1
            temp = 0
        else:
            temp = temp * 10 + arr[i]
        if i == len(arr) - 1:
            summ = summ + neg * temp
    
    print("\nSum = " + str(summ))
    return str(summ)

print(calcu("1 11 2"))