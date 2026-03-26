from tkinter import*
from tkinter import ttk,messagebox
import sqlite3
from helpers import setHeadingsAndColumns, addRecord, showRecord, getRecordData, updateRecord, deleteRecord, searchRecord, font

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
        searchFrame=LabelFrame(self.root,text="Search Employee",font=(font,12,"bold"),bd=2,relief=RIDGE,bg="white")
        searchFrame.place(x=250,y=20,width=600,height=70)

        #------------ options ----------------
        cmbSearch=ttk.Combobox(searchFrame,textvariable=self.varSearchby,values=("Select","Email","Name","Contact"),state='readonly',justify=CENTER,font=(font,15))
        cmbSearch.place(x=10,y=10,width=180)
        cmbSearch.current(0)

        Entry(searchFrame,textvariable=self.varSearchtxt,font=(font,15),bg="lightyellow").place(x=200,y=10)
        Button(searchFrame,command=self.search,text="Search",font=(font,15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #-------------- title ---------------
        Label(self.root,text="Employee Details",font=(font,15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #-------------- content ---------------
        
        #---------- label creation ----------------
        labels = [{"label": "Emp ID", "x": 50, "y": 150},
                  {"label": "Gender", "x": 350, "y": 150},
                  {"label": "Contact", "x": 750, "y": 150},
                  {"label": "Name", "x": 50, "y": 190},
                  {"label": "D.O.B.", "x": 350, "y": 190},
                  {"label": "D.O.J.", "x": 750, "y": 190},
                  {"label": "Email", "x": 50, "y": 230},
                  {"label": "Password", "x": 350, "y": 230},
                  {"label": "User Type", "x": 750, "y": 230},
                  {"label": "Address", "x": 50, "y": 270},
                  {"label": "Salary", "x": 500, "y": 270}]

        for label in labels:
            Label(self.root, text=label["label"], font=(font, 15), bg="white").place(x=label["x"], y=label["y"])


        entries = [{"variable": self.varEmpId, "x": 150, "y": 150},
                   {"variable": self.varGender, "x": 500, "y": 150},
                   {"variable": self.varContact, "x": 850, "y": 150},
                   {"variable": self.varName, "x": 150, "y": 190},
                   {"variable": self.varDob, "x": 500, "y": 190},
                   {"variable": self.varDoj, "x": 850, "y": 190},
                   {"variable": self.varEmail, "x": 150, "y": 230},
                   {"variable": self.varPass, "x": 500, "y": 230},
                   {"variable": self.varUtype, "x": 850, "y": 230},
                   {"variable": self.varSalary, "x": 600, "y": 270}]
        
        #---------- entry creation ----------------
        for entry in entries:
            if entry["variable"] in [self.varGender, self.varUtype]:
                cmb = ttk.Combobox(self.root, textvariable=entry["variable"], state='readonly', justify=CENTER, font=(font, 15))
                if entry["variable"] == self.varGender:
                    cmb['values'] = ("Select", "Male", "Female", "Other")
                else:
                    cmb['values'] = ("Admin", "Employee")
                cmb.place(x=entry["x"], y=entry["y"], width=180)
                cmb.current(0)
            else:
                Entry(self.root, textvariable=entry["variable"], font=(font, 15), bg="lightyellow").place(x=entry["x"], y=entry["y"], width=180)

        self.txtAddress = Text(self.root, font=(font, 15), bg="lightyellow")
        self.txtAddress.place(x=150, y=270, width=300, height=60)

        #-------------- buttons -----------------
        Button(self.root,text="Save",command=self.add,font=(font,15),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
        Button(self.root,text="Update",command=self.update,font=(font,15),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
        Button(self.root,text="Delete",command=self.delete,font=(font,15),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
        Button(self.root,text="Clear",command=self.clear,font=(font,15),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=305,width=110,height=28)

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
        setHeadingsAndColumns(self.employeeTable, "eid", "EMP ID", 90)
        setHeadingsAndColumns(self.employeeTable, "name", "Name", 100)
        setHeadingsAndColumns(self.employeeTable, "email", "Email", 100)
        setHeadingsAndColumns(self.employeeTable, "gender", "Gender", 100)
        setHeadingsAndColumns(self.employeeTable, "contact", "Contact", 100)
        setHeadingsAndColumns(self.employeeTable, "dob", "D.O.B", 100)
        setHeadingsAndColumns(self.employeeTable, "doj", "D.O.J", 100)
        setHeadingsAndColumns(self.employeeTable, "pass", "Password", 100)
        setHeadingsAndColumns(self.employeeTable, "utype", "User Type", 100)
        setHeadingsAndColumns(self.employeeTable, "address", "Address", 100)
        setHeadingsAndColumns(self.employeeTable, "salary", "Salary", 100)
        self.employeeTable["show"]="headings"

        self.employeeTable.pack(fill=BOTH,expand=1)
        self.employeeTable.bind("<ButtonRelease-1>",self.getData)
        self.show()
#-----------------------------------------------------------------------------------------------------

    #Add a new employee to the database
    def add(self):
        if self.varEmpId.get()=="":
            messagebox.showerror("Error","Employee ID must be required",parent=self.root)
        else:
            labels=["eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"]
            data=[
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
            ]
            if addRecord("employee","eid",self.varEmpId,labels,data,self.root):
                self.clear()
                self.show()

    #Display all employees in the employee table
    def show(self):
        showRecord("employee",self.employeeTable)

    #Get the selected employee data and populate the fields for editing or deletion
    def getData(self,ev):
        getRecordData(self.employeeTable,[self.varEmpId,self.varName,self.varEmail,self.varGender,self.varContact,self.varDob,self.varDoj,self.varPass,self.varUtype,self.txtAddress,self.varSalary])

    #Update the selected employee's information in the database
    def update(self):
        if self.varEmpId.get()=="":
            messagebox.showerror("Error","Employee ID must be required",parent=self.root)
        else:
            labels=["name","email","gender","contact","dob","doj","pass","utype","address","salary"]
            data=[
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
            ]
            if updateRecord("employee","eid",self.varEmpId,labels,data,self.root):
                self.show()

    #Delete the selected employee from the database
    def delete(self):
        if self.varEmpId.get()=="":
            messagebox.showerror("Error","Employee ID must be required",parent=self.root)
        else:
            if deleteRecord("employee","eid",self.varEmpId,self.root):
                self.clear()

    #Clear all input fields
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

    #Search for employees based on the selected search criteria and input text
    def search(self):
        if self.varSearchby.get()=="Select":
            messagebox.showerror("Error","Select Search By option",parent=self.root)
        elif self.varSearchtxt.get()=="":
            messagebox.showerror("Error","Search input should be required",parent=self.root)
        else:
            searchRecord("employee",self.varSearchby.get(),self.varSearchtxt,self.employeeTable,self.root)


if __name__=="__main__":
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()
