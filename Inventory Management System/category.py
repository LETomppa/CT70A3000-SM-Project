from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
from helpers import setHeadingsAndColumns, font
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ variables -------------
        self.varCatId=StringVar()
        self.varName=StringVar()
        #--------------- title ---------------------
        Label(self.root,text="Manage Product Category",font=(font,30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        Label(self.root,text="Enter Category Name",font=(font,30),bg="white").place(x=50,y=100)
        Entry(self.root,textvariable=self.varName,bg="lightyellow",font=(font,18)).place(x=50,y=170,width=300)

        Button(self.root,text="ADD",command=self.add,font=(font,15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        Button(self.root,text="Delete",command=self.delete,font=(font,15),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)

        #------------ category details -------------
        catFrame=Frame(self.root,bd=3,relief=RIDGE)
        catFrame.place(x=700,y=100,width=380,height=100)

        scrolly=Scrollbar(catFrame,orient=VERTICAL)
        scrollx=Scrollbar(catFrame,orient=HORIZONTAL)\

        self.categoryTable=ttk.Treeview(catFrame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)

        setHeadingsAndColumns(self.categoryTable, "cid", "C ID", 90)
        setHeadingsAndColumns(self.categoryTable, "name", "Name", 100)
        self.categoryTable["show"]="headings"

        self.categoryTable.pack(fill=BOTH,expand=1)
        self.categoryTable.bind("<ButtonRelease-1>",self.getData)
        self.show()

        #----------------- images ---------------------
        self.addImage(os.path.join(IMAGE_DIR, "cat.jpg"), 50, 220)
        self.addImage(os.path.join(IMAGE_DIR, "category.jpg"), 580, 220)
#----------------------------------------------------------------------------------

    def addImage(self, path, x, y):
        img = Image.open(path)
        img = img.resize((500, 250))
        img = ImageTk.PhotoImage(img)
        lbl = Label(self.root, image=img, bd=2, relief=RAISED)
        lbl.image = img
        lbl.place(x=x, y=y)

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.varName.get()=="":
                messagebox.showerror("Error","Category Name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.varName.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already present",parent=self.root)
                else:
                    cur.execute("insert into category(name) values(?)",(
                        self.varName.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


    def clear(self):
        self.varName.set("")
        self.show()

    def getData(self):
        f=self.categoryTable.focus()
        content=(self.categoryTable.item(f))
        row=content['values']
        self.varCatId.set(row[0])
        self.varName.set(row[1])

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.varCatId.get()=="":
                messagebox.showerror("Error","Category name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.varCatId.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Category Name",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.varCatId.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.clear()
                        self.varCatId.set("")
                        self.varName.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")



if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()
