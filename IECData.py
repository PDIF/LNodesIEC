#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 14:58:41 2021

@author: petrov
"""

from json import loads as LOAD              #Чтение данных из JSON
from pathlib import Path as PATH            #Организация путей к файлам
from codecs import open as OPEN             #Декодирование
from tkinter import ttk as TTK              #Таблицы
import tkinter as GUI                       #Подключаем графическую библиотеку



def ExistInDATA(InputDATA, FindString):
    """
    Проверка существования записи в базе
    """

    #Список,в котором будем проверять записи (при необходимости)
    ListDATA = []

    #Список искомых величин
    FindDATA = FindString.split(' ')

    #Если в качестве InputDATA используется строка,
    #то ищем в ней все элементы FindDATA
    if type(InputDATA) == str:

        #Поиск
        if all(FindRECORD.lower() in InputDATA.lower() \
            for FindRECORD in FindDATA):

            return True                     #Если нашли, то возвращаем True
        else:
            return False                    #Если не нашли, то возвращаем False

    #Если в качестве InputDATA используется список,
    #то присваиваем ListDATA его значения
    elif type(InputDATA) == list:

        ListDATA = InputDATA                #Присваиваем значения базы

    #Если в качестве InputDATA используется словарь,
    #то берем его список ключей и присваиваем ListDATA его значения
    elif type(InputDATA) == dict:

        ListDATA = list(InputDATA.values())

    #Если список ListDATA к текущему моменту не пуст,
    #то разбиваем его на элементы и для каждого вызываем
    #в виде рекурсии функцию поиска и ищем FindString
    if len(ListDATA) > 0:

        #Элемент списка
        for RECORD in ListDATA:

            #Рекурсивно вызываем функцию
            if ExistInDATA(RECORD, FindString):

                return True

    #Если добрались до этой команды, значит, ничего не нашли
    return False


def ReturnDATA(InputDATA, FindString):
    """
    Возвращает запись, содержащую нужные значения
    """
    #Список,в котором будем проверять записи (при необходимости)
    OutDATA = {'isString': False,
               'isFound':  False,
               'Value':    []}

    #Список искомых величин
    FindDATA = FindString.split(' ')

    #Если в качестве InputDATA используется строка,
    #то ищем в ней все элементы FindDATA
    if type(InputDATA) == str:

        OutDATA['isString'] = True

        if all(FindRECORD.lower() in InputDATA.lower() \
            for FindRECORD in FindDATA):

            OutDATA['isFound'] = True
            OutDATA['Value'] = InputDATA
        else:

            OutDATA['isFound'] = False

        return OutDATA


    elif type(InputDATA) == list:

        if len(InputDATA) > 0:

            for RECORD in InputDATA:

                iFOUND = ReturnDATA(RECORD, FindString)

                if iFOUND['isFound']:
                    OutDATA['isFound'] = True
                    OutDATA['Value'].append(iFOUND['Value'])

    elif type(InputDATA) == dict:

        if len(InputDATA) > 0:

            for RECORD in InputDATA:

                iFOUND = ReturnDATA(InputDATA[RECORD], FindString)

                if iFOUND['isFound']:
                    OutDATA['isFound'] = True
                    OutDATA['Value'].append({RECORD: iFOUND['Value']})


    return OutDATA




def FindRecord(FindString):
    '''
    Формирование итогового массива значений
    '''
    #Подключаем общую базу данных
    global FullDataBase

    #Выходной массив
    TotalOutput = []

    #Массив искомых значений
    FindDATA = FindString.split(';')

    #Перебираем все записи полной базы данных
    for iRECORD in FullDataBase:

        #Все элементы FindDATA должны быть найдены
        if all(ExistInDATA(iRECORD, FindREC) for FindREC in FindDATA):

            #Итоговый массив значений
            TotalOutput.append(iRECORD)

    return TotalOutput



#============================
#Обработка событий интерфейса
#============================
'''
Обработка события
'''
def APPLY(event):
    CmdFindAll()

def SETNODE(event):
    CmdSet()

def CONFIGSIZE(event):
    '''
    Размещение элементов в окне
    '''
    if event.widget == Window:

        #Константы
        dH = 3       #На сколько по вертикали отступают друг от друга элементы
        hSTR = 25    #Базовая высота строки


        #Координаты в зависимости от размеров окна
        dVBase = event.width - 32                   #Базовая ширина элемента
        dHBase = (event.height - 8 * hSTR) // 13     #Базовая высота элемента

        #Высота элементов на окне
        hFnd = hSTR                     #Строка "Найти"
        hNod = hSTR + 4 * dHBase - dH   #Общая таблица результатов
        hRst = hSTR                     #Строка "Результат"
        hDsc = hSTR + 3 * dHBase - dH   #Общее описание узла
        hTtl = hSTR + 5 * dHBase - dH   #Таблица характеристик узла
        hCnd = hSTR                     #Строка "Разделы"
        hSpc = hSTR + 1 * dHBase - dH   #Путь к найденным разделам

        hHEIGHT = {'FIND': hFnd,
                   'NODE': hNod,
                   'RSLT': hRst,
                   'DSCR': hDsc,
                   'TOTL': hTtl,
                   'COND': hCnd,
                   'SPEC': hSpc
                  }

        #Координаты элементов на окне
        yCOORD = {}
        kHEIGHT = list(hHEIGHT.keys())            #Ключи
        vHEIGHT = list(hHEIGHT.values())          #Значения

        for iVAL in kHEIGHT:
            yCOORD[iVAL] = sum(vHEIGHT[:kHEIGHT.index(iVAL)],
                               kHEIGHT.index(iVAL)*dH)

        lblFnd.place(
                height = hFnd, width = 50,
                x = 15, y = yCOORD['FIND'] + dH,
                anchor = 'nw')
        txtFnd.place(
                height = hFnd, width = dVBase - 160,
                x = 80, y = yCOORD['FIND'] + dH,
                anchor = 'nw')
        btnFnd.place(
                height = hFnd, width = 80,
                x = dVBase - 70, y = yCOORD['FIND'] + dH,
                anchor = 'nw')

        #Результат глобального поиска
        BASEW = (dVBase / sum(TableSIZE['TOTAL']))
        for i in range(len(TableSIZE['TOTAL'])):
            tblNod.column('#' + str(i),
                          width = int(BASEW * TableSIZE['TOTAL'][i]))
        tblNod.place(
                height = hNod, width = dVBase,
                x = 10, y = yCOORD['NODE'] + dH,
                anchor = 'nw')
        scrNodBar.place(
                height = hNod, width = 21,
                x = dVBase + 10, y = yCOORD['NODE'] + dH,
                anchor = 'nw')

        #Заголовок результата
        lblRST.place(
                height = hRst, width = 70,
                x = 15, y = yCOORD['RSLT'] + dH,
                anchor = 'nw')

        #Описание узла
        txtDSC.place(
                height = hDsc, width = dVBase,
                x = 10, y = yCOORD['DSCR'] + dH,
                anchor = 'nw')
        scrDSCBar.place(
                height = hDsc, width = 21,
                x = dVBase + 10, y = yCOORD['DSCR'] + dH,
                anchor = 'nw')

        #Данные узла
        BASEW = (dVBase / sum(TableSIZE['PART']))
        for i in range(len(TableSIZE['PART'])):
            tblTTL.column('#' + str(i),
                          width = int(BASEW * TableSIZE['PART'][i]))
        tblTTL.place(
                height = hTtl, width = dVBase ,
                x = 10, y = yCOORD['TOTL'] + dH,
                anchor = 'nw')
        scrTTLBar.place(
                height = hTtl, width = 21,
                x = dVBase + 10, y = yCOORD['TOTL'] + dH,
                anchor = 'nw')

        #Условие
        lblCND.place(
                height = hCnd, width = 70,
                x = 15, y = yCOORD['COND'] + dH,
                anchor = 'nw')

        txtSPC.place(
                height = hSpc, width = dVBase,
                x = 10, y = yCOORD['SPEC'] + dH,
                anchor = 'nw')
        scrSPCBar.place(
                height = hSpc, width = 21,
                x = dVBase + 10, y = yCOORD['SPEC'] + dH,
                anchor = 'nw')


def SETCLIPBOARDVALUES(event):
    '''
    Заполняет буфер обмена значениями таблицы
    '''
    
    #Нажали на второй таблице
    if event.widget == tblTTL:
        
        if len(tblTTL.selection()) > 0:
            
            #Чистим буфер
            Window.clipboard_clear()
            
            #Перебираем выделенные строки
            for iROW in tblTTL.selection():
                #Перебираем значения в каждой строке
                AddVAL = tblTTL.item(iROW)['values']
                
                Window.clipboard_append('\t'.join(AddVAL))
                Window.clipboard_append('\n')
        
    #Нажали на главной таблице
    elif event.widget == tblNod:
        
        if len(tblNod.selection()) > 0:
            
            #Чистим буфер
            Window.clipboard_clear()
            
            #Перебираем выделенные строки
            for iROW in tblNod.selection():
                #Перебираем значения в каждой строке
                AddVAL = tblNod.item(iROW)['values']
                
                Window.clipboard_append('\t'.join(AddVAL))
                Window.clipboard_append('\n')
    
    #Нажали на текстовом поле "Найдено"
    elif event.widget == txtDSC:
        
        strSELECTION = txtDSC.selection_get()
        
        if len(strSELECTION) > 0:
            #Чистим буфер
            Window.clipboard_clear()
            
            #Копируем выделенный текст в буфер
            Window.clipboard_append(strSELECTION)
        
    
    #Нажали на окне
    elif event.widget == Window:
        
        #Чистим буфер
        Window.clipboard_clear()
        
        #Главная таблица
        for iROW in tblNod.get_children():
            #Перебираем значения в каждой строке
            AddVAL = tblNod.item(iROW)['values']
            
            Window.clipboard_append('\t'.join(AddVAL))
            Window.clipboard_append('\n')
            
        #Главная таблица
        for iROW in tblTTL.get_children():
            #Перебираем значения в каждой строке
            AddVAL = tblTTL.item(iROW)['values']
            
            Window.clipboard_append('\t'.join(AddVAL))
            Window.clipboard_append('\n')



def SETTABLE(event):
    '''
    Изменение размеров таблицы
    '''            
    
    global TableSIZE
    
    for i in range(len(TableSIZE['TOTAL'])):
        TableSIZE['TOTAL'][i] = tblNod.column('#' + str(i))['width']
    for i in range(len(TableSIZE['PART'])):
        TableSIZE['PART'][i] = tblTTL.column('#' + str(i))['width']
    

def FINDSELECTEDRECORD(FindString):
    '''
    Поиск записей, соответствующих каждому критерию поиска
    в базе найденных значений
    '''
    tblTTL.selection_clear                  #Чистим выделение
    FindDATA = FindString.split(';')        #Искомое значение
    
    #Перебираем строки в таблице
    for iROW in tblTTL.get_children():
        #Перебираем значения в каждой строке
        for iVAL in tblTTL.item(iROW)['values']:
            #Перебираем значения в запросе, разделенные ';'
            for FindWORDS in FindDATA:
                #Ищем все слова в запросе, разделенные пробелом
                if all(iWORD.lower() in iVAL.lower() \
                                     for iWORD in FindWORDS.split()):
                    #Выделяем строки
                    tblTTL.selection_add(iROW)
    
    
#============================
#Выполнение команд
#============================
def CmdFindAll():
    '''
    Поиск всех значений по базе данных
    '''

    global FoundDATA

    #Поиск значения
    M = FindRecord(txtFnd.get())

    #Передаем найденные значения
    FoundDATA = M

    #Очищаем таблицу результатов
    tblNod.delete(*tblNod.get_children())
    #Заполнение таблицы результатов
    for i in range(0,len(M)):
        #Выходные данные
        OutVals = [M[i]['CLASS'], M[i]['SHORT'], M[i]['EXPLAN']]
        #Заполнение
        tblNod.insert(parent = '',
                       index = 'end',
                       iid = i,
                       text = i+1,
                       values = OutVals)


'''
Выбор узла
'''
def CmdSet():

    global FoundDATA

    #Выходим, если таблица пуста
    if len(tblNod.get_children()) == 0:
        return

    #Индекс считанного значения
    iVAL = int(tblNod.focus())

    #Очистка
    tblTTL.delete(*tblTTL.get_children())

    #Заполнение таблицы результатов
    OutVals = []

    for iREC in FoundDATA[iVAL]['DESCR']:
        #Строка
        OutVals.append([
                   iREC['NAME'],
                   iREC['CDC'],
                   iREC['EXPLANATION'],
                   iREC['T'],
                   iREC['IEC'],
                   iREC['CORP']])

    for iREC in FoundDATA[iVAL]['LNNAME']:
        #Строка
        OutVals.append([
                   iREC['NAME'],
                   iREC['CDC'],
                   iREC['EXPLANATION'],
                   iREC['T'],
                   iREC['IEC'],
                   iREC['CORP']])

    for iREC in FoundDATA[iVAL]['STATUS']:
        #Строка
        OutVals.append([
                   iREC['NAME'],
                   iREC['CDC'],
                   iREC['EXPLANATION'],
                   iREC['T'],
                   iREC['IEC'],
                   iREC['CORP']])

    for iREC in FoundDATA[iVAL]['DIRECT']:
        #Строка
        OutVals.append([
                   iREC['NAME'],
                   iREC['CDC'],
                   iREC['EXPLANATION'],
                   iREC['T'],
                   iREC['IEC'],
                   iREC['CORP']])

    for iREC in FoundDATA[iVAL]['PARAMS']:
        #Строка
        OutVals.append([
                   iREC['NAME'],
                   iREC['CDC'],
                   iREC['EXPLANATION'],
                   iREC['T'],
                   iREC['IEC'],
                   iREC['CORP']])

    i = 1
    for iREC in OutVals:
        #Заполнение
        tblTTL.insert(parent = '',
                         index = 'end',
                         iid = i,
                         text = i,
                         values = iREC)
        i +=1

    #Заполнение полей
    strOut = 'Описание:\n'
    strOut += FoundDATA[iVAL]['USAGE'] + '\n'

    strOut += '\n'
    strOut += 'Функции:\n'
    for i in range(0, len(FoundDATA[iVAL]['FUNCT'])):
        strOut = strOut + str(i+1) + '. ' + FoundDATA[iVAL]['FUNCT'][i]
        strOut = strOut + '.' if strOut[-1] != '.' else strOut
        strOut += '\n'

    strOut += '\n'
    strOut += 'Условия:\n'
    for iREC in FoundDATA[iVAL]['COND']:
        for iKEY in list(iREC.keys()):
            strOut = strOut + iKEY + ': ' + iREC[iKEY]
            strOut = strOut + '.' if strOut[-1] != '.' else strOut
            strOut += '\n'

    #Убираем последний символ переноса строки
    strOut = strOut[:-1] if len(strOut) > 2 else strOut

    txtDSC.delete('1.0','end')
    txtDSC.insert('1.0', strOut)

    #ВЫделение найденных строк
    FINDSELECTEDRECORD(txtFnd.get())
    

#=========
#Программа
#=========

#Читаем и декодируем файл с базой данных по логическим узлам
fImportDataIEC = OPEN(PATH.cwd() / 'DB' / 'iecdata', 'r', 'cp1251').read()
fImportDataADD = OPEN(PATH.cwd() / 'DB' / 'adddata', 'r', 'cp1251').read()

#Найденные значения
FoundDATA = []

#Формируем общую базу данных
FullDataBase = LOAD(fImportDataIEC) + LOAD(fImportDataADD)

#Размер таблицы
WindowSize = {'W': 900,
              'H': 850}

TableSIZE = {'TOTAL': [1, 2, 3, 10],
             'PART':  [2, 4, 2, 18, 1, 2, 3]}
        
#==========
#Оформление
#==========
#Окно
Window = GUI.Tk()                                               #Объект
#Window.resizable(width = False, height = False)

#Поле для поиска
lblFnd = GUI.Label(Window, text = 'Запрос:')                   #Метка
txtFnd = GUI.Entry(Window)                                     #Текстовое поле
btnFnd = GUI.Button(Window, text = 'Найти', command = CmdFindAll) #Кнопка

#Поле для результатов
strHeaders = ['№', 'Класс', 'Обозначение', 'Описание']          #Наименование
tblNod = TTK.Treeview(Window, columns = strHeaders[1:])        #Заголовки
scrNodBar = TTK.Scrollbar(Window, command = tblNod.yview)     #Прокрутка
tblNod.configure(yscrollcommand = scrNodBar.set)              #Прокрутка
for i in range(0, len(strHeaders)):                             #Применение
    tblNod.heading('#' + str(i), text = strHeaders[i])

#Поля для отдельного узла
#Метки
lblRST = GUI.Label(Window, text = 'Найдено:', justify = 'left')
lblCND = GUI.Label(Window, text = 'Разделы:', justify = 'left')

#Текст
txtDSC = GUI.Text(Window, wrap = 'word')
txtSPC = GUI.Text(Window, wrap = 'word')

#Прокрутка
scrDSCBar = TTK.Scrollbar(Window, command = txtDSC.yview)
scrSPCBar = TTK.Scrollbar(Window, command = txtSPC.yview)
#Взаимосвязь текста и прокрутки
txtDSC.configure(yscrollcommand = scrDSCBar.set)
txtSPC.configure(yscrollcommand = scrSPCBar.set)

#Таблица
strHeaders = ['№', 'Имя', 'Тип', 'Описание', 'T', 'МЭК', 'Профиль'] #Наименов
tblTTL = TTK.Treeview(Window, columns = strHeaders[1:])          #Заголовки
scrTTLBar = TTK.Scrollbar(Window, command = tblTTL.yview)     #Прокрутка
tblTTL.configure(yscrollcommand = scrTTLBar.set)              #Прокрутка
for i in range(0, len(strHeaders)):                                 #Применение
    tblTTL.heading('#' + str(i), text = strHeaders[i])


#=================
#Обработка событий
#=================
txtFnd.bind('<Return>',APPLY)                   #Нажатие на Enter в поле поиска
tblNod.bind('<Double-1>',SETNODE)               #Двойной клик на таблице
tblNod.bind('<Button-1>',SETTABLE)              #Одинарный клик на таблице
tblTTL.bind('<Button-1>',SETTABLE)              #Одинарный клик на таблице

Window.bind('<Configure>', CONFIGSIZE)          #Изменение размеров окна
Window.bind('<Control-c>', SETCLIPBOARDVALUES)  #Копирование Ctrl+C где угодно



Window.geometry(str(WindowSize['W']) + 'x' + str(WindowSize['H']))
Window.title("Корпоративный профиль")                           #Заголовок
Window.mainloop()
