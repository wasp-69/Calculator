def verify_parenthesis(parts):
    counter = 0
    for i in parts:
        if i == "(":
            counter += 1
        elif i == ")":
            counter -= 1
        if counter < 0:
            return False
    return counter == 0

print(verify_parenthesis(["("])) #F
print(verify_parenthesis(["(","3",")"])) #T
print(verify_parenthesis(["(","3",")","(",")"])) #T
print(verify_parenthesis([")","(","3",")","("])) #F
print(verify_parenthesis(["(","(","3",")",")"])) #T
print(verify_parenthesis(["(", ")", ")", "("])) #F