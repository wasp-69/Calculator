from random import randint, choice
from json import dump, load
from math import pi, e, sin, cos, tan, asin, acos, atan ,log, log10, fabs, floor, ceil, factorial

def calculator(equation):
    global history_record, history, sequence, detail, variables
    try:
        try:
            parts = equation.split()
        except AttributeError:
            parts = equation
        
        if len(parts) > 1:
            if parts[1] == "=":
                vshvalue = parts[2:]
                parts = ["/v","a",parts[0]]
                for i in vshvalue:
                    parts.append(i)
            elif parts[1] == ":":
                fshvalue =  parts[2:]
                parts = ["/f","a",parts[0],]
                for i in fshvalue:
                    parts.append(i)
        
        try:

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
                return handle_variable(parts)

            elif parts[0].lower() in ["/function","/f"]:
                return handle_function(parts,)
            
        except AttributeError:

            pass

        if "(" in parts:
            return handle_parenthesis(parts)
        
        parts = evaluate_variable(parts)
        if isinstance(parts, str):
            return parts

        parts = evaluate_function(parts)
        if isinstance(parts, str):
            return parts
        
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
                history[" ".join(map(str,equation))] = solution
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
    if str(parts[0]) in "+-*/^" or str(parts[-1]) in "+-*/^":
        return False
    for i in range(len(parts)): 
        try:
            float(str(parts[i]))
            if i % 2 != 0:
                return False
        except ValueError:
            pass
        if str(parts[i]) in "+-*/^" and i % 2 == 0:
            return False
    return True

def handle_help(parts):
    help_text = """
~/History     [1]
~/Sequence    [2]
~/Example     [3]
~/Memory      [4]
~/Detail      [5]
~/Variable    [6]
~/Function    [7]
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
TIP: Can also be followed by any equation to switch sequence, solve the equation and switch back. {dim("/s <eq>")}
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
TIP: While using /Memory Add, you can provide a list and all the items will be added to memory separatley.
    """
    help_detail = f"""
/Detail: Toggles showing steps when solving equations for added detail. {dim("/d")}
TIP: Can also be followed by any equation to get a detailed solution on that equation only. {dim("/d <eq>")}
    """
    help_variable = f"""
/Variable: Lists all variables stored with their values (pi, e, ans are built-in). {dim("/v")}
Sub-Commands:
    /Variable Define <name> <value>: Define a new variable with name and value. {dim("/v d")}
    /Variable Forget <name>: Forget the definition of the given variable. {dim("/v f")}
    /Variable Wipe: Wipe all variable definitions. {dim("/v w")}
TIP: Typing 'name = value' creates a new variable "name" with "value".
"""
    help_function = f"""
/Function:  Lists all functions names and their definitions (program includes several built-in functions). {dim("/f")}
Sub-Commands:
    /Function <name>: Shows the definition and description of the given function. {dim("/f <name>")}
    /Function Add <name> <definition>: Adds a new function with the given name and definition. {dim("/f a")}
    /Function Description <name> <description>: Adds a description to the given function. {dim("/f d")}
    /Function Remove <name>: Removes the given function. {dim("/f r")}
    /Function Clear: Removes all user-defined functions. {dim("/f c")}
TIP: Typing 'name : definition' creates a new function "name" with "definition".
"""
    
    if len(parts) == 1:
        return help_text
    elif parts[1].lower().lstrip("~/") in ["history","h","1","[1]"]:
        return help_history
    elif parts[1].lower().lstrip("~/") in ["sequence","s","2","[2]"]:
        return help_sequence
    elif parts[1].lower().lstrip("~/") in ["example","e","3","[3]"]:
        return help_example
    elif parts[1].lower().lstrip("~/") in ["memory","m","4","[4]"]:
        return help_memory
    elif parts[1].lower().lstrip("~/") in ["detail","d","5","[5]"]:
        return help_detail
    elif parts[1].lower().lstrip("~/") in ["variable","v","6","[6]"]:
        return help_variable
    elif parts[1].lower().lstrip("~/") in ["function","f","7","[7]"]:
        return help_function
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
        return f"There are {len(history)} equations currently recorded in history."
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
        with open("MAIN\\memory.txt","w") as file:
                dump(memory, file)
        print(dim("~ ~ ~ ~ ~\n"),"\n".join(memory).strip(),dim("\n~ ~ ~ ~ ~"))
        return f"Memory contains {len(memory)} entries currently."

    elif parts[1].lower() in ["add","a"]:
        if len(parts) == 2:
            try:
                memory.append(list(history)[-1])
            except IndexError:
                return "No equation found to add to memory, provide one or have one in history."
        else:
            del parts[0:2]
            subject = " ".join(list(map(str, parts)))
            if subject.startswith("[") and subject.endswith("]"):
                subject = subject.removeprefix("[").removesuffix("]")
                for i in subject.split(","):
                    element = i.strip(" '\"")
                    memory.append(element)
            else:
                memory.append(subject.strip())
        with open("MAIN\\memory.txt","w") as file:
            dump(memory, file)
        return "Memory updated!"

    elif parts[1].lower() in ["remove","r"]:
        if len(memory) == 0:
            return "Memory is empty."
        if len(parts) == 2:
            removed_item = memory.pop()
            with open("MAIN\\memory.txt","w") as file:
                dump(memory, file)
            return f"'{removed_item}' has been removed from memory."
        del parts[0:2]
        try:
            memory.remove(" ".join(parts))
            with open("MAIN\\memory.txt","w") as file:
                dump(memory, file)
            return f"'{" ".join(parts)}' has been removed from memory."
        except ValueError:
            return f"'{" ".join(parts)}' not found in memory."
        
    elif parts[1].lower() in ["clear","c"]:
        with open("MAIN\\memory.txt","w") as file:
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
        parts.pop(0)
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
    global detail
    parts = evaluate_variable(parts)
    if not verify_parenthesis(parts):
        return "Invalid parenthesis."
    while "(" in parts:
        op_index = len(parts) - 1
        cl_index = 0
        for i in reversed(parts):
            if i == "(":
                break
            else:
                op_index -= 1
        try:
            if (is_float(parts[op_index-1]) or parts[op_index-1].endswith(")")) and op_index != 0:
                parts.insert(op_index, "*")
                op_index += 1
        except IndexError:
            pass
        for i in parts:
            if i == ")":
                if cl_index > op_index:
                    break
                else: 
                    cl_index += 1
            else:
                cl_index += 1
        try:
            if (is_float(parts[cl_index+1]) or parts[cl_index+1].startswith("(")) and cl_index+1 != 0:
                parts.insert(cl_index+1, "*")
        except IndexError:
            pass
        between = slice(op_index+1,cl_index)
        if detail:
            print(dim(f" = {" ".join(map(str,parts))}"))
        temp_detail = detail
        if detail:
            detail = False
        if not calculator(parts[between]).startswith("Solution: "):
            return calculator(parts[between]).removeprefix("Solution: ")
        parts = parts[:op_index] + calculator(parts[between]).removeprefix("Solution: ").split() + parts[cl_index+1:]
        detail = temp_detail
    if detail:
        print(dim(f" = {" ".join(map(str,parts))}"))
    return calculator(parts)

