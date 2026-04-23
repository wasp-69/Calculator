from random import randint, choice
from json import dump, load

def calculator(equation):
    global history_record, history, sequence
    try:
        try:
            parts = equation.split()
        except AttributeError:
            parts = equation
        if "(" in parts or ")" in parts:
            return handle_parenthesis(parts)
        
        if parts[0].lower() == "/help":
            return handle_help(parts)

        elif parts[0].lower() in ["/example","/e"]:
            return handle_example()
        
        elif parts[0].lower() in ["/history","/h"]:
            return handle_history(parts)

        elif parts[0].lower() in ["/sequence","/s"]:
            return handle_sequence(parts)

        elif parts[0].lower() in ["/memory","/m"]:
                return handle_memory(parts, history)

        elif parts[0].lower() in ["/detail","/d"]:
            return handle_detail(parts)

        elif parts[0].lower() in ["/variable","/v"]:
            return handle_variable(parts,)

        elif parts[0].lower() in ["/function","/f"]:
            return handle_variable(parts,)

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
                if detail:
                    print(dim(" = " + " ".join(list(map(str, parts)))))
                i += 1
            else:
                i -= 1
        i = 0
        while i < len(parts):
            if parts[i] == "*":
                parts = parts[:i-1] + [float(parts[i-1])*float(parts[i+1])] + parts[i+2:]
                if detail:
                    print(dim(" = " + " ".join(list(map(str, parts)))))
                i = max(i-1,0)
            elif parts[i] == "/":
                parts = parts[:i-1] + [float(parts[i-1])/float(parts[i+1])] + parts[i+2:]
                if detail:
                    print(dim(" = " + " ".join(list(map(str, parts)))))
                i = max(i-1,0)
            else: 
                i += 1
        i = 0
        while i < len(parts):
            if parts[i] == "+":
                parts = parts[:i-1] + [float(parts[i-1])+float(parts[i+1])] + parts[i+2:]
                if detail:
                    print(dim(" = " + " ".join(list(map(str, parts)))))
                i = max(i-1,0)
            elif parts[i] == "-":
                parts = parts[:i-1] + [float(parts[i-1])-float(parts[i+1])] + parts[i+2:]
                if detail:
                    print(dim(" = " + " ".join(list(map(str, parts)))))
                i = max(i-1,0)
            else:
                i += 1
        solution = parts[0]
        if history_record:
            try:
                history[equation] = solution
            except TypeError:
                history[" ".join(equation)] = solution
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
                parts = [a+b] + parts[3:]
                if detail:
                    print(dim(" = " + " ".join(list(map(str, parts)))))
            elif parts[1] == "-":
                parts = [a-b] + parts[3:]
                if detail:
                    print(dim(" = " + " ".join(list(map(str, parts)))))
            elif parts[1] == "*":
                parts = [a*b] + parts[3:]
                if detail:
                    print(dim(" = " + " ".join(list(map(str, parts)))))
            elif parts[1] == "/":
                parts = [a/b] + parts[3:]
                if detail:
                    print(dim(" = " + " ".join(list(map(str, parts)))))
            elif parts[1] == "^":
                parts = [a**b] + parts[3:]
                if detail:
                    print(dim(" = " + " ".join(list(map(str, parts)))))
            else:
                return "Invalid operation used."
        solution = parts[0]
        if history_record:
            history[equation] = solution
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
~/Detail      [5]
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
    /Memory Limit: Sets the Max Recursion Limit to specified value (default 100). {dim("/m l")}
    """
    help_detail = f"""
