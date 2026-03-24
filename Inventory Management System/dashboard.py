from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import sqlite3
import os

from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from billing import billClass

from helpers import font

# ------------------ BASE PATH SETUP ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
BILL_DIR = os.path.join(BASE_DIR, "bill")

os.makedirs(BILL_DIR, exist_ok=True)
# ---------------------------------------------------

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        # ------------- title --------------
        self.iconTitle = PhotoImage(file=os.path.join(IMAGE_DIR, "logo1.png"))
        Label(
            self.root,
            text="Inventory Management System",
            image=self.iconTitle,
            compound=LEFT,
            font=(font, 40, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20
        ).place(x=0, y=0, relwidth=1, height=70)

        # ------------ logout button -----------
        Button(
            self.root, text="Logout",
            font=(font, 15, "bold"),
            bg="yellow", cursor="hand2"
        ).place(x=1150, y=10, height=50, width=150)

        # ------------ clock -----------------
        self.lblClock = Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",
            font=(font, 15),
            bg="#4d636d", fg="white"
        )
        self.lblClock.place(x=0, y=70, relwidth=1, height=30)

        # ---------------- left menu ---------------
        self.menuLogo = Image.open(os.path.join(IMAGE_DIR, "menu_im.png"))
        self.menuLogo = self.menuLogo.resize((200, 200))
        self.menuLogo = ImageTk.PhotoImage(self.menuLogo)

        leftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        leftMenu.place(x=0, y=102, width=200, height=565)

        lblMenuLogo = Label(leftMenu, image=self.menuLogo)
        lblMenuLogo.pack(side=TOP, fill=X)

        Label(
            leftMenu, text="Menu",
            font=(font, 20),
            bg="#009688"
        ).pack(side=TOP, fill=X)

        self.iconSide = PhotoImage(file=os.path.join(IMAGE_DIR, "side.png"))

        self.categories = [ 
            {"id": "employee",  "name": "Employee", "color": "#33bbf9", "labelName": "lblEmployee", "x": 300, "y": 120}, 
            {"id": "supplier",  "name": "Supplier", "color": "#ff5722", "labelName": "lblSupplier", "x": 650, "y": 120}, 
            {"id": "category",  "name": "Category", "color": "#009688", "labelName": "lblCategory", "x": 1000,"y": 120}, 
            {"id": "product",   "name": "Products", "color": "#607d8b", "labelName": "lblProduct",  "x": 300, "y": 300}, 
            {"id": "sales",     "name": "Sales",    "color": "#ffc107", "labelName": "lblSales",    "x": 650, "y": 300}, 
            {"id": "exit",      "name": "Exit",     "color": "#f44336",                             "x": 1000,"y": 300}]
        # creates the buttons for the left menu and content elements on the main page
        for item in self.categories:
            Button(
                leftMenu, text=item["name"], command=lambda id=item["id"]: self.openModule(id),
                image=self.iconSide, compound=LEFT,
                padx=5, anchor="w",
                font=(font, 20, "bold"),
                bg="white", bd=3, cursor="hand2"
            ).pack(side=TOP, fill=X)        
            
            # Content for the main page
            if item["id"] != "exit":
                self.__dict__[item["labelName"]] = Label(
                    self.root, text=f"Total {item['name']}\n{{ 0 }}",
                    bd=5, relief=RIDGE, bg=item["color"],
                    fg="white", font=(font, 20, "bold")
                )
                self.__dict__[item["labelName"]].place(x=item["x"], y=item["y"], height=150, width=300)

        # ------------ open billing -----------------
        Button(
            self.root, text="Open Billing",
            command=lambda: self.openModule("billing"),
            font=(font, 15, "bold"),
            bg="#00FF0D", fg="white", cursor="hand2"
        ).place(x=1100, y=620, width=200, height=50)

        # ------------ footer -----------------
        Label(
            self.root,
            text="IMS-Inventory Management System",
            font=(font, 12),
            bg="#4d636d", fg="white"
        ).pack(side=BOTTOM, fill=X)

        self.updateContent()

    # -------------- functions ----------------
    def openModule(self, id):
        self.newWin = Toplevel(self.root)
        if id == "employee":
            self.app = employeeClass(self.newWin)
        elif id == "supplier":
            self.app = supplierClass(self.newWin)
        elif id == "category":
            self.app = categoryClass(self.newWin)
        elif id == "product":
            self.app = productClass(self.newWin)
        elif id == "sales":
            self.app = salesClass(self.newWin)
        elif id == "billing":
            self.app = billClass(self.newWin)
        elif id == "exit":
            self.root.destroy()

    def updateContent(self):
        con = sqlite3.connect(database=os.path.join(BASE_DIR, 'ims.db'))
        cur = con.cursor()

        try:
            for item in self.categories:
                if item["id"] != "exit" and item["id"] != "sales":
                    cur.execute(f"select * from {item['id'].lower()}")
                    data = cur.fetchall()
                    self.__dict__[item["labelName"]].config(text=f"Total {item['name']}\n[ {len(data)} ]")

            bill = len(os.listdir(BILL_DIR))
            self.lblSales.config(text=f"Total Sales\n[ {bill} ]")

            timeStr = time.strftime("%I:%M:%S")
            dateStr = time.strftime("%d-%m-%Y")
            self.lblClock.config(
                text=f"Welcome to Inventory Management System\t\t Date: {dateStr}\t\t Time: {timeStr}"
            )

            self.lblClock.after(200, self.updateContent)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
