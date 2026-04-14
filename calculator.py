from random import randint, choice

def dim(string):
    return "\033[2m"+string+"\033[0m"

def calculator(equation):
    global history_record, history, mode
    try:
        parts = equation.split()
        if parts[0].lower() == "/help":
            if len(parts) == 1:
                return help_text
            elif parts[1].lower() in ["/history","/h","history","h","1"]:
                return help_history
            elif parts[1].lower() in ["/mode","/m","mode","m","2"]:
                return help_mode
            elif parts[1].lower() in ["/example","/e","example","e","3"]:
                return help_example
            else:
                return f"No help topic found for '{parts[1]}'."

        elif parts[0].lower() in ["/example","/e"]:
            example = ""
            for i in range((randint(1,20)*2)+1):
                example += str(randint(1,1000)) + " " + choice(["+","-","*","/"]) + " "
            example += str(randint(1,1000))
            return f"Example Equation: {example} [{dim(calculator(example))}]"
        
        elif parts[0].lower() in ["/history","/h"]:
            if len(parts) == 1:
                print(dim("-----"))
                for eq, ans in history.items():
                    print(f"Equation: {eq}\nSolution: {ans}")
                return dim("-----")
            elif parts[1].lower() in ["clear","c"]:
                history={}
                return "History cleared."
            elif parts[1].lower() in ["record","r"]:
                if history_record:
                    history_record = False
                    return "History Recording is now toggled to: Paused"
                else:
                    history_record = True
                    return "History Recording is now toggled to: Resumed"
            elif parts[1].lower() in ["equate","e"]:
                try:
                    print(f"Equation From History: {list(history)[-1]}")
                    return calculator(list(history)[-1])
                except IndexError:
                    return "Nothing to equate."
            else:
                return f"No sub-command '{parts[1]}' found"
            
        elif parts[0].lower() in ["/mode","/m"]:
            if len(parts) == 1:
                if mode == "LTR":
                    mode = "PEMDAS"
                    return "Now evaluating in PEMDAS mode."
                else:
                    mode = "LTR"
                    return "Now evaluating in Left-to-Right mode."
            else:
                parts[0] = parts[0].lower()
                if mode == "LTR":
                    try:
                        parts.remove("/m")
                    except ValueError:
                        parts.remove("/mode")
                    return evaluate_PEMDAS(parts, " ".join(parts))
                else:
                    try:
                        parts.remove("/m")
                    except ValueError:
                        parts.remove("/mode")
                    return evaluate_LTR(parts, " ".join(parts))
        else:
            if mode == "LTR":
                return evaluate_LTR(parts, equation)
            else:
                return evaluate_PEMDAS(parts, equation)
    except IndexError:
        return "Invalid equation format."
    
def evaluate_PEMDAS(parts, equation):
    global history_record, history
    if not verify(parts):
        return "Invalid equation format."
    try:
        i = len(parts)-1
        while i > 0:
            if i > len(parts)-1:
                i = len(parts)-1
            if parts[i] == "^":                                                              #   fix the ^ 6 6 6 bug
                parts = parts[:i-1] + [float(parts[i-1])**float(parts[i+1])] + parts[i+2:]
                i += 1
            else:
                i -= 1
        i = 0
        while i < len(parts):
            if parts[i] == "*":
                parts = parts[:i-1] + [float(parts[i-1])*float(parts[i+1])] + parts[i+2:]
                i = max(i-1,0)
            elif parts[i] == "/":
                parts = parts[:i-1] + [float(parts[i-1])/float(parts[i+1])] + parts[i+2:]
                i = max(i-1,0)
            else: 
                i += 1
        i = 0
        while i < len(parts):
            if parts[i] == "+":
                parts = parts[:i-1] + [float(parts[i-1])+float(parts[i+1])] + parts[i+2:]
                i = max(i-1,0)
            elif parts[i] == "-":
                parts = parts[:i-1] + [float(parts[i-1])-float(parts[i+1])] + parts[i+2:]
                i = max(i-1,0)
            else:
                i += 1
        solution = parts[0]
        if history_record:
            history[equation + f"    {dim("[PEMDAS]")}"] = solution
        return f"Solution: {solution}"
    except IndexError:
        return "Invalid equation format."
    except ValueError:
        return "Invalid equation format."
    except ZeroDivisionError:
        return "Cannot divide by zero."
    
def evaluate_LTR(parts, equation):
    global history_record, history
    if not verify(parts):
        return "Invalid equation format."
    try:
        while len(parts) > 1:
            a,b = float(parts[0]),float(parts[2])
            if parts[1] == "+":
                new = a + b
            elif parts[1] == "-":
                new = a - b
            elif parts[1] == "*":
                new = a * b
            elif parts[1] == "/":
                new = a / b
            elif parts[1] == "^":
                new = a ** b
            else:
                return "Invalid operation used."
            parts = [new] + parts[3:]
        solution = parts[0]
        if history_record:
            history[equation + f"    {dim("[LTR]")}"] = solution
        return f"Solution: {solution}"
    except ValueError:
        return "Invalid operand used."
    except IndexError:
        return "Invalid equation format."
    except ZeroDivisionError:
        return "Cannot divide by zero."
    
def verify(parts):
    if parts[0] in "+-*/^" or parts[-1] in "+-*/^":
        return False
    for i in range(len(parts)): 
        try:
            int(parts[i])
            if i % 2 != 0:
                return False
        except:
            pass
        if parts[i] in "+-*/^" and i % 2 == 0:
            return False
    return True
    
def main():
    while True:
        try: 
            print(calculator(input("\rEquation: ")))
        except KeyboardInterrupt:
            try:
                print(calculator(input(dim("[Ctrl+C again to confirm exit]")+"\nEquation: ")))
            except KeyboardInterrupt:
                print("\n\nProgram closed.\n")
                return


history_record = True
mode = "PEMDAS"
history = {}

print(dim("v2.3 stable"))
print("""\n-Type in equations in the form <operand><space><operation><space><operand> and so on.
-Current operands include: + - * / ^.
-Keyboard interrupt (twice) to exit.
-Type /help (recommended for first use).\n""")

help_text = """
~/History [1]
~/Mode    [2]
~/Example [3]
Type help and then name of the command or its index to get more info.
"""
help_history = f"""
/History: Shows all successfully solved equations in a list. {dim("/h")}
Sub-Commands: 
    History Clear: Clears all history. {dim(("/h c"))}
    History Record: Toggles recording history. {dim("/h r")}
    History Equate: Equates the most recent equation from history. {dim("/h e")}
"""
help_mode = f"""
/Mode: Toggles between Pemdas evaluation and left-to-right evaluation modes. {dim("/m")}
Can also be followed by any equation to switch mode, solve the equation and switch back. {dim("/m <eq>")}
"""
help_example = f"""
/Example: Gives an example equation and solution with all operands except exponents. {dim("/e")}
"""

if __name__ == "__main__":
    main()


# [done] version 1.5: added error handling for invalid input, added error handling for division by zero, added error handling for non-integer input, added error handling for invalid operations, added error handling for missing operands, added error handling for extra operands, added error handling for empty input.
# [done] version 2: added pemdas functionality, added exponents functionality, added and imporved history functionality, added history pause cmd, improve help text, added help cmd, added clear history cmd, added history evaluate cmd, added mode shifting cmd, added quick shift cmd.
# version 3: add variable functionality, add parentheses functionality, add memory [+ - ? ! /] functionality, add command to clear memory (memeory saves to memory.txt).