import sys
import time

STATE_SIZE = 50000

def is_repeatable(t):
    return "INC" in t or "DEC" in t or "RIGHT" in t or "LEFT" in t

def write_repeatable(out, t, count):
    match t:
        case "INC":
            out += ["+" for i in range(count)]
            return True
        case "DEC":
            out += ["-" for i in range(count)]
            return True
        case "RIGHT":
            out += [">" for i in range(count)]
            return True
        case "LEFT":
            out += ["<" for i in range(count)]
            return True
        case _:
            return False

def compile(file_path):
    output = []
    file = open(file_path, "r")
    tokens = file.read().split("\n")
    file.close()
    cur = 0
    for token in tokens:
        cur += 1
        token = token.strip()
        match token:
            case token if len(token) == 0:
                continue
            case token if token[0] == "#":
                continue
            case token if is_repeatable(token):
                t_split = token.split()
                op = t_split[0]
                if len(t_split) == 2:
                    count = int(t_split[1])
                elif len(t_split) == 1:
                    count = 1
                else:
                    print(f"ERROR: {file_path}, line {cur}: Incorrect usage of {op}")
                    return False
					
                if not write_repeatable(output, op, count):
                    raise RuntimeError(f"\n\t{file_path}, Line {cur}: Unreachable")
					
            case "LOOP":
                output += ["["]
            case "ENDLOOP":
                output += ["]"]
            case "OUT":
                output += ["."]
            case "IN":
                output += [","]
            case _:
                print(f"ERROR: {file_path}, line {cur}: Unknown token: {token}")
                return False
		
    return "".join(output)

def inc(num):
    if num == 255:
        return 0
    else:
        return num + 1

def dec(num):
    if num == 0:
        return 255
    else:
        return num - 1

def checked_input():
    result = input()
    try:
        result = int(result)
    except ValueError:
        return False

    if result > 255 or result < 0:
        return False
    else:
        return result

def get_key_by_val(d, val):
    for key in d.keys():
        if d.get(key) == val:
            return key
    return None
    
def eval(code):
    state = [0 for i in range(STATE_SIZE)]
    cursor = 0
    loop_bounds = dict()
    col = 0
    while col < len(code):
        command = code[col]
        match command:
            case ">":
                cursor += 1
                col += 1
            case "<":
                cursor -= 1
                col += 1
            case "+":
                state[cursor] = inc(state[cursor])
                col += 1
            case "-":
                state[cursor] = dec(state[cursor])
                col += 1
            case ".":
                print(chr(state[cursor]), end="")
                col += 1
            case ",":
                state[cursor] = checked_input()
                col += 1
            case "[":
                if loop_bounds.get(col) is None:
                    closing_idx = col
                    count_open_braces = 1
                    while count_open_braces > 0:
                        closing_idx += 1
                        if closing_idx == len(code):
                            print(f"\nERROR: char {col}: Unclosed loop")
                            return False
                    
                        if code[closing_idx] == "[":
                            count_open_braces += 1
                        elif code[closing_idx] == "]":
                            count_open_braces -= 1

                        if count_open_braces < 0:
                            print(f"\nERROR: char {closing_idx}: Unmatched brace")
                            return False
                        
                    loop_bounds[col] = closing_idx

                elif state[cursor] == 0:
                    col = loop_bounds[col] + 1

                else:
                    col += 1

            case "]":
                opening_idx = get_key_by_val(loop_bounds, col)
                if opening_idx is None:
                    raise RuntimeError(f"\n\tERROR: char {col}: Unreachable")
                
                if state[cursor] == 0:
                    col += 1
                    del loop_bounds[opening_idx]
                else:
                    col = opening_idx
    return True
                
def main():
    file_path = sys.argv[1]
    parsed = compile(file_path)
    print(parsed)
    if not parsed:
        sys.exit(1)
    if not eval(parsed):
        sys.exit(1)
	
if __name__ == "__main__":
    main()
