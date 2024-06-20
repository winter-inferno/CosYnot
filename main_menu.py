'''
The main menu class
'''

import tkinter as tk
from tkinter import messagebox
import mysql.connector


class Main_menu(tk.Frame):
    def __init__(self, parent, controller,db):
        tk.Frame.__init__(self, parent)
        
        tk.Label(self,text="CosYnot!!",bg='white',fg='black',font="Arial 40 bold").place(x=275,y=10)

        border = tk.LabelFrame(self, text='Login', bg='ivory', bd = 10, font=("Arial", 20))
        border.pack(fill="both", expand="yes", padx = 170, pady=170)
        
        L1 = tk.Label(border, text="Username", font=("Arial Bold", 15), bg='ivory')
        L1.place(x=50, y=20)
        self.T1 = tk.Entry(border, width = 30, bd = 5)
        self.T1.place(x=180, y=20)

      
        def verify():
            mydb=mysql.connector.connect(host='localhost',user=db[0],password=db[1])
            mycursor=mydb.cursor()
            mycursor.execute('use CosYnot;')
            mycursor.execute('select * from PLAYERS;')
            for i in mycursor:
                if i[0]==self.T1.get():
                    controller.show_frame('Maingame',parent)
                    break
            else:
                messagebox.showinfo("Error","Entered username does not exist!")
            mydb.close()

        B1 = tk.Button(border, text="Start Game!", font=("Arial", 15), command=verify)
        B1.place(x=180, y=75)
                
        def register():
            window = tk.Toplevel(controller)
            window.resizable(0,0)
            window.configure(bg="deep sky blue")
            window.title("SIGNUP")
            window.grab_set()
            l1 = tk.Label(window, text="Username:", font=("Arial",15), bg="deep sky blue")
            l1.place(x=10, y=10)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x = 200, y=10)
            t1.focus()
            def check():
                if t1.get()!="":
                    mydb=mysql.connector.connect(host='localhost',user=db[0],password=db[1])
                    mycursor=mydb.cursor()
                    mycursor.execute('use CosYnot;')
                    mycursor.execute('select * from PLAYERS;')
                    for i in mycursor:
                        if i[0]==t1.get():
                            messagebox.showinfo("Error","The entered username already exists!")
                            break
                    else:
                        mycursor.execute("insert into PLAYERS(USERNAME,GAMES) VALUES('%s',0)" % (str(t1.get())))
                        mycursor.execute("insert into QNANALYSIS values('%s',0,0,0,0,0,0,0,0)" % (str(t1.get())))
                        mydb.commit()
                        messagebox.showinfo("Welcome","You are registered successfully!!")
                        window.destroy()
                    
                    mydb.close()
                    
                else:
                    messagebox.showinfo("Error","Please enter username!")
                    
            b1=tk.Button(window,text="Signup",font=("Arial",15),bg="#ffc22a",command=lambda:check())
            b1.place(x=170, y=150)
                        
            window.geometry("470x220")
            window.mainloop()
                        
        B2=tk.Button(self,text="Signup",bg="dark orange",font=("Arial",15),command=register).place(x=650,y=20)

        B3=tk.Button(self,text="EXIT",bg="dark orange",font=("Arial",15),command=controller.destroy).place(x=650,y=450)
     
        B4=tk.Button(self,text="Help",bg="dark orange",font=("Arial",15),command=lambda:controller.show_frame('Help',parent)).place(x=650,y=350)

        B5=tk.Button(self,text="Instructions",bg="dark orange",font=("Arial",15),command=lambda: controller.show_frame('Instructions',parent)).place(x=650,y=250)

        B6=tk.Button(self,text="Analysis",bg="dark orange",font=("Arial",15),command=lambda: controller.show_frame('Analysis',parent)).place(x=650,y=150)
        
