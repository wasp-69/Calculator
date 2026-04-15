from random import randint, choice

def calculator(equation):
    global history_record, history, sequence
    try:
        parts = equation.split()
        if parts[0].lower() == "/help":
            return handle_help(parts)

        elif parts[0].lower() in ["/example","/e"]:
            return handle_example()
        
        elif parts[0].lower() in ["/history","/h"]:
            return handle_history(parts, history, history_record)
            
        elif parts[0].lower() in ["/sequence","/s"]:
            return handle_sequence(parts, sequence)
        else:
            if sequence == "LTR":
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
    
def handle_help(parts):
    help_text = """
    ~/History     [1]
    ~/Sequence    [2]
    ~/Example     [3]
    ~/Memory      [4]
    Type help and then name of the command or its index to get more info.
    """
    help_history = f"""
    /History: Shows all successfully solved equations in a list. {dim("/h")}
    Sub-Commands: 
        /History Clear: Clears all history. {dim(("/h c"))}
        /History Record: Toggles recording history. {dim("/h r")}
        /History Equate: Equates the most recent equation from history. {dim("/h e")}
    """
    help_sequence = f"""
    /Sequence: Toggles between Pemdas evaluation and left-to-right evaluation sequences. {dim("/s")}
    Can also be followed by any equation to switch sequence, solve the equation and switch back. {dim("/s <eq>")}
    """
    help_example = f"""
    /Example: Gives an example equation and solution with all operands except exponents. {dim("/e")}
    """
    help_memory = f"""
    /Memory: Lists the Memory (memory saves to file). {dim("/m")}
    Sub-Commands:
        /Memory Add <eq>: Saves the provided equation to memory, saves the most recent one in history if no equation given. {dim("/m a")}
        /Memory Remove <eq>: Removes the provided equation from memory, removes the most recent one in memory if no equation given. {dim("/m r")}
        /Memory Clear: Clears all equations from memory. {dim("/m c")}
        /Memory Solve: Starts solving all equations in memory in order. {dim("/m s")}
    """

    if len(parts) == 1:
        return help_text
    elif parts[1].lower() in ["/history","/h","history","h","1"]:
        return help_history
    elif parts[1].lower() in ["/sequence","/s","sequence","s","2"]:
        return help_sequence
    elif parts[1].lower() in ["/example","/e","example","e","3"]:
        return help_example
    elif parts[1].lower() in ["/memory","/m","memory","m","4"]:
        return help_memory
    else:
        return f"No help topic found for '{parts[1]}'."

def handle_example():
    example = ""
    for i in range((randint(1,20)*2)+1):
        example += str(randint(1,1000)) + " " + choice(["+","-","*","/"]) + " "
    example += str(randint(1,1000))
    return f"Example Equation: {example} [{dim(calculator(example))}]"

def handle_history(parts, history, history_record):
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

def handle_sequence(parts, sequence):
    if len(parts) == 1:
        if sequence == "LTR":
            sequence = "PEMDAS"
            return "Now evaluating with PEMDAS sequence."
        else:
            sequence = "LTR"
            return "Now evaluating with Left-to-Right sequence."
    else:
        parts[0] = parts[0].lower()
        if sequence == "LTR":
            try:
                parts.remove("/s")
            except ValueError:
                parts.remove("/sequence")
            return evaluate_PEMDAS(parts, " ".join(parts))
        else:
            try:
                parts.remove("/s")
            except ValueError:
                parts.remove("/sequence")
            return evaluate_LTR(parts, " ".join(parts))

def dim(string):
    return "\033[2m"+string+"\033[0m"

def main():
    print(dim("v2.49 stable")) # working on 3.0 push
    print(start_text)
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
sequence = "PEMDAS"
history = {}
memory = {}

start_text = """\n-Type in equations in the form <operand><space><operation><space><operand> and so on.
-Current operands include: + - * / ^.
-Keyboard interrupt (twice) to exit.
-Type /help (recommended for first use).\n"""


if __name__ == "__main__":
    main()


# [done] version 1.5: added error handling for invalid input, added error handling for division by zero, added error handling for non-integer input, added error handling for invalid operations, added error handling for missing operands, added error handling for extra operands, added error handling for empty input.
# [done] version 2: added pemdas functionality, added exponents functionality, added and imporved history functionality, added history pause cmd, improve help text, added help cmd, added clear history cmd, added history evaluate cmd, added sequence shifting cmd, added quick shift cmd.
# version 3: add variable functionality, add parentheses functionality, add memory functionality (memory saves to memory.txt), add function support.
