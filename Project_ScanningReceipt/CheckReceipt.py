def validate_twid_company(id):
    if len(id) != 8:
        return False

    # 檢查統一編號是否全是數字
    if not id.isdigit():
        return False

    # 檢查統一編號的檢查碼是否正確
    check_sum = 0
    factors = [1, 2, 1, 2, 1, 2, 4, 1]
    for i in range(0, 7):
        factor = factors[i]
        value = ord(id[i]) - ord('0')
        check_sum += factor * value
    if id[6] == '7':
        check_sum += 1
    check_digit = (10 - check_sum % 10) % 10
    if ord(id[7]) - ord('0') != check_digit:
        return False

    return True
id = "04595252"

if validate_twid_company(id):     #呼叫函式檢查
    print(id + " is a valid TIN")
else:
    print(id + " is not a valid TIN")