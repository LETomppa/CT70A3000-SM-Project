from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

from helpers import setHeadingsAndColumns, addLabelAndEntry, addRecord, showRecord, getRecordData, updateRecord, deleteRecord, searchRecord, font

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
    #Add a new supplier to the database
    def add(self):
        if self.varSupInvoice.get()=="":
            messagebox.showerror("Error","Invoice must be required",parent=self.root)
        else:
            labels=["invoice","name","contact","desc"]
            data=[
                self.varSupInvoice.get(),
                self.varName.get(),
                self.varContact.get(),
                self.txtDesc.get('1.0',END),
            ]
            if addRecord("supplier","invoice",self.varSupInvoice,labels,data,self.root):
                self.clear()
                self.show()

    #Display all suppliers in the supplier table
    def show(self):
        showRecord("supplier",self.supplierTable)

    #Get the selected supplier data and populate the fields for editing or deletion
    def getData(self,ev):
        getRecordData(self.supplierTable,[self.varSupInvoice,self.varName,self.varContact,self.txtDesc])

    #Update the selected supplier's information in the database
    def update(self):
        if self.varSupInvoice.get()=="":
            messagebox.showerror("Error","Invoice must be required",parent=self.root)
        else:
            labels=["name","contact","desc"]
            data=[
                self.varName.get(),
                self.varContact.get(),
                self.txtDesc.get('1.0',END),
            ]
            if updateRecord("supplier","invoice",self.varSupInvoice,labels,data,self.root):
                self.show()

    #Delete the selected supplier from the database
    def delete(self):
        if self.varSupInvoice.get()=="":
            messagebox.showerror("Error","Invoice No. must be required",parent=self.root)
        else:
            if deleteRecord("supplier","invoice",self.varSupInvoice,self.root):
                self.clear()

    #Clear all input fields
    def clear(self):
        self.varSupInvoice.set("")
        self.varName.set("")
        self.varContact.set("")
        self.txtDesc.delete('1.0',END)
        self.varSearchtxt.set("")
        self.show()

    #Search for suppliers based on the selected search criteria and input text
    def search(self):
        if self.varSearchtxt.get()=="":
            messagebox.showerror("Error","Invoice No. should be required",parent=self.root)
        else:
            searchRecord("supplier","invoice",self.varSearchtxt,self.supplierTable,self.root)


if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()
