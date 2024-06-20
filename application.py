'''
Main application program,along with other areas
'''
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from main_menu import Main_menu
from maingame import Maingame
from analysis import Analysis
import os
from pickle import load as pickle_load

dbdetails=(None,None)
current_frame=None

#Gets the database password and username, creates the database and tables if it does not exist
class dbinit(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        frame=ttk.Frame(self,padding='3 3 12 12')
        frame.grid(column=0,row=0,sticky=(tk.N,tk.S,tk.E,tk.W))
        self.resizable(False,False)
        self.title('CosYnot: Database')
        def checkdb(*args):
            try:
                mydb=mysql.connector.connect(host='localhost',user=str(user.get()),password=str(password.get()))
                mycursor=mydb.cursor()
                mycursor.execute('show databases;')
                x=mycursor.fetchall()
                if ('cosynot',) not in x:
                    mycursor.execute('create database CosYnot;')
                    mycursor.execute('use CosYnot;')
                    mycursor.execute('create table PLAYERS(USERNAME varchar(30),GAMES int,SGLVL int,SGSCORE int,SGLIVES int,SGQNO int);')
                    mycursor.execute('create table SCORES(USERNAME varchar(30),DATE date,SCORE int,QNO int);')
                    mycursor.execute('create table QNANALYSIS(USERNAME varchar(30),AR2FACED int,AR2CRCT int,AR3FACED int,AR3CRCT int,QUADFACED int,QUADCRCT int,LINFACED int,LINCRCT int);')
                    mycursor.execute('create table EXTRAQN(LVL int,QN varchar(250),TYPE varchar(10),ANS float,TIME int,BASEPOINTS int);')
                if os.path.exists('qndata.dat'):
                    with open('qndata.dat','rb') as f:
                        mycursor.execute('use CosYnot;')
                        d=pickle_load(f)
                        for i in d:
                            mycursor.execute('insert into EXTRAQN values({},"{}","{}",{},{},{});'.format(i[0],i[1],i[2],i[3],i[4],i[5]))
                    mydb.commit()
                    os.remove('qndata.dat')
                mydb.close()
            except :
                messagebox.showinfo(title='Error',message='Please enter correct user name and password!')
                return
            self.destroy()
            global dbdetails
            dbdetails=(str(user.get()),str(password.get()))
            app = Application()
            app.resizable(False,False)
            app.mainloop()
            
                
            
        ttk.Label(frame,text='Enter MySQL Database details').grid(column=2,row=1,columnspan=2,sticky=(tk.E,tk.W))
        ttk.Label(frame,text='User:').grid(column=1,row=2,sticky=tk.W)
        ttk.Label(frame,text='Password:').grid(column=1,row=3,sticky=tk.W)

        user=tk.StringVar()
        userbox=ttk.Entry(frame,textvariable=user)
        userbox.grid(column=2,row=2,sticky=tk.E)
        password=tk.StringVar()
        passbox=ttk.Entry(frame,textvariable=password)
        passbox.grid(column=2,row=3,sticky=tk.E)

        ttk.Button(frame,text='Proceed',command=checkdb).grid(column=3,row=4,sticky=(tk.N,tk.S,tk.W,tk.E))
        self.bind('<Return>',checkdb)
        
        for child in frame.winfo_children():
            child.grid_configure(padx=5,pady=5)


        
        
#Frame for instructions      
class Instructions(tk.Frame):
    def __init__(self, parent, controller,db):
        tk.Frame.__init__(self, parent)
        self.img=tk.PhotoImage(file='Instructions.png')
        canvas=tk.Canvas(self,width=550,height=500)
        canvas.grid(column=0,row=0,columnspan=5,sticky='nsew')
        canvas.create_image(280,250,image=self.img)
        cont=ttk.Button(self,text='Continue',command=lambda:controller.show_frame('Main_menu',parent))
        cont.grid(column=2,row=1,sticky='we')
        cont.grid_configure(padx=5,pady=5)
            

#Frame for help
class Help(tk.Frame):
    def __init__(self, parent, controller,db):
        tk.Frame.__init__(self, parent)
        self.configure(bg='Tomato')
        tk.Label(self, text="Help", font=("Arial Bold", 25),width=6,anchor='w',bg='Tomato').grid(row=0,column=1,columnspan=2,sticky='w')
        
        ttk.Button(self, text="Quadratic Equations",command=self.help_quad).grid(row=1,column=0,sticky='w')
        ttk.Button(self, text="Linear Equations in Two Variables",command=self.help_linear).grid(row=2,column=0,columnspan=2,sticky='w')
        
        tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame('Main_menu',parent)).grid(row=4,column=3,sticky='e')
        
        for child in self.winfo_children():
            child.grid_configure(padx=10,pady=10)
    def help_quad(*args):
        self=args[0]
        window=tk.Toplevel(self)
        window.title('Help:Quadratic Equations')
        window.grab_set()
        canvas=tk.Canvas(window,width=895,height=507)
        canvas.grid(column=0,row=0,sticky='nsew')
        self.img=tk.PhotoImage(file='Quad_Eqns_Help.png')
        canvas.create_image(447,253,image=self.img)
    def help_linear(*args):
        self=args[0]
        window=tk.Toplevel(self)
        window.title('Help:Linear Equations')
        window.grab_set()
        canvas=tk.Canvas(window,width=970,height=550)
        canvas.grid(column=0,row=0,sticky='nsew')
        self.img=tk.PhotoImage(file='Linear_Eqns_Help.png')
        canvas.create_image(485,275,image=self.img)

#Main application window,other parts are the frames of this window
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #creating a window
        window = tk.Frame(self)
        window.pack()
        
        
        self.frames = {}
        for F in ('Main_menu','Maingame','Analysis','Instructions','Help'):
            frame = eval(F+'(window,self,dbdetails)')
            self.frames[F] = frame
            frame.grid(row=0,column=0,sticky='nsew')
            frame.grid_remove()
            
        self.show_frame('Main_menu',window)
        
    def show_frame(self, page,parent=None):
        if page=='Analysis' and self.frames['Main_menu'].T1.get()=='':
            messagebox.showinfo(title='Error',message='Please enter valid user name in the entry box, then try again.')
        else:
            global current_frame
            frame = self.frames[page]
            if current_frame:
                current_frame.grid_remove()
            frame.grid(row=0,column=0,sticky='nsew')
            current_frame=frame
            if page=='Main_menu':
                self.title('CosYnot: Main Menu')
                parent.grid_rowconfigure(0, minsize = 500)
                parent.grid_columnconfigure(0, minsize = 800)
            elif page=='Maingame':
                self.title('CosYnot: Game')
                frame.user=self.frames['Main_menu'].T1.get()
                parent.grid_rowconfigure(0, minsize = 0)
                parent.grid_columnconfigure(0, minsize = 0)
                frame.begin()
            elif page=='Instructions':
                self.title('CosYnot: Instructions')
                parent.grid_rowconfigure(0, minsize = 0)
                parent.grid_columnconfigure(0, minsize = 0)
            elif page=='Help':
                self.title('CosYnot: Help')
                parent.grid_rowconfigure(0, minsize = 0)
                parent.grid_columnconfigure(0, minsize = 0)
            elif page=='Analysis':
                self.title('CosYnot: Analysis')
                parent.grid_rowconfigure(0, minsize = 0)
                parent.grid_columnconfigure(0, minsize = 0)
                frame.show(self.frames['Main_menu'].T1.get())
                

            
initialize=dbinit()
