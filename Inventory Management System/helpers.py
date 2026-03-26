from tkinter import*
from tkinter import messagebox
import sqlite3

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

#Add a new record to the database
def addRecord(name, type, id, labels, data, root):
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    try:
        cur.execute(f"Select * from {name} where {type}=?",(id.get(),))
        row=cur.fetchone()
        if row!=None:
            messagebox.showerror("Error",f"{name} already present",parent=root)
            return False
        else:
            cur.execute(f"insert into {name}({', '.join(labels)}) values({', '.join(['?' for _ in labels])})", tuple(data))
            con.commit()
            messagebox.showinfo("Success",f"{name} Added Successfully",parent=root)
            return True
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to : {str(ex)}")
        return False

 #Display all records in the given table
def showRecord(name, table):
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    try:
        cur.execute(f"select * from {name}")
        rows=cur.fetchall()
        table.delete(*table.get_children())
        for row in rows:
            table.insert('',END,values=row)
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to : {str(ex)}")

 #Get the selected record data and populate the fields for editing or deletion
def getRecordData(table, fields):
    f=table.focus()
    content=(table.item(f))
    row=content['values']
    for i,field in enumerate(fields):
        if hasattr(field,'set'):
            field.set(row[i])
        else:
            field.delete('1.0',END)
            field.insert(END,row[i])

#Update the selected records's information in the database
def updateRecord(name, type, id, labels, data, root):
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    try:
        cur.execute(f"Select * from {name} where {type}=?",(id.get(),))
        row=cur.fetchone()
        if row==None:
            messagebox.showerror("Error",f"Invalid {name}",parent=root)
            return False
        else:
            cur.execute(f"update {name} set {', '.join([l+'=?' for l in labels])} where {type}=?", tuple(data)+(id.get(),))
            con.commit()
            messagebox.showinfo("Success",f"{name} Updated Successfully",parent=root)
            return True
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to : {str(ex)}")
        return False

#Delete the selected record from the database
def deleteRecord(name, type, id, root):
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    try:
        cur.execute(f"Select * from {name} where {type}=?",(id.get(),))
        row=cur.fetchone()
        if row==None:
            messagebox.showerror("Error",f"Invalid {name}",parent=root)
            return False
        else:
            op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=root)
            if op:
                cur.execute(f"delete from {name} where {type}=?",(id.get(),))
                con.commit()
                messagebox.showinfo("Delete",f"{name} Deleted Successfully",parent=root)
                return True
            return False
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to : {str(ex)}")
        return False

#Search for records based on the selected search criteria and input text
def searchRecord(name, type, id, table, root):
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    try:
        cur.execute(f"select * from {name} where {type} LIKE '%{id.get()}%'")
        rows=cur.fetchall()
        if len(rows)!=0:
            table.delete(*table.get_children())
            for row in rows:
                table.insert('',END,values=row)
        else:
            messagebox.showerror("Error","No record found!!!",parent=root)
    except Exception as ex:
        messagebox.showerror("Error",f"Error due to : {str(ex)}")