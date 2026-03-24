from tkinter import*

font = "times new roman"

def setHeadingsAndColumns(table, id, text, width):
    table.heading(id, text=text)
    table.column(id, width=width)

def addLabelAndEntry(parent, labelText, textVar, labelX, labelY, entryX, entryY, width, state='normal'):
    Label(parent,text=labelText,font=(font,15),bg="white").place(x=labelX,y=labelY)
    Entry(parent,textvariable=textVar,font=(font,15),bg="lightyellow",state=state).place(x=entryX,y=entryY,width=width)