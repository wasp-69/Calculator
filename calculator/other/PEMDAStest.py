from random import randint, choice

def dim(string):
    return "\033[2m"+string+"\033[0m"

def calculator(equation):
    global history
    parts = equation.split()
    if equation.lower()=="example":
        example = ""
        for i in range((randint(1,20)*2)+1):
            example += str(randint(1,1000)) + " " + choice(["+","-","*","/"]) + " "
        example += str(randint(1,1000))
        return f"Example Equation: {example}"
    elif equation.lower()=="history":
        print(dim("-----"))
        for eq, ans in history.items():
            print(f"Equation: {eq}\nSolution: {ans}")
        return dim("-----")
    else:
        return evaluate_PEMDAS(parts, equation)

def evaluate_PEMDAS(parts, equation):
    global history
    try:
        i = 0
        while i < len(parts):
            if parts[i] == "^":
                parts = parts[:i-1] + [float(parts[i-1])**float(parts[i+1])] + parts[i+2:]
                i -= 1
            else:
                i += 1
        i = 0
        while i < len(parts):
            if parts[i] == "*":
                parts = parts[:i-1] + [float(parts[i-1])*float(parts[i+1])] + parts[i+2:]
                i -= 1
            elif parts[i] == "/":
                parts = parts[:i-1] + [float(parts[i-1])/float(parts[i+1])] + parts[i+2:]
                i -= 1
            else: 
                i += 1
        i = 0
        while i < len(parts):
            if parts[i] == "+":
                parts = parts[:i-1] + [float(parts[i-1])+float(parts[i+1])] + parts[i+2:]
                i -= 1
            elif parts[i] == "-":
                parts = parts[:i-1] + [float(parts[i-1])-float(parts[i+1])] + parts[i+2:]
                i -= 1
            else:
                i += 1
        solution = parts[0]
        history[equation] = solution
        return f"Answer: {solution}"
    except IndexError:
        return "Invalid equation format."
    except ValueError:
        return "Invalid equation format."
    except ZeroDivisionError:
        return "Cannot divide by zero."
    
def main():
    while True:
        try: 
            print(dim("\n"+" "*90+"test_build"),end="")
            print(calculator(input("\rEquation: ")))
        except KeyboardInterrupt:
            try:
                print(calculator(input(dim("[Ctrl+C again to confirm exit]")+"\nEquation: ")))
            except KeyboardInterrupt:
                print("\n\nProgram closed.\n")
                exit()

history = {}
print("""\n-Type in equations in the form <operand><space><operation><space><operand> and so on.
-The space is required.
-Current operands include: + - * / ^.
-Evaluation is left-to-right, PEMDAS will not be followed exclusively.
-Keyboard interrupt (twice) to exit.
-Type Example for an example equation.
-Type History to get usage history.\n""")

if __name__ == "__main__":
    main()


# [done] version 1.5: added error handling for invalid input, added error handling for division by zero, added error handling for non-integer input, added error handling for invalid operations, added error handling for missing operands, added error handling for extra operands, added error handling for empty input.
# version 2: add pemdas functionality, added exponents functionality, added history functionality.
# version 3: add variable functionality, add parentheses functionality