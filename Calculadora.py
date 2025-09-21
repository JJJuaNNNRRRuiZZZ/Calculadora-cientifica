import tkinter as tk
import math

modo_f2_activo = False
modo_f3_activo = False

def calcular_factorial(n):
    try:
        n = int(float(n))
        if n < 0:
            return "Error"
        if n == 0:
            return 1
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
    except:
        return "Error"

def formatear_resultado(valor):
    """Formatea el resultado para mostrarlo correctamente"""
    try:
        # Si es un número, formatearlo adecuadamente
        num = float(valor)
        
        # Si es entero, mostrarlo sin decimales
        if num.is_integer():
            return str(int(num))
        
        # Si es un decimal, mostrar hasta 10 decimales pero eliminar ceros finales
        resultado = f"{num:.10f}"
        resultado = resultado.rstrip('0').rstrip('.') if '.' in resultado else resultado
        
        # Manejar casos como 0.5 que se convierte en .5
        if resultado.startswith('.'):
            resultado = '0' + resultado
            
        return resultado
        
    except:
        return str(valor)

def evaluar_expresion(expresion):
    """Función que evalúa correctamente todas las operaciones"""
    try:
        if not expresion.strip():
            return "0"
            
        # Manejar factorial
        if '!' in expresion:
            partes = expresion.split('!')
            if len(partes) == 2 and partes[1] == '':
                num = partes[0].strip()
                return formatear_resultado(calcular_factorial(num))
        
        # Manejar raíz cúbica
        if '∛' in expresion:
            partes = expresion.split('∛')
            if len(partes) == 2:
                num = partes[1].strip()
                resultado = float(num) ** (1/3)
                return formatear_resultado(resultado)
        
        # Manejar deg() especialmente
        if 'deg(' in expresion:
            start = expresion.find('deg(')
            end = expresion.find(')', start)
            if start != -1 and end != -1:
                contenido = expresion[start+4:end]
                valor = evaluar_expresion(contenido)  # Evaluar el contenido primero
                resultado = math.degrees(float(valor))
                return formatear_resultado(resultado)
        
        # Manejar rad() especialmente
        if 'rad(' in expresion:
            start = expresion.find('rad(')
            end = expresion.find(')', start)
            if start != -1 and end != -1:
                contenido = expresion[start+4:end]
                valor = evaluar_expresion(contenido)  # Evaluar el contenido primero
                resultado = math.radians(float(valor))
                return formatear_resultado(resultado)
        
        # Reemplazar constantes
        expresion = expresion.replace('π', str(math.pi))
        expresion = expresion.replace('e', str(math.e))
        expresion = expresion.replace('^', '**')
        
        # Crear entorno seguro con todas las funciones
        safe_dict = {
            'math': math,
            '__builtins__': {},
            'sin': lambda x: math.sin(math.radians(float(x))),
            'cos': lambda x: math.cos(math.radians(float(x))),
            'tan': lambda x: math.tan(math.radians(float(x))),
            'asin': lambda x: math.degrees(math.asin(float(x))),
            'acos': lambda x: math.degrees(math.acos(float(x))),
            'atan': lambda x: math.degrees(math.atan(float(x))),
            'log': math.log10,
            'ln': math.log,
            'rad': math.radians,
            'deg': math.degrees,
            'sqrt': math.sqrt
        }
        
        result = eval(expresion, safe_dict)
        return formatear_resultado(result)
        
    except Exception as e:
        return "Error"

funciones_f2 = {
    "7": "sin", "8": "cos", "9": "tan",
    "4": "asin", "5": "acos", "6": "atan",
    "1": "log", "2": "ln", "3": "π", "0": "e"
}

funciones_f3 = {
    "7": "^", "8": "∛", "9": "**",
    "4": "!", "5": "rad", "6": "deg",
    "1": "π", "2": "e", "3": "log", "0": "ln"
}

