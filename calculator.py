import tkinter as tk
import ast , operator

root = tk.Tk()
root.title('calculator')
root.geometry("500x300")
expr_var = tk.StringVar(value="")
display = tk.Entry(root, textvariable=expr_var, font=('Arial',20), justify="right",
                   bd=8,relief="ridge", state="readonly",readonlybackground="white")

display.grid(row=0,column=0,columnspan=7, padx=10,pady=10, sticky="nsew")
for r in range(1,6):
    root.grid_rowconfigure(r, weight=1)
for c in range(4):
    root.grid_columnconfigure(c,weight=1)
buttons = [
    ("C",  1, 0), ("(", 1, 1), (")", 1, 2), ("⌫", 1, 3),
    ("7",  2, 0), ("8", 2, 1), ("9", 2, 2), ("/", 2, 3),
    ("4",  3, 0), ("5", 3, 1), ("6", 3, 2), ("*", 3, 3),
    ("1",  4, 0), ("2", 4, 1), ("3", 4, 2), ("-", 4, 3),
    ("0",  5, 0), (".", 5, 1), ("=", 5, 2), ("+", 5, 3),
]
OPS = "+-*/"
def press(token:str):
    s=expr_var.get()
    if token in OPS:
        if not s:
            if token == "-":
                expr_var.set("-")
            return
        if s[-1] in OPS:
            s = s[:-1]+token
            expr_var.set(s)
            return
    expr_var.set(s+token)
#clear and backspace
def clear():
    expr_var.set("")
def backspace():
    s = expr_var.get()
    if s:
        expr_var.set(s[:-1])
#safe evalution
# Allowed operators map
ALLOWED = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,  # unary minus
}

def _eval_ast(node):
    if isinstance(node, ast.Num):            # py<3.8
        return node.n
    if isinstance(node, ast.Constant):       # py>=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Invalid constant")

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return ALLOWED[type(node.op)](_eval_ast(node.operand))

    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED:
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        return ALLOWED[type(node.op)](left, right)

    # Parentheses are handled implicitly by the AST structure
    raise ValueError("Invalid expression")

def safe_eval(expr: str):
    # Basic sanitation: disallow consecutive dots, illegal chars, etc.
    if not expr:
        return ""
    tree = ast.parse(expr, mode="eval")
    return _eval_ast(tree.body)
#evaluate and show result
def evaluate():
    s = expr_var.get()
    # Trim trailing operator like "3+"
    if s and s[-1] in OPS:
        s = s[:-1]
    try:
        result = safe_eval(s)
        # Show integers without .0
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        expr_var.set(str(result))
    except ZeroDivisionError:
        expr_var.set("Error")
    except Exception:
        expr_var.set("Error")
# build button
def on_click(label):
    if label == "C":
        clear()
    elif label == "⌫":
        backspace()
    elif label == "=":
        evaluate()
    else:
        press(label)

for (text, r, c) in buttons:
    tk.Button(
        root, text=text, font=("Arial", 16), bd=2, relief="raised",
        command=lambda t=text: on_click(t)
    ).grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
def on_key(event):
    ch = event.char
    if ch in "0123456789.+-*/()":
        press(ch)
    elif event.keysym in ("Return", "KP_Enter"):
        evaluate()
    elif event.keysym == "BackSpace":
        backspace()
    elif event.keysym in ("Escape", "Delete"):
        clear()

root.bind("<Key>", on_key)



root.mainloop()