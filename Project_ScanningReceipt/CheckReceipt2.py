def check_TIN(tin):
    if len(tin) != 8:
        return False
    factors = [1, 2, 1, 2, 1, 2, 4, 1]
    check_sum = 0
    if factors[6] == 7:     #如果第七位為七
        for i in range(8):
            digit = int(tin[i])
            factor = factors[i]
            product = digit * factor
            if product > 9:
                product = product // 10 + product % 10
            check_sum += product
    else:     #第七位不為七
        for i in range(8):
            digit = int(tin[i])
            factor = factors[i]
            product = digit * factor
            if product > 9:
                product = product // 10 + product % 10
            check_sum += product
    print(check_sum)
    return check_sum % 5 == 0     #新制檢查法，能否被5整除

tin = "04595252"

if check_TIN(tin):     #呼叫函式檢查
    print(tin + " is a valid TIN")
else:
    print(tin + " is not a valid TIN")