buttons = [
    "7", "8", "9", "/", 
    "4", "5", "6", "*", 
    "1", "2", "3", "-", 
    "0", ".", "=", "+", 
    "C", "√", "%", "∑"
]

botones_numericos = {}

root = tk.Tk()
root.title("Calculadora Científica")

entry = tk.Entry(root, font=("Helvetica", 20), width=20)
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

def actualizar_texto_botones():
    for btn_text, btn_widget in botones_numericos.items():
        if modo_f3_activo:
            btn_widget.config(text=funciones_f3[btn_text])
        elif modo_f2_activo:
            btn_widget.config(text=funciones_f2[btn_text])
        else:
            btn_widget.config(text=btn_text)

    for widget in root.grid_slaves():
        if widget.cget("text") in ["%", "% ON"]:
            widget.config(text="% ON" if modo_f2_activo else "%", bg="lightblue" if modo_f2_activo else "SystemButtonFace")
        elif widget.cget("text") in ["∑", "∑ ON"]:
            widget.config(text="∑ ON" if modo_f3_activo else "∑", bg="lightgreen" if modo_f3_activo else "SystemButtonFace")

def insertar_funcion_con_parentesis(funcion):
    posicion_actual = entry.index(tk.INSERT)
    entry.insert(tk.INSERT, funcion + "()")
    entry.icursor(posicion_actual + len(funcion) + 1)

def on_click_general(button_text):
    global modo_f2_activo, modo_f3_activo

    if button_text == "=":
        current_text = entry.get()
        result = evaluar_expresion(current_text)
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
        return

    if button_text == "C":
        entry.delete(0, tk.END)
        return

    if button_text == "√":  
        current_text = entry.get()
        if current_text.strip() == "":
            entry.insert(tk.END, "√")
        else:
            result = evaluar_expresion("sqrt(" + current_text + ")")
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        return

    if button_text == "%":
        current_text = entry.get()
        if not modo_f2_activo and current_text.strip() != "":
            try:
                number = float(current_text)
                entry.delete(0, tk.END)
                entry.insert(tk.END, formatear_resultado(number / 100))
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error")
            return
        modo_f2_activo = not modo_f2_activo
        if modo_f2_activo:
            modo_f3_activo = False
        actualizar_texto_botones()
        return

    if button_text == "∑":
        modo_f3_activo = not modo_f3_activo
        if modo_f3_activo:
            modo_f2_activo = False
        actualizar_texto_botones()
        return

    if modo_f2_activo and button_text in funciones_f2:
        funcion = funciones_f2[button_text]
        if funcion in ["sin", "cos", "tan", "asin", "acos", "atan", "log", "ln", "rad", "deg"]:
            insertar_funcion_con_parentesis(funcion)
        else:
            entry.insert(tk.INSERT, funcion)
        return

    if modo_f3_activo and button_text in funciones_f3:
        funcion = funciones_f3[button_text]
        if funcion in ["rad", "deg", "log", "ln"]:
            insertar_funcion_con_parentesis(funcion)
        elif funcion == "∛":
            entry.insert(tk.INSERT, "∛")
        elif funcion == "!":
            current_text = entry.get()
            entry.delete(0, tk.END)
            entry.insert(tk.END, current_text + "!")
        elif funcion == "**":
            entry.insert(tk.INSERT, "^")
        else:
            entry.insert(tk.INSERT, funcion)
        return

    entry.insert(tk.INSERT, button_text)

row = 1
col = 0
for button_text in buttons:
    btn = tk.Button(root, text=button_text, font=("Helvetica", 15), padx=15, pady=15)
    btn.grid(row=row, column=col, padx=2, pady=2)
    btn.config(command=lambda b=button_text: on_click_general(b))
    
    if button_text in "0123456789":
        botones_numericos[button_text] = btn
    
    col += 1
    if col > 3:
        col = 0
        row += 1

actualizar_texto_botones()
root.mainloop()