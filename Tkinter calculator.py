"""
Смысл даже есть там, где кажется его нет
Недопонятые баги:
    1)Операции возведения в степень с минусом
    2)Процент от числа (переход в экспоненциальную форму -> повторная операция берет
    процент от степени а не от всего числа)
"""
import time as t
import tkinter as tk
import math
from decimal import Decimal
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

rt = tk.Tk()
rt.geometry("870x400+300+250")
rt.title('PyCalc')
rt.resizable(False, False)
operators = '0.+-*/^'
operation = ''
expression = ''
number = ''
result = ''
f = ''


def addDigit(digit):
    global expression, operation
    getEntrysContent()
    try:
        if expression[0] == '0' and '.' not in expression:
            expression = expression[1:]
        if digit == 'Pi':
            digit = str(math.pi) if operation in '+-*/' else '*' + str(math.pi)
            operation = 'not true'  # Фикс бага с '' ('' в чём либо ('' in '123abc+-') всегда даёт true)
        elif digit == 'e':
            digit = str(math.e) if operation in '+-*/' else '*' + str(math.e)
            operation = 'not true'
    except:
        if digit == 'Pi':
            digit = str(math.pi)
        elif digit == 'e':
            digit = str(math.e)
    entry.delete(0, tk.END)
    entry.insert(0, expression + digit)
    getEntrysContent()
    extractNumber()


