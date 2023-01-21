import datetime
import sqlite3
from tkcalendar import DateEntry
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk

#Connect the database to SQlite
connector = sqlite3.connect("Expense Tracker.db")
cursor = connector.cursor()

connector.execute(
    'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Description TEXT, Amount FLOAT)'
)
connector.commit()


# Backgrounds and Fonts
dataentery_frame_bg = 'Red'
hlb_btn_bg = 'IndianRed'
lbl_font = ('Georgia', 13)
entry_font = 'Times 13 bold'
btn_font = ('Gill Sans MT', 13)


# Initializing the GUI window. TK is our main window
root = Tk()
root.title('Expense Tracker')
root.geometry('1200x550')

Label(root, text = 'Expense Tracker', font=('Noto Sans CJK TC', 15, 'bold'), bg=hlb_btn_bg).pack(side=TOP, fill=X) 

# StringVar and DoubleVar variables
desc = StringVar()
amnt = DoubleVar()

#functions

#In the list_all_expenses() function, we will delete all the children of the table, 
# then get all the data from the database table using the connector’s SELECT command and then we will insert all of it to the table using the .insert() method of it.
def list_all_expenses():
    global connector, table

    table.delete(*table.get_children())

    all_data = connector.execute('SELECT * FROM ExpenseTracker')
    data = all_data.fetchall()

    for values in data:
        table.insert('', END, values= values)

#In the clear_fields() function, we will set all the StringVar variables to an empty string and the DataEntry variable to the current date.

def clear_fields():
    global desc, amnt, date, table

    today_date = datetime.datetime.now().date()
    
    desc.set('') ; amnt.set(0.0); date.set_date(today_date)
    table.selection_remove(*table.selection())


#In the add_another_expense() function, if any of the Entry fields is empty, we will display an error message box, 
# otherwise we will enter the INSERT command in the connector’s execute-commit methods combination, then clear all the entry fields and display the updated table.
def add_expense():
    global date, desc, amnt
    global connector

    if not date.get() or not desc.get() or not amnt.get():
        mb.showerror('Field empty. Please fill out all missing fields before adding expense.')
    else:
        connector.execute(
            'INSERT INTO ExpenseTracker (Date, Description, Amount) VALUES (?,?,?)',
            (date.get_date(), desc.get(), amnt.get())
        )
        
        connector.commit()

        clear_fields()
        list_all_expenses()


# In the remove_expense() function, we will get the values of the currently selected item in the table, 
# and ask the user if he really wants to delete it. If he/she wants to delete it, we will delete it using the DELETE command in the execute-commit method combo of the connector.   

def remove_expense():
    if not table.selection():
        mb.showerror('No record selected!', 'Please select a record to delete!')
        return
     
    current_selected_expense = table.item(table.focus())
    values_selected = current_selected_expense['values']
    surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')
     
    if surety:
        connector.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values_selected[0])
        connector.commit()
        list_all_expenses()



# Frames  
data_entry_frame = Frame(root, bg = dataentery_frame_bg)
data_entry_frame.place(x=0, y=30, relheight=0.95, relwidth=0.25)


tree_frame = Frame(root)
tree_frame.place(relx=0.25, rely=0.26, relwidth=0.75, relheight=0.74)

#Data entry Frame - Enter expenses, add/delete button. This is on the left side.
Label(data_entry_frame, text='Date (M/DD/YY) :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=50)
date = DateEntry(data_entry_frame, date=datetime.datetime.now().date(), font=entry_font)
date.place(x=160, y=50)

Label(data_entry_frame, text='Description\t     :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=100)
Entry(data_entry_frame, font=entry_font, width=31, text=desc).place(x=10, y=130)

Label(data_entry_frame, text='Amount\t             :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=180)
Entry(data_entry_frame, font=entry_font, width=14, text=amnt).place(x=160, y=180)

Button(data_entry_frame, text='Add expense', command=add_expense, font=btn_font, width=30,
      bg=hlb_btn_bg).place(x=10, y=350)

Button(data_entry_frame, text='Delete Expense', command=remove_expense, font=btn_font, width=30,
      bg=hlb_btn_bg).place(x=10, y=400)



# Treeview Frame - View and select expenses
table = ttk.Treeview(tree_frame, selectmode=BROWSE, columns=('ID', 'Date', 'Description', 'Amount'))
X_Scroller = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
Y_Scroller = Scrollbar(table, orient=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)
table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)
table.heading('ID', text= 'NO.', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Description', text='Description', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.column('#0', width=0, stretch=NO)
table.column('#1', width=50, stretch=NO) #ID
table.column('#2', width=115, stretch=NO)# Date column
table.column('#3', width=325, stretch=NO)  # Title column
table.column('#4', width=165, stretch=NO)  # Amount column

table.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_expenses()

root.update()
root.mainloop()



