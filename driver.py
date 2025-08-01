from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector

class ViolationSearchFrame:
    def __init__(self, master):
        self.master = master
        self.master.title("Violation Records")
        self.master.geometry("1530x790+0+0")
        self.create_widgets()

    def create_widgets(self):
        # Down Frame
        down_frame = Frame(self.master, bd=2, relief=RIDGE, bg='white')
        down_frame.place(x=10, y=10, width=1470, height=700)

        # Search Frame
        search_frame = LabelFrame(down_frame, bd=2, relief=RIDGE, text="Search Violation Record",
                                  font=('times new roman', 11, 'bold'), fg='red', bg='white')
        search_frame.place(x=0, y=0, width=1470, height=60)

        # Search type label and combo box
        search_by = Label(search_frame, text='Search By:', font=('arial', 11, 'bold'), bg='red', fg='white')
        search_by.grid(row=0, column=0, padx=5, sticky=W)

        self.var_com_search=StringVar()
        combo_search_box = ttk.Combobox(search_frame,textvariable=self.var_com_search,font=('arial', 11, 'bold'), width=18, state='readonly')
        combo_search_box['values'] = ('Select Option', 'DriverID', 'VehicleNo','Location','FirstName','LastName')
        combo_search_box.current(0)
        combo_search_box.grid(row=0, column=1, sticky=W, padx=5)

        # Search entry
        self.var_search=StringVar()
        search_type = ttk.Entry(search_frame,textvariable=self.var_search, width=18, font=('arial', 11, 'bold'))
        search_type.grid(row=0, column=2, padx=2, sticky=W)

        # Search and Show All buttons
        btn_search = Button(search_frame,command=self.search_data, text='Search', font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
        btn_search.grid(row=0, column=3, padx=3, pady=5)

        btn_all = Button(search_frame,command=self.fetch_data, text='Show All', font=('arial', 13, 'bold'), width=14, bg='blue', fg='white')
        btn_all.grid(row=0, column=4, padx=3, pady=5)

        # Title label
        vio_gen = Label(search_frame, text='NATIONAL VIOLATION AGENCY', font=('arial', 30, 'bold'),
                        bg='white', fg='crimson')
        vio_gen.grid(row=0, column=5, padx=50, sticky=W, pady=0)

        # Table Frame
        table_frame = Frame(down_frame, bd=2, relief=RIDGE)
        table_frame.place(x=0, y=60, width=1470, height=300)

        # Scroll bars
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.vio_table = ttk.Treeview(table_frame, columns=("1", "2", "3", "4", "5", "6", "7", "8","9","10","11","12","13","14","15"),
                                      xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.vio_table.xview)
        scroll_y.config(command=self.vio_table.yview)


        self.vio_table.heading('1',text='Driver ID')
        self.vio_table.heading('2',text='First Name')
        self.vio_table.heading('3',text='Last Name')
        self.vio_table.heading('4',text='DOB')
        self.vio_table.heading('5',text='gender')
        self.vio_table.heading('6',text='Address')
        self.vio_table.heading('7',text='City')
        self.vio_table.heading('8',text='State')
        self.vio_table.heading('9',text='House No')
        self.vio_table.heading('10',text='Violation ID')
        self.vio_table.heading('11',text='Violation Date')
        self.vio_table.heading('12',text='Location')
        self.vio_table.heading('13',text='Violation Type')
        self.vio_table.heading('14',text='Fine amount')
        self.vio_table.heading('15',text='Vehicle No')
    
        self.vio_table['show']='headings'

        self.vio_table.column('1',width=100)
        self.vio_table.column('2',width=100)
        self.vio_table.column('3',width=100)
        self.vio_table.column('4',width=100)
        self.vio_table.column('5',width=100)
        self.vio_table.column('6',width=100)
        self.vio_table.column('7',width=100)
        self.vio_table.column('8',width=100)
        self.vio_table.column('9',width=100)
        self.vio_table.column('10',width=100)
        self.vio_table.column('11',width=100)
        self.vio_table.column('12',width=100)
        self.vio_table.column('13',width=100)
        self.vio_table.column('14',width=100)
        self.vio_table.column('15',width=100)
        
        self.vio_table.pack(fill=BOTH, expand=1)

        
    #fetch data
    def fetch_data(self):
        conn=mysql.connector.connect(host='localhost',username='root',password='Harshitha@27',database='TrafficViolationManagement')
        my_cursor=conn.cursor()
        my_cursor.execute('select * from driverviolations')
        data=my_cursor.fetchall()
        if len(data)!=0:
            self.vio_table.delete(*self.vio_table.get_children())
            for i in data:
                self.vio_table.insert('',END,values=i)
            conn.commit()
        conn.close()


    # search
    def search_data(self):
        if not self.var_com_search.get().strip() or not self.var_search.get().strip():
            messagebox.showerror('Error', 'Both search field and value are required.')
            return
        try:
            # Database connection
            conn = mysql.connector.connect(
                host='localhost',
                username='root',
                password='Harshitha@27',
                database='TrafficViolationManagement'
            )
            my_cursor = conn.cursor()
            column_name = str(self.var_com_search.get()).strip()  # Column name
            search_value = '%' + str(self.var_search.get()).strip() + '%'  # Search term with wildcards
            query = f"SELECT * FROM driverviolations WHERE `{column_name}` LIKE %s"
            my_cursor.execute(query, (search_value,))
            rows = my_cursor.fetchall()
            if rows:
                self.vio_table.delete(*self.vio_table.get_children())
                for row in rows:
                    self.vio_table.insert('', 'end', values=row)
                messagebox.showinfo('Search Results', f'{len(rows)} record(s) found.')
            else:
                messagebox.showinfo('Search Results', 'No records found.')
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror('Error', f'Failed to fetch records: {err.msg}')


    

    


def main(user_type):
    root = Tk()
    obj=ViolationSearchFrame(root)
    root.mainloop()
