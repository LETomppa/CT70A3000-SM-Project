from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile

class billClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False,False)
        self.root.config(bg="white")
        self.cartList=[]
        self.chkPrint=0

        #------------- title --------------
        self.iconTitle=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.iconTitle,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #------------ logout button -----------
        btnLogout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        #------------ clock -----------------
        self.lblClock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lblClock.place(x=0,y=70,relwidth=1,height=30)

        #-------------- product frame -----------------
        productFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        productFrame1.place(x=6,y=110,width=410,height=550)

        pTitle=Label(productFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        self.varSearch=StringVar()

        productFrame2=Frame(productFrame1,bd=2,relief=RIDGE,bg="white")
        productFrame2.place(x=2,y=42,width=398,height=90)

        lblSearch=Label(productFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

        lblSearch=Label(productFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        txtSearch=Entry(productFrame2,textvariable=self.varSearch,font=("times new roman",15),bg="lightyellow").place(x=128,y=47,width=150,height=22)
        btnSearch=Button(productFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btnShowAll=Button(productFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)

        productFrame3=Frame(productFrame1,bd=3,relief=RIDGE)
        productFrame3.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(productFrame3,orient=VERTICAL)
        scrollx=Scrollbar(productFrame3,orient=HORIZONTAL)\

        self.productTable=ttk.Treeview(productFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
        self.productTable.heading("pid",text="P ID")
        self.productTable.heading("name",text="Name")
        self.productTable.heading("price",text="Price")
        self.productTable.heading("qty",text="Quantity")
        self.productTable.heading("status",text="Status")
        self.productTable["show"]="headings"
        self.productTable.column("pid",width=40)
        self.productTable.column("name",width=100)
        self.productTable.column("price",width=100)
        self.productTable.column("qty",width=40)
        self.productTable.column("status",width=90)
        self.productTable.pack(fill=BOTH,expand=1)
        self.productTable.bind("<ButtonRelease-1>",self.getData)
        self.show()

        lblNote=Label(productFrame1,text="Note: 'Enter 0 Quantity to remove product from the Cart'",font=("goudy old style",12),anchor="w",bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #-------------- customer frame ---------------
        self.varCname=StringVar()
        self.varContact=StringVar()

        customerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        customerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(customerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)

        lblName=Label(customerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txtName=Entry(customerFrame,textvariable=self.varCname,font=("times new roman",13),bg="lightyellow").place(x=80,y=35,width=180)

        lblContact=Label(customerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=270,y=35)
        txtContact=Entry(customerFrame,textvariable=self.varContact,font=("times new roman",15),bg="lightyellow").place(x=380,y=35,width=140)

        calCartFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        calCartFrame.place(x=420,y=190,width=530,height=360)

        #--------------- calculator frame ---------------------
        self.varCalInput=StringVar()

        calFrame=Frame(calCartFrame,bd=9,relief=RIDGE,bg="white")
        calFrame.place(x=5,y=10,width=268,height=340)

        self.txtCalInput=Entry(calFrame,textvariable=self.varCalInput,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        self.txtCalInput.grid(row=0,columnspan=4)

        btn7=Button(calFrame,text=7,font=('arial',15,'bold'),command=lambda:self.getInput(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
        btn8=Button(calFrame,text=8,font=('arial',15,'bold'),command=lambda:self.getInput(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
        btn9=Button(calFrame,text=9,font=('arial',15,'bold'),command=lambda:self.getInput(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
        btnSum=Button(calFrame,text="+",font=('arial',15,'bold'),command=lambda:self.getInput('+'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

        btn4=Button(calFrame,text=4,font=('arial',15,'bold'),command=lambda:self.getInput(4),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)
        btn5=Button(calFrame,text=5,font=('arial',15,'bold'),command=lambda:self.getInput(5),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)
        btn6=Button(calFrame,text=6,font=('arial',15,'bold'),command=lambda:self.getInput(6),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)
        btnSub=Button(calFrame,text="-",font=('arial',15,'bold'),command=lambda:self.getInput('-'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)

        btn1=Button(calFrame,text=1,font=('arial',15,'bold'),command=lambda:self.getInput(1),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=0)
        btn2=Button(calFrame,text=2,font=('arial',15,'bold'),command=lambda:self.getInput(2),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=1)
        btn3=Button(calFrame,text=3,font=('arial',15,'bold'),command=lambda:self.getInput(3),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=2)
        btnMul=Button(calFrame,text="*",font=('arial',15,'bold'),command=lambda:self.getInput('*'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=3)

        btn0=Button(calFrame,text=0,font=('arial',15,'bold'),command=lambda:self.getInput(0),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=0)
        btnC=Button(calFrame,text="C",font=('arial',15,'bold'),command=self.clearCal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=1)
        btnEq=Button(calFrame,text="=",font=('arial',15,'bold'),command=self.performCal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=2)
        btnDiv=Button(calFrame,text="/",font=('arial',15,'bold'),command=lambda:self.getInput('/'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=3)

        #------------------ cart frame --------------------
        cartFrame=Frame(calCartFrame,bd=3,relief=RIDGE)
        cartFrame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(cartFrame,text="Cart \t Total Products: [0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(cartFrame,orient=VERTICAL)
        scrollx=Scrollbar(cartFrame,orient=HORIZONTAL)\

        self.cartTable=ttk.Treeview(cartFrame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)
        self.cartTable.heading("pid",text="P ID")
        self.cartTable.heading("name",text="Name")
        self.cartTable.heading("price",text="Price")
        self.cartTable.heading("qty",text="Quantity")
        self.cartTable["show"]="headings"
        self.cartTable.column("pid",width=40)
        self.cartTable.column("name",width=100)
        self.cartTable.column("price",width=90)
        self.cartTable.column("qty",width=30)
        self.cartTable.pack(fill=BOTH,expand=1)
        self.cartTable.bind("<ButtonRelease-1>",self.getDataCart)

        #-------------- add cart widgets frame ---------------
        self.varPid=StringVar()
        self.varPname=StringVar()
        self.varPrice=StringVar()
        self.varQty=StringVar()
        self.varStock=StringVar()

        addCartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        addCartWidgetsFrame.place(x=420,y=550,width=530,height=110)

        lblPName=Label(addCartWidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txtPName=Entry(addCartWidgetsFrame,textvariable=self.varPname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lblPPrice=Label(addCartWidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=230,y=5)
        txtPPrice=Entry(addCartWidgetsFrame,textvariable=self.varPrice,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

        lblPQty=Label(addCartWidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        txtPQty=Entry(addCartWidgetsFrame,textvariable=self.varQty,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)

        self.lblInStock=Label(addCartWidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lblInStock.place(x=5,y=70)

        btnClearCart=Button(addCartWidgetsFrame,command=self.clearCart,text="Clear",font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btnAddCart=Button(addCartWidgetsFrame,command=self.addUpdateCart,text="Add | Update",font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)

        #------------------- billing area -------------------
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=110,width=400,height=410)

        bTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txtBillArea=Text(billFrame,yscrollcommand=scrolly.set)
        self.txtBillArea.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txtBillArea.yview)

        #------------------- billing buttons -----------------------
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=520,width=400,height=140)

        self.lblAmnt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lblAmnt.place(x=2,y=5,width=120,height=70)

        self.lblDiscount=Label(billMenuFrame,text="Discount\n[5%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lblDiscount.place(x=124,y=5,width=120,height=70)

        self.lblNetPay=Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lblNetPay.place(x=246,y=5,width=160,height=70)

        btnPrint=Button(billMenuFrame,text="Print",command=self.printBill,cursor="hand2",font=("goudy old style",15,"bold"),bg="lightgreen",fg="white")
        btnPrint.place(x=2,y=80,width=120,height=50)

        btnClearAll=Button(billMenuFrame,text="Clear All",command=self.clearAll,cursor="hand2",font=("goudy old style",15,"bold"),bg="gray",fg="white")
        btnClearAll.place(x=124,y=80,width=120,height=50)

        btnGenerate=Button(billMenuFrame,text="Generate Bill",command=self.generateBill,cursor="hand2",font=("goudy old style",15,"bold"),bg="#009688",fg="white")
        btnGenerate.place(x=246,y=80,width=160,height=50)

        self.show()
        #self.billTop()
        self.updateDateTime()
#---------------------- all functions ------------------------------
    def getInput(self,num):
        xnum=self.varCalInput.get()+str(num)
        self.varCalInput.set(xnum)

    def clearCal(self):
        self.varCalInput.set('')

    def performCal(self):
        result=self.varCalInput.get()
        self.varCalInput.set(eval(result))

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.varSearch.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.varSearch.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def getData(self,ev):
        f=self.productTable.focus()
        content=(self.productTable.item(f))
        row=content['values']
        self.varPid.set(row[0])
        self.varPname.set(row[1])
        self.varPrice.set(row[2])
        self.lblInStock.config(text=f"In Stock [{str(row[3])}]")
        self.varStock.set(row[3])
        self.varQty.set('1')

    def getDataCart(self,ev):
        f=self.cartTable.focus()
        content=(self.cartTable.item(f))
        row=content['values']
        self.varPid.set(row[0])
        self.varPname.set(row[1])
        self.varPrice.set(row[2])
        self.varQty.set(row[3])
        self.lblInStock.config(text=f"In Stock [{str(row[4])}]")
        self.varStock.set(row[4])

    def addUpdateCart(self):
        if self.varPid.get()=="":
            messagebox.showerror("Error","Please select product from the list",parent=self.root)
        elif self.varQty.get()=="":
            messagebox.showerror("Error","Quantity is required",parent=self.root)
        elif int(self.varQty.get())>int(self.varStock.get()):
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)
        else:
            priceCal=self.varPrice.get()
            cartData=[self.varPid.get(),self.varPname.get(),priceCal,self.varQty.get(),self.varStock.get()]
            #---------- update cart --------------
            present="no"
            index=0
            for row in self.cartList:
                if self.varPid.get()==row[0]:
                    present="yes"
                    break
                index+=1
            if present=="yes":
                op=messagebox.askyesno("Confirm","Product already present\nDo you want to Update|Remove from the Cart List",parent=self.root)
                if op==True:
                    if self.varQty.get()=="0":
                        self.cartList.pop(index)
                    else:
                        self.cartList[index][3]=self.varQty.get()
            else:
                self.cartList.append(cartData)
            self.showCart()
            self.billUpdate()

    def billUpdate(self):
        self.billAmnt=0
        self.netPay=0
        self.siscount=0
        for row in self.cartList:
            self.billAmnt=self.billAmnt+(float(row[2])*int(row[3]))
        self.discount=(self.billAmnt*5)/100
        self.netPay=self.billAmnt-self.discount
        self.lblAmnt.config(text=f"Bill Amnt\n{str(self.billAmnt)}")
        self.lblNetPay.config(text=f"Net Pay\n{str(self.netPay)}")
        self.cartTitle.config(text=f"Cart \t Total Products: [{str(len(self.cartList))}]")

    def showCart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cartList:
                self.cartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def generateBill(self):
        if self.varCname.get()=="" or self.varContact.get()=="":
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cartList)==0:
            messagebox.showerror("Error",f"Please Add product to the Cart!!!",parent=self.root)
        else:
            #--------- bill top -----------------
            self.billTop()
            #--------- bill middle --------------
            self.billMiddle()
            #--------- bill bottom --------------
            self.billBottom()

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txtBillArea.get('1.0',END))
            fp.close()
            messagebox.showinfo("Saved","Bill has been generated",parent=self.root)
            self.chkPrint=1

    def billTop(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        billTopTemp=f'''
\t\tXYZ-Inventory
\t Phone No. 9899459288 , Delhi-110053
{str("="*46)}
 Customer Name: {self.varCname.get()}
 Ph. no. : {self.varContact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*46)}
 Product Name\t\t\tQTY\tPrice
{str("="*46)}
'''
        self.txtBillArea.delete('1.0',END)
        self.txtBillArea.insert('1.0',billTopTemp)

    def billBottom(self):
        billBottomTemp=f'''
{str("="*46)}
 Bill Amount\t\t\t\tRs.{self.billAmnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.netPay}
{str("="*46)}\n
'''
        self.txtBillArea.insert(END,billBottomTemp)

    def billMiddle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cartList:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status="Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txtBillArea.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                #------------- update qty in product table --------------
                cur.execute("update product set qty=?,status=? where pid=?",(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clearCart(self):
        self.varPid.set("")
        self.varPname.set("")
        self.varPrice.set("")
        self.varQty.set("")
        self.lblInStock.config(text=f"In Stock")
        self.varStock.set("")

    def clearAll(self):
        del self.cartList[:]
        self.clearCart()
        self.show()
        self.showCart()
        self.varCname.set("")
        self.varContact.set("")
        self.chkPrint=0
        self.txtBillArea.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Products: [0]")
        self.varSearch.set("")

    def updateDateTime(self):
        timeStr=time.strftime("%I:%M:%S")
        dateStr=time.strftime("%d-%m-%Y")
        self.lblClock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(dateStr)}\t\t Time: {str(timeStr)}")
        self.lblClock.after(200,self.updateDateTime)

    def printBill(self):
        if self.chkPrint==1:
            messagebox.showinfo("Print","Please wait while printing",parent=self.root)
            newFile=tempfile.mktemp('.txt')
            open(newFile,'w').write(self.txtBillArea.get('1.0',END))
            os.startfile(newFile,'print')
        else:
            messagebox.showinfo("Print","Please generate bill to print the receipt",parent=self.root)

if __name__=="__main__":
    root=Tk()
    obj=billClass(root)
    root.mainloop()
