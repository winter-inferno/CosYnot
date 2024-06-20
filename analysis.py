from tkinter import *
from  tkinter import ttk
import mysql.connector

class Analysis(Frame):
    def __init__(self, parent, controller,database):
        global db,crcttable,hightable,tgames,cuser
        Frame.__init__(self, parent)
        self.configure()
        db=database

        #Correct percent analysis table
        crcttable=ttk.Treeview(self,height=1)

        crcttable['columns'] = ('A1','A2','A3','A4')

        crcttable.column("#0", width=0,  stretch=NO)
        crcttable.column("A1",anchor=CENTER, width=160)
        crcttable.column("A2",anchor=CENTER,width=160)
        crcttable.column("A3",anchor=CENTER,width=160)
        crcttable.column("A4",anchor=CENTER,width=160)

        crcttable.heading("#0",text="",anchor=CENTER)
        crcttable.heading("A1",text="Arithmetic with 2 values",anchor=CENTER)
        crcttable.heading("A2",text="Arithmetic with 3 values",anchor=CENTER)
        crcttable.heading("A3",text="Quadratic Equations",anchor=CENTER)
        crcttable.heading("A4",text="Linear Equations",anchor=CENTER)

        crcttable.grid(row=2,column=2,columnspan=2)
        
        #High scores
        hightable = ttk.Treeview(self,height=5)

        hightable['columns'] = ('Username', 'Score', 'Date')

        hightable.column("#0", width=0,  stretch=NO)
        hightable.column("Username",anchor=CENTER, width=80)
        hightable.column("Score",anchor=CENTER,width=80)
        hightable.column("Date",anchor=CENTER,width=80)

        hightable.heading("#0",text="",anchor=CENTER)
        hightable.heading("Username",text="Username",anchor=CENTER)
        hightable.heading("Score",text="Score",anchor=CENTER)
        hightable.heading("Date",text="Date",anchor=CENTER)

        hightable.grid(row=2,column=0,columnspan=2)
        #Other widgets
        ttk.Label(self,text='Game Analysis',font=('Arial',15),anchor=CENTER).grid(column=0,row=0,columnspan=4,sticky=(W,E))

        ttk.Label(self,text='High Scores',font=('Arial',12),anchor=CENTER).grid(column=0,row=1,columnspan=2,sticky=(W,E))
        ttk.Label(self,text='Answer Precision',font=('Arial',12),anchor=CENTER).grid(column=2,row=1,columnspan=2,sticky=(W,E))

        ttk.Label(self,text='Current Player:').grid(column=2,row=3,sticky=W)
        cuser=StringVar()
        ttk.Label(self,textvar=cuser).grid(column=3,row=3,sticky=W)

        ttk.Label(self,text='Total Number of Games Played:').grid(column=2,columnspan=2,row=4,sticky=W)
        tgames=StringVar()
        ttk.Label(self,textvar=tgames).grid(column=3,row=4,sticky=W)
        
        ttk.Button(self, text="Home", command=lambda: controller.show_frame('Main_menu',parent)).grid(row=5,column=3,sticky=E)

        for child in self.winfo_children():
            child.grid_configure(padx=5,pady=5)

    def show(self,user):
        global db,crcttable,hightable,tgames,cuser,prec,scores
        if cuser.get()!='':
            crcttable.delete(1)
            for i in range(5):
                hightable.delete(i)
        cuser.set(user)

        mydb=mysql.connector.connect(host="localhost",user=db[0],password=db[1],database="cosynot")
        mycursor=mydb.cursor()
        mycursor.execute("select username,score,date from scores order by score desc;")
        scores=mycursor.fetchall()
        mycursor.execute('select ar2crct*100/ar2faced,ar3crct*100/ar3faced,quadcrct*100/quadfaced,lincrct*100/linfaced from qnanalysis where username="{}";'.format(user))
        prec=mycursor.fetchone()
        mycursor.execute('select games from players where username="{}";'.format(user))
        tgames.set(mycursor.fetchone()[0])
        mydb.close()
        
        prec=list(prec)
        for i in range(4):
            if prec[i]!=None:
                prec[i]=str(round(prec[i],2))+'%'
            
        crcttable.insert(parent='',index='end',iid=1,text='',values=prec)
        
        if len(scores)<5:
            for i in range(0,5-len(scores)):
                scores.append(("-","-","-"))
        for i in range(5):
            hightable.insert(parent='',index='end',iid=i,text='',values=scores[i])
