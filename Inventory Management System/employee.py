from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")

        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ all variables --------------
        self.varSearchby=StringVar()
        self.varSearchtxt=StringVar()
        self.varEmpId=StringVar()
        self.varGender=StringVar()
        self.varContact=StringVar()
        self.varName=StringVar()
        self.varDob=StringVar()
        self.varDoj=StringVar()
        self.varEmail=StringVar()
        self.varPass=StringVar()
        self.varUtype=StringVar()
        self.varSalary=StringVar()

        #---------- Search Frame -------------
        searchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        searchFrame.place(x=250,y=20,width=600,height=70)

        #------------ options ----------------
        cmbSearch=ttk.Combobox(searchFrame,textvariable=self.varSearchby,values=("Select","Email","Name","Contact"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmbSearch.place(x=10,y=10,width=180)
        cmbSearch.current(0)

        txtSearch=Entry(searchFrame,textvariable=self.varSearchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btnSearch=Button(searchFrame,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #-------------- title ---------------
        title=Label(self.root,text="Employee Details",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #-------------- content ---------------
        #---------- row 1 ----------------
        lblEmpid=Label(self.root,text="Emp ID",font=("goudy old style",15),bg="white").place(x=50,y=150)
        lblGender=Label(self.root,text="Gender",font=("goudy old style",15),bg="white").place(x=350,y=150)
        lblContact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=750,y=150)

        txtEmpid=Entry(self.root,textvariable=self.varEmpId,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180)
        cmbGender=ttk.Combobox(self.root,textvariable=self.varGender,values=("Select","Male","Female","Other"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmbGender.place(x=500,y=150,width=180)
        cmbGender.current(0)
        txtContact=Entry(self.root,textvariable=self.varContact,font=("goudy old style",15),bg="lightyellow").place(x=850,y=150,width=180)

        #---------- row 2 ----------------
        lblName=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=190)
        lblDob=Label(self.root,text="D.O.B.",font=("goudy old style",15),bg="white").place(x=350,y=190)
        lblDoj=Label(self.root,text="D.O.J.",font=("goudy old style",15),bg="white").place(x=750,y=190)

        txtName=Entry(self.root,textvariable=self.varName,font=("goudy old style",15),bg="lightyellow").place(x=150,y=190,width=180)
        txtDob=Entry(self.root,textvariable=self.varDob,font=("goudy old style",15),bg="lightyellow").place(x=500,y=190,width=180)
        txtDoj=Entry(self.root,textvariable=self.varDoj,font=("goudy old style",15),bg="lightyellow").place(x=850,y=190,width=180)

        #---------- row 3 ----------------
        lblEmail=Label(self.root,text="Email",font=("goudy old style",15),bg="white").place(x=50,y=230)
        lblPass=Label(self.root,text="Password",font=("goudy old style",15),bg="white").place(x=350,y=230)
        lblUtype=Label(self.root,text="User Type",font=("goudy old style",15),bg="white").place(x=750,y=230)

        txtEmail=Entry(self.root,textvariable=self.varEmail,font=("goudy old style",15),bg="lightyellow").place(x=150,y=230,width=180)
        txtPass=Entry(self.root,textvariable=self.varPass,font=("goudy old style",15),bg="lightyellow").place(x=500,y=230,width=180)
        cmbUtype=ttk.Combobox(self.root,textvariable=self.varUtype,values=("Admin","Employee"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmbUtype.place(x=850,y=230,width=180)
        cmbUtype.current(0)

        #---------- row 4 ----------------
        lblAddress=Label(self.root,text="Address",font=("goudy old style",15),bg="white").place(x=50,y=270)
        lblSalary=Label(self.root,text="Salary",font=("goudy old style",15),bg="white").place(x=500,y=270)

        self.txtAddress=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txtAddress.place(x=150,y=270,width=300,height=60)
        txtSalary=Entry(self.root,textvariable=self.varSalary,font=("goudy old style",15),bg="lightyellow").place(x=600,y=270,width=180)

        #-------------- buttons -----------------
        btnAdd=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btnUpdate=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btnDelete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btnClear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=305,width=110,height=28)

        #------------ employee details -------------
        empFrame=Frame(self.root,bd=3,relief=RIDGE)
        empFrame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(empFrame,orient=VERTICAL)
        scrollx=Scrollbar(empFrame,orient=HORIZONTAL)\

        self.employeeTable=ttk.Treeview(empFrame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.employeeTable.xview)
        scrolly.config(command=self.employeeTable.yview)
        self.employeeTable.heading("eid",text="EMP ID")
        self.employeeTable.heading("name",text="Name")
        self.employeeTable.heading("email",text="Email")
        self.employeeTable.heading("gender",text="Gender")
        self.employeeTable.heading("contact",text="Contact")
        self.employeeTable.heading("dob",text="D.O.B")
        self.employeeTable.heading("doj",text="D.O.J")
        self.employeeTable.heading("pass",text="Password")
        self.employeeTable.heading("utype",text="User Type")
        self.employeeTable.heading("address",text="Address")
        self.employeeTable.heading("salary",text="Salary")
        self.employeeTable["show"]="headings"
        self.employeeTable.column("eid",width=90)
        self.employeeTable.column("name",width=100)
        self.employeeTable.column("email",width=100)
        self.employeeTable.column("gender",width=100)
        self.employeeTable.column("contact",width=100)
        self.employeeTable.column("dob",width=100)
        self.employeeTable.column("doj",width=100)
        self.employeeTable.column("pass",width=100)
        self.employeeTable.column("utype",width=100)
        self.employeeTable.column("address",width=100)
        self.employeeTable.column("salary",width=100)

        self.employeeTable.pack(fill=BOTH,expand=1)
        self.employeeTable.bind("<ButtonRelease-1>",self.getData)
        self.show()
#-----------------------------------------------------------------------------------------------------
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.varEmpId.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.varEmpId.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID is already assigned",parent=self.root)
                else:
                    cur.execute("insert into employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.varEmpId.get(),
                        self.varName.get(),
                        self.varEmail.get(),
                        self.varGender.get(),
                        self.varContact.get(),
                        self.varDob.get(),
                        self.varDoj.get(),
                        self.varPass.get(),
                        self.varUtype.get(),
                        self.txtAddress.get('1.0',END),
                        self.varSalary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Added Successfully",parent=self.root)
                    self.clear()
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.employeeTable.delete(*self.employeeTable.get_children())
            for row in rows:
                self.employeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def getData(self,ev):
        f=self.employeeTable.focus()
        content=(self.employeeTable.item(f))
        row=content['values']
        self.varEmpId.set(row[0])
        self.varName.set(row[1])
        self.varEmail.set(row[2])
        self.varGender.set(row[3])
        self.varContact.set(row[4])
        self.varDob.set(row[5])
        self.varDoj.set(row[6])
        self.varPass.set(row[7])
        self.varUtype.set(row[8])
        self.txtAddress.delete('1.0',END)
        self.txtAddress.insert(END,row[9])
        self.varSalary.set(row[10])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.varEmpId.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.varEmpId.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    cur.execute("update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                        self.varName.get(),
                        self.varEmail.get(),
                        self.varGender.get(),
                        self.varContact.get(),
                        self.varDob.get(),
                        self.varDoj.get(),
                        self.varPass.get(),
                        self.varUtype.get(),
                        self.txtAddress.get('1.0',END),
                        self.varSalary.get(),
                        self.varEmpId.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.varEmpId.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.varEmpId.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.varEmpId.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear(self):
        self.varEmpId.set("")
        self.varName.set("")
        self.varEmail.set("")
        self.varGender.set("Select")
        self.varContact.set("")
        self.varDob.set("")
        self.varDoj.set("")
        self.varPass.set("")
        self.varUtype.set("Admin")
        self.txtAddress.delete('1.0',END)
        self.varSalary.set("")
        self.varSearchby.set("Select")
        self.varSearchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.varSearchby.get()=="Select":
                messagebox.showerror("Error","Select Search By option",parent=self.root)
            elif self.varSearchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select * from employee where "+self.varSearchby.get()+" LIKE '%"+self.varSearchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.employeeTable.delete(*self.employeeTable.get_children())
                    for row in rows:
                        self.employeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


if __name__=="__main__":
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()
