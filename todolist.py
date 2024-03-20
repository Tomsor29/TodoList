import sqlite3
import pandas as pd
import tkinter
from tkinter import ttk

#Let's make the table and its origin.
conn = sqlite3.connect("list.db")


#Let's make something that makes transactions
cur = conn.cursor()

#Making the original sql table

cur.execute("CREATE TABLE IF NOT EXISTS list(Task TEXT, Requirements TEXT, Urgency TEXT, ExpirationDate TEXT)")

#Let's add some data to the table

taskinfo = ""
reqinfo = ""
urginfo = ""
dateinfo = ""


def updatetree():
    tree.delete(*tree.get_children())
    tablepd = pd.read_sql_query("SELECT * FROM list", conn)
    for index, row in tablepd.iterrows():
        tree.insert("", "end", text=index, values=list(row))


def butfuc():
    

    window2 = tkinter.Tk()
    window2["bg"] = "chartreuse2"
    window2.title("ADD NEW TASK")

    taskinfolabel = tkinter.Label(window2, text="Task: ")
    taskinfolabel.pack(padx=20, pady=5)
    
    taskinfo = tkinter.Entry(window2)
    taskinfo.pack(padx=20, pady=10)
    
    reqinfolabel = tkinter.Label(window2, text="Requirements: ")
    reqinfolabel.pack(padx=20, pady=12)
    reqinfo = tkinter.Entry(window2)
    reqinfo.pack(padx=20, pady=14)
    
    urginfolabel = tkinter.Label(window2, text="Urgency: ")
    urginfolabel.pack(padx=20, pady=16)
    urginfo = tkinter.Entry(window2)
    urginfo.pack(padx=20, pady=18)
    
    dateinfolabel = tkinter.Label(window2, text="Date: ")
    dateinfolabel.pack(padx=20, pady=20)
    dateinfo = tkinter.Entry(window2)
    dateinfo.pack(padx=20, pady=21)
    

    def finalinfo():
        
        task = taskinfo.get()
        req = reqinfo.get()
        urg = urginfo.get()
        date = dateinfo.get()
        data = [(task, req, urg, date)]
        cur.executemany("INSERT INTO list VALUES (?, ?, ?, ?)", data)
        conn.commit()
        window.withdraw()
        window2.destroy()
        updatetree()
        window.deiconify()
     

    destroybutton = tkinter.Button(window2, text = "FINISH", command= lambda: finalinfo())
    destroybutton.pack(padx=20, pady=23)

    window2.mainloop()






#Let's see the table's output
allquery = cur.execute("SELECT * FROM list")

print(allquery.fetchall())

#Now we're going with pandas

tablepd = pd.read_sql_query("SELECT * FROM list", conn)
print(tablepd)


#Now let's start with my lover tkinter




window = tkinter.Tk()
window["bg"] = "sky blue"

#The add button
Addbutton = tkinter.Button(window, text= "Add Task", command=butfuc, background="SpringGreen2")
Addbutton.pack(side=tkinter.LEFT)

#The delete button

def deleteall():
    queryD = ("DELETE FROM list")
    cur.execute(queryD)
    conn.commit()
    updatetree()
    window.withdraw()
    window.deiconify()
    

Deletebutton = tkinter.Button(window, text="Delete all", command=lambda: deleteall(),background="indian red")
Deletebutton.pack(side=tkinter.RIGHT)





#Let's make a treeview
tree = ttk.Treeview(window)

#Let's add the modification of entries for treeview


#Let's add to the tree its columns
tree["columns"] = list(tablepd.columns)
for colum in tree["columns"]:
    tree.heading(colum, text = colum)


#Let's add the rows

for index, row in tablepd.iterrows():
    tree.insert("", "end", text = index, values=list(row))


tree.pack(padx=20, pady=200, anchor="center")


window.mainloop()