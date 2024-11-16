from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox
import victim

class Traffic:
    def __init__(self,root):
        self.root=root
        self.root.geometry('1530x790+0+0')
        self.root.title("Traffic Management System")

        #varibles
        self.var_acc_id=StringVar()
        self.var_vehicle_no=StringVar()


        lbl_title=Label(self.root,text="TRAFFIC MANAGEMENT SYSYTEM SOFTWARE",font=('times new roman',40,'bold'),bg='black',fg='gold')
        lbl_title.place(x=0,y=0,width=1530,height=70)

        image_logo=Image.open('images/logo.png')
        image_logo=image_logo.resize((60,60),Image.Resampling.LANCZOS)
        self.photo_logo=ImageTk.PhotoImage(image_logo)
        

        self.logo=Label(self.root,image=self.photo_logo)
        self.logo.place(x=80,y=5,width=60,height=60)

        #image frame
        img_frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        img_frame.place(x=0,y=70,width=1530,height=130)

        #1
        img1=Image.open('images/face1.jpeg')
        img1=img1.resize((540,160),Image.Resampling.LANCZOS)
        self.photo1=ImageTk.PhotoImage(img1)
        
        self.img_1=Label(img_frame,image=self.photo1)
        self.img_1.place(x=0,y=0,width=540,height=160)

        #2
        img2=Image.open('images/face2.jpeg')
        img2=img2.resize((540,160),Image.Resampling.LANCZOS)
        self.photo2=ImageTk.PhotoImage(img2)
        
        self.img_2=Label(img_frame,image=self.photo2)
        self.img_2.place(x=540,y=0,width=540,height=160)

        #3
        img3=Image.open('images/face3.jpeg')
        img3=img3.resize((540,160),Image.Resampling.LANCZOS)
        self.photo3=ImageTk.PhotoImage(img3)
        
        self.img_3=Label(img_frame,image=self.photo3)
        self.img_3.place(x=1000,y=0,width=540,height=160)

        #main frame
        Main_frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        Main_frame.place(x=10,y=200,width=1500,height=560)
        
        #upper frame
        upper_frame=LabelFrame(Main_frame,bd=2,relief=RIDGE,text="Accident-Vehicle Information",font=('times new roman',11,'bold'),fg='red',bg='white')
        upper_frame.place(x=10,y=10,width=1480,height=270)

        # Label entry

        #Accident ID
        Caseid=Label(upper_frame,text='Accident ID:',font=('arial',11,'bold'),bg='white')
        Caseid.grid(row=0,column=0,padx=2,sticky=W)

        casentry=ttk.Entry(upper_frame,textvariable=self.var_acc_id,width=22,font=('arial',11,'bold'))
        casentry.grid(row=0,column=1,padx=2,sticky=W)


        #vehcile No
        vioid=Label(upper_frame,text='Vehicle No:',font=('arial',12,'bold'),bg='white')
        vioid.grid(row=0,column=2,padx=2,pady=7,sticky=W)

        vioentry=ttk.Entry(upper_frame,textvariable=self.var_vehicle_no,width=22,font=('arial',11,'bold'))
        vioentry.grid(row=0,column=3,padx=2,pady=7)



        #buttons
        Button_frame=Frame(upper_frame,bd=2,relief=RIDGE,bg='White')
        Button_frame.place(x=5,y=200,width=820,heigh=45)

        # add button
        btn_add=Button(Button_frame,command=self.add_data,text='Record Save',font=('arial',13,'bold'),width=14,bg='blue',fg='white')
        btn_add.grid(row=0,column=0,padx=3,pady=5)

        #update
        btn_upd=Button(Button_frame,command=self.update_data,text='Update',font=('arial',13,'bold'),width=14,bg='blue',fg='white')
        btn_upd.grid(row=0,column=1,padx=3,pady=5)

        #delete
        btn_del=Button(Button_frame,command=self.delete_data,text='Delete',font=('arial',13,'bold'),width=14,bg='blue',fg='white')
        btn_del.grid(row=0,column=2,padx=3,pady=5)

        #clear
        btn_clear=Button(Button_frame,text='Clear',font=('arial',13,'bold'),width=14,bg='blue',fg='white')
        btn_clear.grid(row=0,column=3,padx=3,pady=5)

        
        #next
        btn_clear=Button(Button_frame,command=self.open_next_page,text='Next',font=('arial',13,'bold'),width=14,bg='blue',fg='white')
        btn_clear.grid(row=0,column=4,padx=3,pady=5)

        

        #bg right-side image
        bgimg=Image.open('images/violation.jpeg')
        bgimg=bgimg.resize((470,245),Image.Resampling.LANCZOS)
        self.photocrime=ImageTk.PhotoImage(bgimg)
        
        self.bgimg=Label(upper_frame,image=self.photocrime)
        self.bgimg.place(x=1000,y=0,width=470,height=245)

        #Down frame
        down_frame=LabelFrame(Main_frame,bd=2,relief=RIDGE,text="Traffic Violation Information Table",font=('times new roman',11,'bold'),fg='red',bg='white')
        down_frame.place(x=10,y=280,width=1480,height=270)

        #search frame
        search_frame=LabelFrame(down_frame,bd=2,relief=RIDGE,text="Search Violation Record",font=('times new roman',11,'bold'),fg='red',bg='white')
        search_frame.place(x=0,y=0,width=1470,height=60)


        #Search type
        search_by=Label(search_frame,text='Search By:',font=('arial',11,'bold'),bg='red',fg='white')
        search_by.grid(row=0,column=0,padx=5,sticky=W)

        combo_search_box=ttk.Combobox(search_frame,font=('arial',11,'bold'),width=18,state='readonly')
        combo_search_box['value']=('Select Option','Case_id','Violation ID','Driver ID')
        combo_search_box.current(0)
        combo_search_box.grid(row=0,column=1,sticky=W,padx=5)

        search_type=ttk.Entry(search_frame,width=18,font=('arial',11,'bold'))
        search_type.grid(row=0,column=2,padx=2,sticky=W)

        #search
        btn_search=Button(search_frame,text='Search',font=('arial',13,'bold'),width=14,bg='blue',fg='white')
        btn_search.grid(row=0,column=3,padx=3,pady=5)

        #all
        btn_all=Button(search_frame,text='Show All',font=('arial',13,'bold'),width=14,bg='blue',fg='white')
        btn_all.grid(row=0,column=4,padx=3,pady=5)

        vio_gen=Label(search_frame,text='NATIONAL VIOLATION AGENCY',font=('arial',30,'bold'),bg='white',fg='crimson')
        vio_gen.grid(row=0,column=5,padx=50,sticky=W,pady=0)

        #table frame
        table_frame=Frame(down_frame,bd=2,relief=RIDGE)
        table_frame.place(x=0,y=60,width=1470,height=170)


        #scroll bar
        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.vio_table=ttk.Treeview(table_frame,column=("1","2"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.vio_table.xview)
        scroll_y.config(command=self.vio_table.yview)

        self.vio_table.heading('1',text='Accident ID')
        self.vio_table.heading('2',text='Vehicle No')
    
        self.vio_table['show']='headings'

        self.vio_table.column('1',width=100)
        self.vio_table.column('2',width=100)
        
        self.vio_table.pack(fill=BOTH, expand=1)
        self.vio_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()

    def open_next_page(self):
        self.root.destroy()  # Close the current window
        victim.main("user")  # Launch the next page by calling the main function in violation.py


    def add_data(self):
        if self.var_acc_id=="":
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                # Connect to the database
                conn = mysql.connector.connect(
                    host='localhost',
                    username='root',
                    password='Harshitha@27',
                    database='TrafficViolationManagement'
                )
                my_cursor = conn.cursor()

                # Insert the data into the Accidents table
                my_cursor.execute('''
                    INSERT INTO accidentvehicles (AccidentID,VehicleNo)
                    VALUES (%s, %s)
                    ''', (
                        self.var_acc_id.get(),
                        self.var_vehicle_no.get()
                ))

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo('Success', 'Accident-Vehicle record has been added')
            
            except mysql.connector.Error as err:
                messagebox.showerror('Error', f'Failed to add record: {err}')

    #fetch data
    def fetch_data(self):
        conn=mysql.connector.connect(host='localhost',username='root',password='Harshitha@27',database='TrafficViolationManagement')
        my_cursor=conn.cursor()
        my_cursor.execute('select * from accidentvehicles')
        data=my_cursor.fetchall()
        if len(data)!=0:
            self.vio_table.delete(*self.vio_table.get_children())
            for i in data:
                self.vio_table.insert('',END,values=i)
            conn.commit()
        conn.close()   
    
    #get cursor
    def get_cursor(self,event=""):
        cursor_row=self.vio_table.focus()
        content=self.vio_table.item(cursor_row)
        data=content['values']

        self.var_acc_id.set(data[0])
        self.var_vehicle_no.set(data[1])

    def update_data(self):
        if self.var_acc_id.get()=="":
            messagebox.showerror('Error','All the fields are required')
        else:
            try:
                update=messagebox.askyesno('Update','Are you sure you want to update')
                if update>0:
                    conn = mysql.connector.connect(
                    host='localhost',
                    username='root',
                    password='Harshitha@27',
                    database='TrafficViolationManagement'
                    )
                    my_cursor = conn.cursor()
                    my_cursor.execute('update accidentvehicles set VehicleNo=%s where AccidentID=%s',(     
                                                                                                    self.var_vehicle_no.get(),
                                                                                                    self.var_acc_id.get()
                                                                                                                         ))
                else:
                    if not update:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo('Success','Accident-Vehicle Information has been successfully updated')
            except Exception as es:
                messagebox.showerror('Error',f'Due to{str(es)}')

    #delete
    def delete_data(self):
        if self.var_acc_id.get()=="":
            messagebox.showerror('Error','All the fields are required')
        else:
            try:
                delete=messagebox.askyesno('Delete','Are you sure you want to delete')
                if delete>0:
                    conn = mysql.connector.connect(
                    host='localhost',
                    username='root',
                    password='Harshitha@27',
                    database='TrafficViolationManagement'
                    )
                    my_cursor = conn.cursor()
                    sql='delete from accidentvehicles where AccidentID=%s'
                    value=(self.var_acc_id.get(),)
                    my_cursor.execute(sql,value)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo('Success','Accident-Vehicle Information has been successfully Deleted')
            except Exception as es:
                messagebox.showerror('Error',f'Due to{str(es)}')
  
      


# if __name__ == "__main__":
#     root=Tk()
#     obj=Traffic(root)
#     root.mainloop()

def main(user_type):
    root = Tk()
    obj=Traffic(root)
    root.mainloop()

