import psycopg2
import tkinter as tk

el1 = ''
el2 = ''
class BestMessage(tk.Message):# класс для окна вывода сообщеий 
    
    def __init__(self, *args, **kwargs):
        self.__text =  '\n'*20
        kwargs['text'] = self.__text
        super().__init__(*args, **kwargs)

    def add_line(self, line):
        line += '\n'
        lines_count = 0
        for symbol in line:
            if symbol == '\n':
                lines_count +=1
        for i in range(lines_count):
            index = self.__text.index('\n')
            self.__text = self.__text[index+1:]
        self['text'] = self.__text = self.__text + line
all_of = False # переменная которая запускает создание соединений
number_of_elements = 1 #переменная которая выбирает какой элемент вводится

def exit_(event): #функция которая закрывае окно вывода\ввода
    window.quit()

def give_element(event):# функция в которой ввод\вывод данных
    global el1, el2, number_of_elements, all_of
    if number_of_elements == 1:# ввод первого элемента
        el1 = text_input.get()
        text_input.delete(0, len(el1))
        messange_box.add_line(f'el1: {el1}')
    if number_of_elements == 2:# ввод второго элемента
        el2 = text_input.get()
        text_input.delete(0, len(el2))
        messange_box.add_line(f'el2: {el2}')
        all_of = True
    number_of_elements += 1
    if all_of == True:#создание соединений
        conn = psycopg2.connect(dbname = 'elements' , user = 'postgres', password= '1234', host= 'localhost')# вход в базу данныхх
        cursor = conn.cursor()#создание курсора 
        cursor.execute('SELECT wal, metal_or_notmetal FROM elements.elements_ WHere name_of_element = %(el1)s ', {'el1': el1}) # обращение в базу данных
        el1_wal = cursor.fetchall()#
        cursor.close()# закрытие курсора
        cursor = conn.cursor()#создание соединений
        cursor.execute('SELECT wal, metal_or_notmetal FROM elements.elements_ WHere name_of_element = %(el2)s ', {'el2': el2})# обращение в базу данных
        el2_wal = cursor.fetchall() 
        cursor.close()# закрытие курсора



        while True:#цикл создания соединений
            try:
                el1_wal[0][1] == None # ошибка несуществования элемента
            except IndexError:# что делать при ошибке несуществования элемента
                messange_box.add_line ('Введён несуществующий элемент или невозможная комбинация элементов')
                all_of = False
                number_of_elements = 1
            if el1_wal[0][1] == 0 and el2_wal[0][1] == 1 :# создание соединения из неметала и металла 
                for i in el1_wal[0][0]:
                    for i2 in el2_wal[0][0]:
                        if i == i2 :# при  равных валлентностях
                            messange_box.add_line(el2 + el1)
                        elif i % i2 == 0:# при валлентности неметалла кратной валлентонсти металла
                            i3 = i/i2
                            i3 = int(i3)
                            messange_box.add_line( el2 + str(i3) + el1)
                        elif i2 % i == 0:# при валлентности металла кратной валлентонсти неметалла
                            i3 = i2/i
                            i3 = int(i3)
                            messange_box.add_line(el2 + el1 + str(i3))
                        else:# при не кратных валлентонстях    
                            messange_box.add_line(el2 + str(i) + el1 + str(i2))
                break
            elif el1_wal[0][1] == 1 and el2_wal[0][1] == 0:# создание соединения из неметала и металла
                for i in el1_wal[0][0]:
                    for i2 in el2_wal[0][0]:
                        if i == i2 :# при  равных валлентностях
                            messange_box.add_line (el1 + el2)
                        elif i % i2 == 0:# при валлентности металла кратной валлентонсти неметалла
                            i3 = i/i2
                            i3 = int(i3)
                            messange_box.add_line(el1 + el2 + str(i3))
                        elif i2 % i == 0:# при валлентности неметалла кратной валлентонсти металла
                            i3 = i2/i
                            i3 = int(i3)
                            messange_box.add_line(el1 + str(i3) + el2)
                        else:# при не кратных валлентонстях
                            messange_box.add_line(el1 + str(i2) + el2 + str(i))
                break   
            elif el1_wal[0][1] == 0 and el2_wal[0][1] == 0:# создание соединения из неметала1 и неметалла2
                for i in el1_wal[0][0]:
                    for i2 in el1_wal[0][0]:
                        if i == i2 :# при  равных валлентностях
                            messange_box.add_line(el1 + el2)
                        elif i % i2 == 0:# при валлентности неметалла1 кратной валлентонсти неметалла2
                            i3 = i/i2
                            i3 = int(i3)
                            messange_box.add_line(el1 + el2 + str(i3))
                        elif i2 % i == 0:# при валлентности неметалла2 кратной валлентонсти неметалла1
                            i3 = i2/i
                            i3 = int(i3)
                            messange_box.add_line(el1 + str(i3) + el2)
                        else:    # при не кратных валлентонстях
                            messange_box.add_line (el1 + str(i2) + el2 + str(i))
                break
            elif el1_wal[0][1] == 1 and el2_wal[0][1] == 1:#если два металла
                messange_box.add_line ('Введён несуществующий элемент или невозможная комбинация элементов')
        all_of = False
        number_of_elements = 1


window = tk.Tk()#окно ввода\вывода
text_input = tk.Entry(width= 150)# строка ввода
button = tk.Button(text='Нажмите что-бы ввести элемент')# кнопка для ввода
messange_box = BestMessage(text='Hello')# окно вывода
window.bind('<Return>', give_element)# теперь по нажатию Enter вводиться сообщение
window.bind('<Escape>', exit_)# теперь по нажатию Escape выход 
button.bind('<Button-1>', give_element)# теперь по нажатию пкм вводиться сообщение
messange_box.pack()
text_input.pack()
button.pack()

window.mainloop()