def addOperation(oprn):  # operation
    global expression, number, operation
    getEntrysContent()
    extractNumber()
    operation = oprn

    if oprn in '+-*/':
        number = ''
    try:
        if expression[-1] in '.+-*/':
            expression = expression[:-1]
            number = ''
    except IndexError:
        entry.insert(0, '0')
    if oprn == '.':
        if '.' in number:
            oprn = ''
        number += oprn
        entry.delete(0, tk.END)
        entry.insert(0, '0' + expression + oprn)

    elif oprn == '√':
        try:
            entry.delete(len(expression) - len(number), tk.END)
            oprn = str(math.sqrt(Decimal(number)))
            getEntrysContent()
            archive.config(state=tk.NORMAL)
            archive.insert(1.0, f'√({number})' + ' = ' + oprn + '\n')
            archive.config(state=tk.DISABLED)
        except:
            tk.messagebox.showerror(title='Ошибка квадратного корня числа',
                                    message="Не получилось взять корень от числа.")
            oprn = ''
            entry.insert(0, '0')
    elif oprn == '^':
        oprn = '**'
        if '*' in expression:
            oprn = ''
    elif oprn == '%':
        try:
            entry.delete(len(expression) - len(number), tk.END)
            oprn = str(Decimal(number) / 100)
            getEntrysContent()
            archive.config(state=tk.NORMAL)
            archive.insert(1.0, f'%({number})' + ' = ' + oprn + '\n')
            archive.config(state=tk.DISABLED)
        except:
            tk.messagebox.showerror(title='Ошибка процента числа', message="Не получилось взять "
                                                                           "процент от числа.")
            oprn = ''

    elif oprn == 'div':
        try:
            entry.delete(len(expression) - len(number), tk.END)
            oprn = str(Decimal(number) // 1)
            getEntrysContent()
            archive.config(state=tk.NORMAL)
            archive.insert(1.0, f'div({number})' + ' = ' + oprn + '\n')
            archive.config(state=tk.DISABLED)
        except:
            tk.messagebox.showerror(title='Ошибка операции', message="Не получилось взять "
                                                                     "целую часть от числа.")
            oprn = ''
    elif oprn == 'mod':
        try:
            entry.delete(len(expression) - len(number), tk.END)
            oprn = str(Decimal(number) % 1)
            getEntrysContent()
            archive.config(state=tk.NORMAL)
            archive.insert(1.0, f'mod({number})' + ' = ' + oprn + '\n')
            archive.config(state=tk.DISABLED)
        except:
            tk.messagebox.showerror(title='Ошибка операции', message="Не получилось взять "
                                                                     "дробную часть от "
                                                                     "числа.")
            oprn = ''
    entry.delete(0, tk.END)
    entry.insert(0, expression + str(oprn))
    extractNumber()


def calc():
    global result
    getEntrysContent()
    entry.delete(0, tk.END)
    try:
        # round как костыль из-за особенности счисления float (0.1+0.1+0.1 = 0.30000000000000004...)
        result = str(round(eval(expression), 16))
        entry.insert(0, result)
        extractNumber()
        archive.config(state=tk.NORMAL)
        archive.insert(1.0, expression + ' = ' + result + '\n')
        archive.config(state=tk.DISABLED)
    except:
        entry.insert(0, expression)
        if not entry.get():
            print(entry.get())
            entry.insert(0, '0')
        tk.messagebox.showerror(title='Ошибка', message='Ошибка вычисления')


def saveResult():
    global f
    try:
        f = open('Вычисления pycalc' + '.txt', 'a', encoding='utf-8')
        f.writelines(
            '\nДата: ' + f'{t.strftime("%B/%a/%Y - %H:%M:%S", t.localtime())}\n' + archive.get(1.0, tk.END).strip())
    except:
        tk.messagebox.showerror(title='Ошибка сохранения', message="Возможно, выражение введено "
                                                                   "некорректно")
    f.flush()
    f.close()


def getEntrysContent():
    global expression
    expression = entry.get()


def extractNumber():
    global number
    number = ''
    for i in range(1, len(expression) + 1):
        if expression[-i] not in '+-*/':
            number += expression[-i]
        else:
            break
    number = number[::-1]
    return number


def createDigitButton(digit):
    return tk.Button(rt, text=digit, font=('Arial', 14), bd=4,
                     command=lambda: addDigit(digit))


def createOperatorButton(oper):  # operator
    return tk.Button(rt, text=oper, font=('Arial', 14), bd=4,
                     command=lambda: addOperation(oper))


def removeChar():
    global number, expression
    entry.delete(len(entry.get()) - 1)
    number = number[:-1]
    if not entry.get():
        entry.insert(0, '0')
    getEntrysContent()
    extractNumber()


def clearEntry():
    global number, expression, operation
    entry.delete(0, tk.END)
    entry.insert(0, '0')
    number = ''
    operation = ''
    getEntrysContent()
    archive.config(state=tk.NORMAL)
    archive.delete(1.0, tk.END)
    archive.config(state=tk.DISABLED)


entry = tk.Entry(rt, font=('Arial', 22), bd=10, justify=tk.RIGHT)
entry.insert(0, '0')
entry.grid(row=0, column=0, columnspan=5, sticky='nswe', pady=5)

tk.Button(rt, text='-char', font=('Arial', 14), bd=4, command=removeChar).grid(row=1, column=0,
                                                                                sticky='nswe')
tk.Button(rt, text='clear', font=('Arial', 14), bd=4, command=clearEntry).grid(row=1, column=1,
                                                                                columnspan=2,
                                                                                sticky='nswe')
createDigitButton('Pi').grid(row=1, column=3, sticky='nswe')
createDigitButton('e').grid(row=1, column=4, sticky='nswe')

createOperatorButton('div').grid(row=2, column=0, sticky='nswe')
createOperatorButton('mod').grid(row=2, column=1, columnspan=2, sticky='nswe')
createOperatorButton('√').grid(row=2, column=3, sticky='nswe')
createOperatorButton('^').grid(row=2, column=4, sticky='nswe')

createDigitButton('7').grid(row=3, column=0, sticky='nswe')
createDigitButton('8').grid(row=3, column=1, sticky='nswe')
createDigitButton('9').grid(row=3, column=2, sticky='nswe')
createOperatorButton('+').grid(row=3, column=3, sticky='nswe')
createOperatorButton('-').grid(row=3, column=4, sticky='nswe')

createDigitButton('4').grid(row=4, column=0, sticky='nswe')
createDigitButton('5').grid(row=4, column=1, sticky='nswe')
createDigitButton('6').grid(row=4, column=2, sticky='nswe')
createOperatorButton('*').grid(row=4, column=3, sticky='nswe')
createOperatorButton('/').grid(row=4, column=4, sticky='nswe')

createDigitButton('1').grid(row=5, column=0, sticky='nswe')
createDigitButton('2').grid(row=5, column=1, sticky='nswe')
createDigitButton('3').grid(row=5, column=2, sticky='nswe')
createOperatorButton('%').grid(row=5, column=3, sticky='nswe')
tk.Button(rt, text='=', font=('Arial', 14), bd=4, command=calc).grid(row=5, column=4, rowspan=2,
                                                                     sticky='nswe')

createDigitButton('0').grid(row=6, column=0, columnspan=2, sticky='nswe')
createOperatorButton('.').grid(row=6, column=2, columnspan=2, sticky='nswe')

tk.Button(rt, text='Сохранить историю вычислений', fg='green', font=('Arial', 14), bd=4,
          command=saveResult).grid(row=7, column=0,
                                 columnspan=5,
                                 sticky='nswe')

tk.Button(rt, text='Выход', fg='red', font=('Arial', 14), bd=4,
          command=exit).grid(row=8, column=0,
                             columnspan=5,
                             sticky='nswe')

archive = tk.scrolledtext.ScrolledText(rt, wrap=tk.WORD, width=40, height=10, font=('Arial', 14))
archive.grid(row=0, column=5, rowspan=9, sticky='nswe')
archive.config(state=tk.DISABLED)
for i in range(5):
    rt.grid_columnconfigure(i, minsize=90)

rt.mainloop()