def handle_variable(parts):
    global variables
    if len(parts) == 1:
        print(dim("▪ ▪ ▪ ▪ ▪"))
        for name, value in variables.items():
            print(f"{name} = {value}")
        print(dim("▪ ▪ ▪ ▪ ▪"))
        return f"There are {len(variables)} defined variables."
    elif parts[1].lower() in ["add","a"]:
        name, value = parts[2], calculator(parts[3:]).removeprefix("Solution: ")
        if is_float(name) or any(item in name for item in list("+-*/^()")):
            return "Invalid variable name, must be a string without any operands or parenthesis."
        try:
            value = float(value)
        except ValueError:
            return "Invalid variable value."
        variables[name] = value
        return f"New variable '{name}' with the value '{value}' defined."
    elif parts[1].lower() in ["remove","r"]:
        if variables.pop(parts[2], False):
            return f"Forgot the definition of '{parts[2]}'."
        return f"No variable found with the name '{parts[2]}' to remove."
    elif parts[1].lower() in ["clear","c"]:
        variables = {}
        return "All variable definitions cleared."
    else:
        return f"No action available for '{" ".join(parts)}'."

def evaluate_variable(parts):
    global detail
    func_list = {**functions_builtin, **functions}
    temp_parts = []
    for index, i in enumerate(parts):
        if str(parts[index-1]) not in "+-*/^([" and i in variables and index != 0:
            if str(parts[index-1]) not in func_list:
                temp_parts.append("*")
        temp_parts.append(i)
    if detail:
        print(dim(f" = {" ".join(map(str,temp_parts))}"))
    for index, i in enumerate(temp_parts):
        if i in variables:
            temp_parts[index] = variables[i]
    return temp_parts

def handle_function(parts):
    global functions_builtin, functions
    func_list = {**functions_builtin, **functions}
    if len(parts) == 1:
        print(dim("◊ ◊ ◊ ◊ ◊"))
        for name, definition in func_list.items():
            print(f"{name} : {definition[0]}")
        print(dim("◊ ◊ ◊ ◊ ◊"))
        return f"There are {len(func_list)} defined functions."
    elif parts[1] in func_list:
        try:
            return f"{func_list[parts[1]][0]} : {func_list[parts[1]][1]}"
        except IndexError:
            return f"No description for {func_list[parts[1]][0]}"
    elif parts[1].lower() in ["add","a"]:
        name, definition = parts[2], parts[3:]
        if name.isdigit() or any(item in name for item in list("+-*/^()[]")):
            return "Invalid function name, must be a string without any operands or brackets."
        if name in functions_builtin:
            return "Invalid function name, such function comes built in."
        functions[name] = [" ".join(definition), "No description provided."]
        return f"Function {name} successfully added."
    elif parts[1].lower() in ["description","d"]:
        if parts[2] in functions:
            functions[parts[2]].append(" ".join(parts[3:]))
            return f"Description for {parts[2]} added."
        return f"Function {parts[2]} doesnt exist."
    elif parts[1].lower() in ["remove","r"]:
        if parts[2] in functions:
            functions.pop(parts[2])
            return f"Function {parts[2]} removed."
        return f"Function {parts[2]} doesnt exist."
    elif parts[1].lower() in ["clear","c"]:
        functions.clear()
        return "All functions removed."

