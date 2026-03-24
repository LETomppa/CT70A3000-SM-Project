from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

from helpers import setHeadingsAndColumns, addLabelAndEntry, font

class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ all variables --------------
        self.varSearchby=StringVar()
        self.varSearchtxt=StringVar()
        self.varSupInvoice=StringVar()
        self.varName=StringVar()
        self.varContact=StringVar()


        #---------- Search Frame -------------
        lblSearch=Label(self.root,text="Invoice No.",bg="white",font=(font,15))
        lblSearch.place(x=700,y=80)

        Entry(self.root,textvariable=self.varSearchtxt,font=(font,15),bg="lightyellow").place(x=850,y=80,width=160)
        Button(self.root,command=self.search,text="Search",font=(font,15),bg="#4caf50",fg="white",cursor="hand2").place(x=980,y=79,width=100,height=28)

        #-------------- title ---------------
        Label(self.root,text="Supplier Details",font=(font,20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1000,height=40)

        #-------------- content ---------------
        addLabelAndEntry(self.root, "Invoice No.", self.varSupInvoice, 50, 80, 180, 80, 180)
        addLabelAndEntry(self.root, "Name", self.varName, 50, 120, 180, 120, 180)
        addLabelAndEntry(self.root, "Contact", self.varContact, 50, 160, 180, 160, 180)

        #---------- row 4 ----------------
        Label(self.root,text="Description",font=(font,15),bg="white").place(x=50,y=200)
        self.txtDesc=Text(self.root,font=(font,15),bg="lightyellow")
        self.txtDesc.place(x=180,y=200,width=470,height=120)

        #-------------- buttons -----------------
        Button(self.root,text="Save",command=self.add,font=(font,15),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=370,width=110,height=35)
        Button(self.root,text="Update",command=self.update,font=(font,15),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=370,width=110,height=35)
        Button(self.root,text="Delete",command=self.delete,font=(font,15),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=370,width=110,height=35)
        Button(self.root,text="Clear",command=self.clear,font=(font,15),bg="#607d8b",fg="white",cursor="hand2").place(x=540,y=370,width=110,height=35)

        #------------ supplier details -------------
        supFrame=Frame(self.root,bd=3,relief=RIDGE)
        supFrame.place(x=700,y=120,width=380,height=350)

        scrolly=Scrollbar(supFrame,orient=VERTICAL)
        scrollx=Scrollbar(supFrame,orient=HORIZONTAL)\

        self.supplierTable=ttk.Treeview(supFrame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        setHeadingsAndColumns(self.supplierTable, "invoice", "Invoice", 90)
        setHeadingsAndColumns(self.supplierTable, "name", "Name", 100)
        setHeadingsAndColumns(self.supplierTable, "contact", "Contact", 100)
        setHeadingsAndColumns(self.supplierTable, "desc", "Description", 100)
        self.supplierTable["show"]="headings"

        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.getData)
        self.show()
#-----------------------------------------------------------------------------------------------------
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.varSupInvoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.varSupInvoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Invoice no. is already assigned",parent=self.root)
                else:
                    cur.execute("insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",(
                        self.varSupInvoice.get(),
                        self.varName.get(),
                        self.varContact.get(),
                        self.txtDesc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def getData(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        row=content['values']
        self.varSupInvoice.set(row[0])
        self.varName.set(row[1])
        self.varContact.set(row[2])
        self.txtDesc.delete('1.0',END)
        self.txtDesc.insert(END,row[3])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.varSupInvoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.varSupInvoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    cur.execute("update supplier set name=?,contact=?,desc=? where invoice=?",(
                        self.varName.get(),
                        self.varContact.get(),
                        self.txtDesc.get('1.0',END),
                        self.varSupInvoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.varSupInvoice.get()=="":
                messagebox.showerror("Error","Invoice No. must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.varSupInvoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op:
                        cur.execute("delete from supplier where invoice=?",(self.varSupInvoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.varSupInvoice.set("")
        self.varName.set("")
        self.varContact.set("")
        self.txtDesc.delete('1.0',END)
        self.varSearchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.varSearchtxt.get()=="":
                messagebox.showerror("Error","Invoice No. should be required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.varSearchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()
