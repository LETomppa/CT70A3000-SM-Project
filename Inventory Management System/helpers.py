from tkinter import*

#Global font variable for consistent styling across the application
font = "times new roman"

#Helper functions for the Inventory Management System

#Set the headings and column widths for a Treeview table
def setHeadingsAndColumns(table, id, text, width):
    table.heading(id, text=text)
    table.column(id, width=width)

#Add a label and entry field to the specified parent widget with the given parameters
def addLabelAndEntry(parent, labelText, textVar, labelX, labelY, entryX, entryY, width, state='normal'):
    Label(parent,text=labelText,font=(font,15),bg="white").place(x=labelX,y=labelY)
    Entry(parent,textvariable=textVar,font=(font,15),bg="lightyellow",state=state).place(x=entryX,y=entryY,width=width)