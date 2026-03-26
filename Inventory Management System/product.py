from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
from helpers import setHeadingsAndColumns, addLabelAndEntry, addRecord, showRecord, getRecordData, updateRecord, deleteRecord, searchRecord, font

class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        #---------------------------------------
        #----------- variables -------------
        self.varCat=StringVar()
        self.catList=[]
        self.supList=[]
        self.fetchCatSup()
        self.varPid=StringVar()
        self.varSup=StringVar()
        self.varName=StringVar()
        self.varPrice=StringVar()
        self.varQty=StringVar()
        self.varStatus=StringVar()
        self.varSearchby=StringVar()
        self.varSearchtxt=StringVar()

        productFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        productFrame.place(x=10,y=10,width=450,height=480)

        #------------ title --------------
        Label(productFrame,text="Manage Product Details",font=(font,18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        Label(productFrame,text="Category",font=(font,18),bg="white").place(x=30,y=60)
        Label(productFrame,text="Supplier",font=(font,18),bg="white").place(x=30,y=110)
        Label(productFrame,text="Status",font=(font,18),bg="white").place(x=30,y=310)

        cmbCat=ttk.Combobox(productFrame,textvariable=self.varCat,values=self.catList,state='readonly',justify=CENTER,font=(font,15))
        cmbCat.place(x=150,y=60,width=200)
        cmbCat.current(0)

        cmbSup=ttk.Combobox(productFrame,textvariable=self.varSup,values=self.supList,state='readonly',justify=CENTER,font=(font,15))
        cmbSup.place(x=150,y=110,width=200)
        cmbSup.current(0)

        addLabelAndEntry(productFrame, "Name", self.varName, 30, 160, 150, 160, 200)
        addLabelAndEntry(productFrame, "Price", self.varPrice, 30, 210, 150, 210, 200)
        addLabelAndEntry(productFrame, "Quantity", self.varQty, 30, 260, 150, 260, 200)

        cmbStatus=ttk.Combobox(productFrame,textvariable=self.varStatus,values=("Active","Inactive"),state='readonly',justify=CENTER,font=(font,15))
        cmbStatus.place(x=150,y=310,width=200)
        cmbStatus.current(0)

        #-------------- buttons -----------------
        Button(productFrame,text="Save",command=self.add,font=(font,15),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        Button(productFrame,text="Update",command=self.update,font=(font,15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        Button(productFrame,text="Delete",command=self.delete,font=(font,15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        Button(productFrame,text="Clear",command=self.clear,font=(font,15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)

        #---------- Search Frame -------------
        searchFrame=LabelFrame(self.root,text="Search Product",font=(font,12,"bold"),bd=2,relief=RIDGE,bg="white")
        searchFrame.place(x=480,y=10,width=600,height=80)

        #------------ options ----------------
        cmbSearch=ttk.Combobox(searchFrame,textvariable=self.varSearchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=(font,15))
        cmbSearch.place(x=10,y=10,width=180)
        cmbSearch.current(0)

        Entry(searchFrame,textvariable=self.varSearchtxt,font=(font,15),bg="lightyellow").place(x=200,y=10)
        Button(searchFrame,text="Search",command=self.search,font=(font,15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #------------ product details -------------
        productListFrame=Frame(self.root,bd=3,relief=RIDGE)
        productListFrame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(productListFrame,orient=VERTICAL)
        scrollx=Scrollbar(productListFrame,orient=HORIZONTAL)\

        self.productTable=ttk.Treeview(productListFrame,columns=("pid","Category","Supplier","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
        setHeadingsAndColumns(self.productTable, "pid", "P ID", 90)
        setHeadingsAndColumns(self.productTable, "Category", "Category", 100)
        setHeadingsAndColumns(self.productTable, "Supplier", "Supplier", 100)
        setHeadingsAndColumns(self.productTable, "name", "Name", 100)
        setHeadingsAndColumns(self.productTable, "price", "Price", 100)
        setHeadingsAndColumns(self.productTable, "qty", "Quantity", 100)
        setHeadingsAndColumns(self.productTable, "status", "Status", 100)

        self.productTable["show"]="headings"

        self.productTable.pack(fill=BOTH,expand=1)
        self.productTable.bind("<ButtonRelease-1>",self.getData)
        self.show()
        self.fetchCatSup()
#-----------------------------------------------------------------------------------------------------
    #Fetch the list of categories and suppliers from the database to populate the dropdowns
    def fetchCatSup(self):
        self.catList.append("Empty")
        self.supList.append("Empty")
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.catList[:]
                self.catList.append("Select")
                for i in cat:
                    self.catList.append(i[0])
            cur.execute("select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.supList[:]
                self.supList.append("Select")
                for i in sup:
                    self.supList.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


    #Add a new product to the database
    def add(self):
        if self.varCat.get()=="Select" or self.varCat.get()=="Empty" or self.varSup=="Select" or self.varSup=="Empty":
            messagebox.showerror("Error","All fields are required",parent=self.root)
        else:
            labels=["Category","Supplier","name","price","qty","status"]
            data=[
                self.varCat.get(),
                self.varSup.get(),
                self.varName.get(),
                self.varPrice.get(),
                self.varQty.get(),
                self.varStatus.get(),
            ]
            if addRecord("product","name",self.varName,labels,data,self.root):
                self.clear()
                self.show()

    #Display all products in the product table
    def show(self):
        showRecord("product",self.productTable)

    #Get the selected product data and populate the fields for editing or deletion
    def getData(self,ev):
        getRecordData(self.productTable,[self.varPid,self.varCat,self.varSup,self.varName,self.varPrice,self.varQty,self.varStatus])

    #Update the selected product's information in the database
    def update(self):
        if self.varPid.get()=="":
            messagebox.showerror("Error","Please select product from list",parent=self.root)
        else:
            labels=["Category","Supplier","name","price","qty","status"]
            data=[
                self.varCat.get(),
                self.varSup.get(),
                self.varName.get(),
                self.varPrice.get(),
                self.varQty.get(),
                self.varStatus.get(),
            ]
            if updateRecord("product","pid",self.varPid,labels,data,self.root):
                self.show()

    #Delete the selected product from the database
    def delete(self):
        if self.varPid.get()=="":
            messagebox.showerror("Error","Select Product from the list",parent=self.root)
        else:
            if deleteRecord("product","pid",self.varPid,self.root):
                self.clear()

    #Clear all input fields
    def clear(self):
        self.varCat.set("Select")
        self.varSup.set("Select")
        self.varName.set("")
        self.varPrice.set("")
        self.varQty.set("")
        self.varStatus.set("Active")
        self.varPid.set("")
        self.varSearchby.set("Select")
        self.varSearchtxt.set("")
        self.show()


    #Search for products based on the selected search criteria and input text
    def search(self):
        if self.varSearchby.get()=="Select":
            messagebox.showerror("Error","Select Search By option",parent=self.root)
        elif self.varSearchtxt.get()=="":
            messagebox.showerror("Error","Search input should be required",parent=self.root)
        else:
            searchRecord("product",self.varSearchby.get(),self.varSearchtxt,self.productTable,self.root)

if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()
