import tkinter as tk
from tkinter import messagebox
import sqlite3

class MainPage:
    def __init__(self, rootObj):
        # SQLITE3
        self.conn = None
        self.curser = None
        # self.generateDB()
        # self.registerUser()
        self.connectDB()
        # Login Form
        self.login(rootObj)

    def generateDB(self):
        ''' 
            generate database file if doesnot exist
            Connect to SQLite database (or create one if it doesn't exist) 
        '''
        self.conn = sqlite3.connect("usersDB.db")
        self.cursor = self.conn.cursor()
        # Create a table (if not exists)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                passw TEXT NOT NULL,
                mail TEXT NOT NULL
            )
        """)
        self.conn.commit()
    
    def registerUser(self):
        ''' 
            Add New User into database
        '''
        name = "admin"              #   get details from registration form 
        passw = "password"          #   get details from registration form or Image Template
        mail = "test@gmail.com"     #   get details from registration form        
        if name and passw:
            try:
                self.cursor.execute("INSERT INTO users (name, passw, mail) VALUES (?, ?, ?)", (name, passw, mail))
                self.conn.commit()
                messagebox.showinfo("Success", "User added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add user: {e}")
        else:
            messagebox.showwarning("Input Error", "Please enter both name and age!")

    def connectDB(self):
        self.conn = sqlite3.connect("usersDB.db")
        self.cursor = self.conn.cursor()

    def login(self, rootObj):
        rootObj.title("Tkinter Form with Class")
        rootObj.geometry("300x400")
        self.label_name = tk.Label(rootObj, text="Name:")
        self.label_name.pack(pady=5)
        self.entry_name = tk.Entry(rootObj)
        self.entry_name.pack(pady=5)
        self.label_pass = tk.Label(rootObj, text="pass:")
        self.label_pass.pack(pady=5)
        self.entry_pass = tk.Entry(rootObj)
        self.entry_pass.pack(pady=5)
        self.label_mail = tk.Label(rootObj, text="mail:")
        self.label_mail.pack(pady=5)
        self.entry_mail = tk.Entry(rootObj)
        self.entry_mail.pack(pady=5)
        self.submit_button = tk.Button(rootObj, text="Submit", command=self.validate_login)
        self.submit_button.pack(pady=10)
        return True
    
    # Function to validate the login
    def validate_login(self):
        userid = self.entry_name.get()
        password = self.entry_pass.get()
        self.cursor.execute("SELECT * FROM users WHERE name = ? AND passw = ?", (userid, password))
        userid = self.cursor.fetchone() 
        if userid :
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.open_dashboard(userid)  # Open dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_dashboard(self, username):
        """Function to open the dashboard window"""
        dashboard = tk.Tk()
        dashboard.title("Dashboard")
        dashboard.geometry("600x300")

        tk.Label(dashboard, text=f"Welcome {username[1]} to the Dashboard!", font=("Arial", 16)).pack(pady=20)

        logout_button = tk.Button(dashboard, text="Logout", command=dashboard.destroy)
        logout_button.pack(pady=10)

        dashboard.mainloop()

if __name__ == "__main__":
    rootObj = tk.Tk()
    app = MainPage(rootObj)
    rootObj.mainloop()




