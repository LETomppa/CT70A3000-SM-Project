from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os

# ------------------ BASE PATH SETUP ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
BILL_DIR = os.path.join(BASE_DIR, "bill")

os.makedirs(BILL_DIR, exist_ok=True)
# ---------------------------------------------------

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()

        self.blllList = []
        self.varInvoice = StringVar()

        # --------------- title ---------------------
        Label(
            self.root,
            text="View Customer Bills",
            font=("goudy old style", 30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE
        ).pack(side=TOP, fill=X, padx=10, pady=20)

        lblInvoice = Label(self.root, text="Invoice No.", font=("times new roman", 15), bg="white")
        lblInvoice.place(x=50, y=100)

        txtInvoice = Entry(self.root, textvariable=self.varInvoice, font=("times new roman", 15), bg="lightyellow")
        txtInvoice.place(x=160, y=100, width=180, height=28)

        Button(
            self.root, text="Search", command=self.search,
            font=("times new roman", 15, "bold"),
            bg="#2196f3", fg="white", cursor="hand2"
        ).place(x=360, y=100, width=120, height=28)

        Button(
            self.root, text="Clear", command=self.clear,
            font=("times new roman", 15, "bold"),
            bg="lightgray", cursor="hand2"
        ).place(x=490, y=100, width=120, height=28)

        # ----------------- bill list -------------------
        salesFrame = Frame(self.root, bd=3, relief=RIDGE)
        salesFrame.place(x=50, y=140, width=200, height=330)

        scrolly = Scrollbar(salesFrame, orient=VERTICAL)
        self.salesList = Listbox(
            salesFrame, font=("goudy old style", 15),
            bg="white", yscrollcommand=scrolly.set
        )
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.salesList.yview)
        self.salesList.pack(fill=BOTH, expand=1)
        self.salesList.bind("<ButtonRelease-1>", self.getData)

        # --------------- bill area ----------------------
        billFrame = Frame(self.root, bd=3, relief=RIDGE)
        billFrame.place(x=280, y=140, width=410, height=330)

        Label(
            billFrame, text="Customer Bill Area",
            font=("goudy old style", 20), bg="orange"
        ).pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(billFrame, orient=VERTICAL)
        self.billArea = Text(billFrame, bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.billArea.yview)
        self.billArea.pack(fill=BOTH, expand=1)

        # ------------- image -----------------
        imagePath = os.path.join(IMAGE_DIR, "cat2.jpg")
        self.billPhoto = Image.open(imagePath)
        self.billPhoto = self.billPhoto.resize((450, 300))
        self.billPhoto = ImageTk.PhotoImage(self.billPhoto)

        lblImage = Label(self.root, image=self.billPhoto, bd=0)
        lblImage.place(x=700, y=110)

        self.show()

    # -------------------------------------------------------
    def show(self):
        del self.blllList[:]
        self.salesList.delete(0, END)

        for i in os.listdir(BILL_DIR):
            if i.split('.')[-1] == 'txt':
                self.salesList.insert(END, i)
                self.blllList.append(i.split('.')[0])

    def getData(self, ev):
        index = self.salesList.curselection()
        if not index:
            return

        fileName = self.salesList.get(index)
        self.billArea.delete('1.0', END)

        filePath = os.path.join(BILL_DIR, fileName)
        with open(filePath, 'r') as fp:
            for i in fp:
                self.billArea.insert(END, i)

    def search(self):
        if self.varInvoice.get() == "":
            messagebox.showerror("Error", "Invoice no. should be required", parent=self.root)
        else:
            if self.varInvoice.get() in self.blllList:
                filePath = os.path.join(BILL_DIR, f"{self.varInvoice.get()}.txt")
                self.billArea.delete('1.0', END)

                with open(filePath, 'r') as fp:
                    for i in fp:
                        self.billArea.insert(END, i)
            else:
                messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)

    def clear(self):
        self.show()
        self.billArea.delete('1.0', END)


if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
