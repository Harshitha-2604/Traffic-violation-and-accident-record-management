# from tkinter import *
# import tkinter as tk
# from tkinter import messagebox
# from tkinter import ttk
# import driverinfo  # Import the traffic module to call its main function
# import driver
# import mysql.connector

# def login():
#     username = entry_username.get()  # Get the username from the entry
#     password = entry_password.get()  # Get the password from the entry
#     user_type = combo_user_type.get()  # Get the selected user type

#     if username == "" or password == "":
#         messagebox.showerror('Error', 'All fields are required')
#     else:
#         if user_type == "Officer":
#             # Officer login requires database validation
#             try:
#                 # Connect to MySQL database
#                 conn = mysql.connector.connect(
#                     host='localhost',
#                     username='root',
#                     password='Harshitha@27',
#                     database='loginpage'
#                 )
#                 my_cur = conn.cursor()

#                 # Check if username and password exist in the login table
#                 my_cur.execute('SELECT * FROM officerlogin WHERE Username = %s AND pass = %s', (username, int(password)))
#                 result = my_cur.fetchone()  # Fetch one record that matches the query
                
#                 if result:
#                     # If a record is found, login is successful
#                     messagebox.showinfo('Success', 'Login successful')
#                     root.destroy()  # Close the login window
#                     driverinfo.main(user_type)  # Open the main application page
#                 else:
#                     # If no record is found, show an error
#                     messagebox.showerror('Error', 'Invalid username or password for Officer')

#                 conn.close()
#             except Exception as ec:
#                 messagebox.showerror('Error', f'Database error: {str(ec)}')
#         else:
#             try:
#                 # Connect to MySQL database
#                 conn = mysql.connector.connect(
#                     host='localhost',
#                     username='root',
#                     password='Harshitha@27',
#                     database='loginpage'
#                 )
#                 my_cur = conn.cursor()

#                 # Insert login data into the 'logindriver' table
#                 try:
#                     my_cur.execute('INSERT INTO driverlogin (pass, Username) VALUES (%s, %s)', (int(password), username))
#                     conn.commit()
#                     messagebox.showinfo('Success', 'Login successful')

#                     # Close the login window and open the main application
#                     root.destroy()
#                     driver.main(user_type)  # Pass user_type to the main application
#                 except mysql.connector.IntegrityError as e:
#                     # Trigger error handling for duplicate username or other integrity constraints
#                     messagebox.showerror('Database Error', 'Username already exists or another database constraint was violated.')
#                 finally:
#                     conn.close()
#             except Exception as ec:
#                 messagebox.showerror('Error', f'Error in database operation: {str(ec)}')


# # Set up Tkinter GUI
# root = tk.Tk()
# root.title("Login Page")
# root.geometry("300x250")

# tk.Label(root, text="User Type:").pack(pady=5)
# combo_user_type = ttk.Combobox(root, values=["Officer", "Driver"])
# combo_user_type.pack(pady=5)
# combo_user_type.current(0)  # Set default selection to "Officer"

# tk.Label(root, text="Username:").pack(pady=5)
# entry_username = tk.Entry(root)
# entry_username.pack(pady=5)

# tk.Label(root, text="Password:").pack(pady=5)
# entry_password = tk.Entry(root, show="*")
# entry_password.pack(pady=5)

# tk.Button(root, text="Login", command=login).pack(pady=20)


# root.mainloop()


import tkinter as tk
from tkinter import messagebox
import mysql.connector
import driverinfo  # Import the driverinfo module
import driver  # Import the driver module

# Function to connect to the database
def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Root user
        password='Harshitha@27',  # Root password
        database='trafficviolationmanagement'  # Database name
    )

# Login Window Class
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("800x600")

        tk.Label(self, text="Username:").pack(pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:").pack(pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Label(self, text="Role:").pack(pady=10)
        self.role_entry = tk.Entry(self)  # Role: Officer or Driver
        self.role_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get().lower()  # Normalize input to lowercase

        if not username or not password or not role:
            messagebox.showerror("Error", "Please enter username, password, and role.")
            return

        db = connect_to_db()
        cursor = db.cursor()

        try:
            # Query to validate login credentials and role
            cursor.execute("SELECT username, role FROM userlogin WHERE username = %s AND pass = %s AND role = %s", 
                           (username, password, role.capitalize()))
            user = cursor.fetchone()

            if user:
                # Grant privileges based on the role
                self.grant_privileges(role, db, cursor)
                self.destroy()  # Close the login window

                # Navigate to the appropriate module
                if role == 'officer':
                    messagebox.showinfo("Success", f"Welcome Officer {username}!")
                    driverinfo.main("Officre")  # Open the Officer dashboard from driverinfo module
                elif role == 'driver':
                    messagebox.showinfo("Success", f"Welcome Driver {username}!")
                    driver.main("Driver")  # Open the Driver dashboard from driver module
            else:
                messagebox.showerror("Error", "Invalid username, password, or role.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            db.close()

    def grant_privileges(self, role, db, cursor):
        try:
            if role == 'officer':
                # Ensure the user exists before granting privileges
                cursor.execute("CREATE USER IF NOT EXISTS 'officer'@'localhost' IDENTIFIED BY 'OfficerPassword';")
                cursor.execute("GRANT ALL PRIVILEGES ON trafficviolationmanagement.* TO 'officer'@'localhost';")
            elif role == 'driver':
                # Ensure the user exists before granting privileges
                cursor.execute("CREATE USER IF NOT EXISTS 'driver'@'localhost' IDENTIFIED BY 'DriverPassword';")
                cursor.execute("GRANT SELECT ON trafficviolationmanagement.* TO 'driver'@'localhost';")
            else:
                messagebox.showerror("Error", "Invalid role for granting privileges.")
                return

            db.commit()
            print(f"Privileges granted successfully for role: {role.capitalize()}")
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error granting privileges: {err}")

# Run the login window
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