/Detail: Toggles showing steps when solving equations for added detail. {dim("/d")}
Can also be followed by any equation to get a detailed solution on that equation only. {dim("/d <eq>")}
    """

    if len(parts) == 1:
        return help_text
    elif parts[1].lower() in ["/history","/h","history","h","1","[1]"]:
        return help_history
    elif parts[1].lower() in ["/sequence","/s","sequence","s","2","[2]"]:
        return help_sequence
    elif parts[1].lower() in ["/example","/e","example","e","3","[3]"]:
        return help_example
    elif parts[1].lower() in ["/memory","/m","memory","m","4","[4]"]:
        return help_memory
    elif parts[1].lower() in ["/detail","/d","detail","d","5","[5]"]:
        return help_detail
    else:
        return f"No help topic found for '{parts[1]}'."

def handle_example():
    example = ""
    for i in range((randint(1,20)*2)+1):
        example += str(randint(1,1000)) + " " + choice(["+","-","*","/"]) + " "
    example += str(randint(1,1000))
    return f"Example Equation: {example} [{dim(calculator(example))}]"

def handle_history(parts):
    global history, history_record
    if len(parts) == 1:
        print(dim("- - - - -"))
        for eq, ans in history.items():
            print(f"Equation: {eq}\nSolution: {ans}")
        print(dim("- - - - -"))
        return f"{len(history)} equations currently recorded in history."
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

def handle_sequence(parts):
    global sequence
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

def handle_memory(parts, history):
    global memory, recursion_counter, inf_rec_var, max_rec_lim
    if len(parts) == 1:
        with open("MAIN/memory.txt","w") as file:
                dump(memory, file)
        print(dim("~ ~ ~ ~ ~\n"),"\n".join(memory),dim("\n~ ~ ~ ~ ~"))
        return f"Memory contains {len(memory)} entries currently."

    elif parts[1].lower() in ["add","a"]:
        if len(parts) == 2:
            try:
                memory.append(list(history)[-1])
            except IndexError:
                return "No equation found to add to memory, provide one or have one in history."
        else:
            del parts[0:2]
            memory.append(" ".join(list(map(str, parts))))
        with open("MAIN/memory.txt","w") as file:
            dump(memory, file)
        return "Memory updated!"

    elif parts[1].lower() in ["remove","r"]:
        if len(memory) == 0:
            return "Memory is empty."
        if len(parts) == 2:
            removed_item = memory.pop()
            with open("MAIN/memory.txt","w") as file:
                dump(memory, file)
            return f"'{removed_item}' has been removed from memory."
        del parts[0:2]
        try:
            memory.remove(" ".join(parts))
            with open("MAIN/memory.txt","w") as file:
                dump(memory, file)
            return f"'{" ".join(parts)}' has been removed from memory."
        except ValueError:
            return f"'{" ".join(parts)}' not found in memory."
        
    elif parts[1].lower() in ["clear","c"]:
        with open("MAIN/memory.txt","w") as file:
            memory.clear()
            dump(memory, file)
            return "Memory has been cleared."

    elif parts[1].lower() in ["solve","s"]:
        no_of_eqs = len(memory)
        print(dim(". . . . ."))
        for equation in memory:
            if equation.lower() in ["/memory solve","/m solve","/memory s","/m s"]:
                recursion_counter += 1
            if recursion_counter != int(max_rec_lim):
                print("Equation: ", equation)
                print(calculator(equation))
            else:
                inf_rec_var = True
                break
        print(dim(". . . . ."))
        return f"Solved all {no_of_eqs} equations."

    elif parts[1].lower() in ["limit","l"]:
        if len(parts) == 2:
            max_rec_lim = 100
            return f"Maximum Recursion Limit is now set to {max_rec_lim}."
        else:
            if not parts[2].isdigit():
                return "Invalid recursion limit provided."
            if int(parts[2]) < 0 or int(parts[2]) > 1000:
                return "Recursion Limit must be between 1 and 1000."
            max_rec_lim = parts[2]
            return f"Maximum Recursion Limit is now set to {max_rec_lim}."
        
    else:
        return f"No action available for '{parts[1]}'."

def handle_detail(parts):
    global detail
    if detail:
        detail = False
    else:
        detail = True
    if len(parts) == 1:
        return f"Detailing has now been set to {bool(detail)}."
    else:
        parts[0] == parts[0].lower()
        try:
            parts.remove("/d")
        except:
            parts.remove("/detail")
        solution = calculator(parts)
        if detail:
            detail = False
        else:
            detail = True
        return solution

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

def handle_parenthesis(parts):
    if not verify_parenthesis(parts):
        return "Invalid parenthesis."
    while "(" in parts:
        found = False
        op_index = len(parts) - 1
        cl_index = 0
        for i in reversed(parts):
            if i == "(":
                break
            else:
                op_index -= 1
        for i in parts:
            if i == ")":
                if cl_index > op_index:
                    break
                else: 
                    cl_index += 1
            else:
                cl_index += 1
        between = slice(op_index+1,cl_index)
        parts = parts[:op_index] + calculator(parts[between]).removeprefix("Solution: ").split() + parts[cl_index+1:]
    return calculator(parts)

def handle_variable(parts):
    ...

def handle_funtion(parts):
    ...

def dim(string):
    return "\033[2m"+str(string)+"\033[0m"

def main():
    global recursion_counter, inf_rec_var
    print(dim("v2.6")) # working on 3.0 push
    print(start_text)
    while True:
        try: 
            if inf_rec_var:
                print("Infinite Recursion Terminated.")
                inf_rec_var = False
            recursion_counter = 0
            print(calculator(input("\rEquation: ")))
        except KeyboardInterrupt:
            try:
                print(calculator(input(dim("[Ctrl+C again to confirm exit]")+"\nEquation: ")))
            except KeyboardInterrupt:
                print("\n\nProgram closed.\n")
                return


history_record = True
sequence = "PEMDAS"
detail = False
inf_rec_var = False
max_rec_lim = 100
history = {}
memory = []
with open("MAIN/memory.txt","r") as file:
    memory = list(load(file))

start_text = """\n-Type in equations in the form <operand><space><operation><space><operand> and so on.
-Current operands include: + - * / ^.
-Keyboard interrupt (twice) to exit.
-Type /help (recommended for first use).\n"""



if __name__ == "__main__":
    main()


# [done] version 1.5: added error handling for invalid input, added error handling for division by zero, added error handling for non-integer input, added error handling for invalid operations, added error handling for missing operands, added error handling for extra operands, added error handling for empty input.
# [done] version 2: added pemdas functionality, added exponents functionality, added and imporved history functionality, added history pause cmd, improve help text, added help cmd, added clear history cmd, added history evaluate cmd, added sequence shifting cmd, added quick shift cmd.
# version 3: add variable functionality, add parentheses functionality, added memory functionality (memory saves to memory.txt), add function support, add a mode to show solution steps. 