def evaluate_function(parts):
    global functions, functions_builtin, detail
    func_list = {**functions_builtin, **functions}
    evaluated_parts = []
    for index, i in enumerate(parts):
        if str(parts[index-1]) not in "+-*/^([" and i in func_list and index != 0:
            evaluated_parts.append("*")
        evaluated_parts.append(i)
    if detail:
        print(dim(f" = {" ".join(map(str,parts))}"))
    parts = evaluated_parts.copy()
    evaluated_parts = []
    for index, i in enumerate(reversed(parts)):
        if i in func_list:
            continue
        try:
            if list(reversed(parts))[index+1] in functions_builtin:
                evaluated_parts.append(globals()[list(reversed(parts))[index+1]](float(i)))
            elif list(reversed(parts))[index+1] in functions:
                temp_detail = detail
                if detail:
                    detail = False
                sol = calculator(functions[list(reversed(parts))[index+1]][0].replace("x",str(i)))
                detail = temp_detail
                if sol.startswith("Solution: "):
                    sol = sol.removeprefix("Solution: ")
                else:
                    return sol
                evaluated_parts.append(sol)
            else:
                evaluated_parts.append(i)
        except TypeError:
            try:
                evaluated_parts.append(globals()[list(reversed(parts))[index+1]](int(i)))
            except ValueError:
                return f"Invalid argument for function."
        except ValueError:
            return f"Invalid argument for function."
        except IndexError:
            evaluated_parts.append(i)
    return list(reversed(evaluated_parts))     

def is_float(test):
    try:
        float(test)
        return True
    except (ValueError, TypeError):
        return False
    
def dim(string):
    return "\033[2m"+str(string)+"\033[0m"

def main():
    global recursion_counter, inf_rec_var, variables
    print(dim("v3.0"))
    print(start_text)
    while True:
        try: 
            if inf_rec_var:
                print("Infinite Recursion Terminated.")
                inf_rec_var = False
            recursion_counter = 0
            output = calculator(input("\rEquation: "))
            if output.startswith("Solution: "):
                variables["ans"] = output.removeprefix("Solution: ")
            print(output)
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
variables = {"pi": pi, "e": e, "ans": 0}
functions_builtin = {
    "sin": [sin, "sine function, usage: sin ( angle in radians )"],
    "cos": [cos, "cosine function, usage: cos ( angle in radians )"],
    "tan": [tan, "tangent function, usage: tan ( angle in radians )"],
    "asin": [asin, "arcsine function, usage: asin ( value )"],
    "acos": [acos, "arccosine function, usage: acos ( value )"],
    "atan": [atan, "arctangent function, usage: atan ( value )"],
    "log": [log, "natural logarithm function, usage: log ( value )"],
    "log10": [log10, "base-10 logarithm function, usage: log10 ( value )"],
    "fabs": [fabs, "absolute value function, usage: fabs ( value )"],
    "floor": [floor, "floor function, usage: floor ( value )"],
    "ceil": [ceil, "ceiling function, usage: ceil ( value )"],
    "factorial": [factorial, "factorial function, usage: factorial ( value )"]
}
functions = {}
with open("MAIN\\memory.txt","r") as file:
    memory = list(load(file))

start_text = """\n-Type in equations in the form <operand><space><operation><space><operand> and so on (e.g. '2 * 3 + 4').
-Parenthesis must have a space on both sides of it (e.g. '2 * ( 3 + 4 )').
-Variables and functions mustnt share the same name and are case-sensitive.
-Functions have 'x' as the independent variable or its argument (e.g. 'f: x^2 + 3x + 2').
-To use functions, type in the name followed by its argument with or without parenthesis (e.g. 'sin 1' or 'sin(1)').
-Implicit multiplication is supported (e.g. 'pi ( 3 e + 4 )' or '2 sin ( 1 )').
-Current operands include: + - * / ^.
-Keyboard interrupt (twice) to exit.
-Type /help (recommended for first use).\n"""



if __name__ == "__main__":
    main()


# [done] version 1.5: added error handling for invalid input, added error handling for division by zero, added error handling for non-integer input, added error handling for invalid operations, added error handling for missing operands, added error handling for extra operands, added error handling for empty input.
# [done] version 2: added pemdas functionality, added exponents functionality, added and imporved history functionality, added history pause cmd, improve help text, added help cmd, added clear history cmd, added history evaluate cmd, added sequence shifting cmd, added quick shift cmd.
# [done] version 3: added variable functionality, added parentheses functionality, added memory functionality (memory saves to MAIN\\memory.txt), added function support, added a mode to show solution steps, added memory packages with [].
