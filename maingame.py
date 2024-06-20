#importing  modules
from tkinter import  *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
import qn_gen
from random import randint,choice
from time import localtime
import mysql.connector
#initialising mainframe

class Maingame(ttk.Frame):
    def __init__(self, prnt, ctrl,database):
        global controller,parent,db,extraqns,totalqns,crctcount,qndict,stoptime,headfont,gamerun,sgdetails
        ttk.Frame.__init__(self, prnt)
        self.grid(column=0,row=0,sticky=(N,S,W,E))
        controller=ctrl
        parent=prnt
        db=database
        self.user=''
        gamerun=False
        extraqns=[]
        sgdetails=None
        
        totalqns={'Arithmetic2':50,'Arithmetic3':50,'LinEqns2':50,'Quadratic':50}
        crctcount={'Arithmetic2':50,'Arithmetic3':50,'LinEqns2':50,'Quadratic':50}

        

        qndict={'Q':'','A':'','P':''}
        stoptime=False

        headfont=font.Font(family='Arial',name='headerfont',size=15,weight='bold')
        
        
    #functions

    #generates the question and sets the ui according to the question
    def qn_set(self):
        global qntype
        ans1.set('')
        ans2.set('')
        dif=int(lvl.get())
        if dif==1:
            qntype='Arithmetic2'
            qn_gen.make_aob(dif,qndict)
        elif dif==2:
            rndmcount=randint(1,10)
            if rndmcount<5:
                qntype='Arithmetic2'
                qn_gen.make_aob(dif,qndict)
            elif rndmcount<9:
                qntype='Arithmetic3'
                qn_gen.make_aoboc(dif-1,qndict)
            else:
                qntype='LinEqns2'
                qn_gen.make_linear(dif-1,qndict)
        elif dif==3:
            #To avoid error with choice,if no extra questions are available
            if len(extraqns)==0:
                rndmcount=randint(1,11)
            else:
                rndmcount=randint(1,13)
            
            if rndmcount<4:
                qntype='Arithmetic2'
                qn_gen.make_aob(dif,qndict)
            elif rndmcount<8:
                qntype='Arithmetic3'
                qn_gen.make_aoboc(dif-1,qndict)
            elif rndmcount<10:
                qntype='LinEqns2'
                qn_gen.make_linear(dif-1,qndict)
            elif rndmcount<12:
                qntype='Quadratic'
                qn_gen.make_quad(dif-2,qndict)
            else:
                q=choice(extraqns)
                extraqns.remove(q)
                qntype=q[2]
                qndict['Q']=q[1]
                qndict['A']=q[3]
                qndict['P']=q[5]
                tleft.set(str(q[4])+'s left')
                
        else:
            #for giving priority to less correct answered qns
            rndmfactor=[int(100-crctcount[i]*100/totalqns[i]) for i in totalqns]
            for i in range(1,len(rndmfactor)):
                if rndmfactor[i]==0:
                    rndmfactor[i]=1
                rndmfactor[i]+=rndmfactor[i-1]

        
            if len(extraqns)==0:
                rndmcount=randint(1,rndmfactor[-1])
            else:
                rndmcount=randint(1,int(rndmfactor[-1]*(1.1))+1)

            if rndmcount<=rndmfactor[0]:
                qntype='Arithmetic2'
                qn_gen.make_aob(dif,qndict)
            elif rndmcount<=rndmfactor[1]:
                qntype='Arithmetic3'
                qn_gen.make_aoboc(dif-1,qndict)
            elif rndmcount<=rndmfactor[2]:
                qntype='LinEqns2'
                qn_gen.make_linear(dif-1,qndict)
            elif rndmcount<=rndmfactor[3]:
                qntype='Quadratic'
                qn_gen.make_quad(dif-2,qndict)
            else:
                q=choice(extraqns)
                extraqns.remove(q)
                qntype=q[2]
                qndict['Q']=q[1]
                qndict['A']=q[3]
                qndict['P']=q[5]
                tleft.set(str(q[4])+'s left')
        qno.set(int(qno.get())+1)
        qn.set(qndict['Q'])


        #setting time limit for generated qns and adding to total qns
        if qntype =='Quadratic':
            tleft.set('60s left')
            qndict['P']=25
        elif qntype =='LinEqns2':
            tleft.set('60s left')
            qndict['P']=20
        elif qntype =='Arithmetic3':
            tleft.set('60s left')
            qndict['P']=15
        elif qntype=='Arithmetic2':
            tleft.set('30s left')
            qndict['P']=10
            
        if qntype not in ('OneAns','TwoAns','XYAns'):
            totalqns[qntype]+=1
        #making changes to the interface according to qn type
        if qntype in ('Quadratic','TwoAns'):
            ans_box1.grid(column=2,row=5,sticky=W)
            ans_box2.grid(column=4,row=5,sticky=W)
            xlbl.grid_remove()
            ylbl.grid_remove()
        elif qntype in ('Arithmetic2','Arithmetic3','OneAns'):
            ans_box2.grid_remove()
            ans_box1.grid(column=3,row=5,sticky=W)
            xlbl.grid_remove()
            ylbl.grid_remove()
        elif qntype in ('LinEqns2','XYAns'):
            ans_box1.grid(column=2,row=5,sticky=W)
            ans_box2.grid(column=4,row=5,sticky=W)
            xlbl.grid(column=1,row=5,sticky=E)
            ylbl.grid(column=3,row=5,sticky=E)
        ans_box1.focus()
        
    def timer(self):
        if stoptime==False and gamerun==True:
            tcurrent=int(str(tleft.get())[0:-6])
            if tcurrent==0:
                messagebox.showinfo(message='Time\'s Up! Try to be quicker next time(lives decreased by 1)')
                if int(lives.get())==1:
                    messagebox.showinfo(message='Game Over...Final Score:'+str(score.get())+'.\nIn the help section,you can find ways to solve different types of questions.')
                    self.ret_back()
                    return
                lives.set(int(lives.get())-1)
                self.qn_set()
            else:
                tcurrent-=1
                tleft.set(str(tcurrent)+'s left')
        if gamerun==True:
            controller.after(1000,self.timer)

    def check_ans(*args):
        self=args[0]
        global stoptime
        stoptime=True
        points=0
        try:
            #generally points=integer of (root(level)*c+timeleft) different c for different question types
            if qntype in ('Arithmetic2','Arithmetic3','OneAns') and self.checkinrange(float(ans1.get()),qndict['A'],0.005):
                points=int((int(lvl.get()))**(0.5)*qndict['P']+int(str(tleft.get())[0:-6]))
            elif qntype in ('LinEqns2','XYAns') and self.checkinrange(float(ans1.get()),qndict['A'][0],0.005) and self.checkinrange(float(ans2.get()),qndict['A'][1],0.005):
                points=int((int(lvl.get()))**(0.5)*qndict['P']+int(str(tleft.get())[0:-6]))
            elif qntype in ('Quadratic','TwoAns') and (qndict['A']==(float(ans1.get()),float(ans2.get())) or qndict['A']==(float(ans2.get()),float(ans1.get()))):
                points=int((int(lvl.get()))**(0.5)*qndict['P']+int(str(tleft.get())[0:-6]))
        except:
            messagebox.showinfo(title='Error',message='Something is wrong with the submitted answer! Check and try again.')
            stoptime=False
            return
        if points!=0:
            if qntype not in ('OneAns','TwoAns','XYAns'):
                crctcount[qntype]+=1
            messagebox.showinfo(message='Correct Answer!(score increased by '+str(points)+' points)')
            score.set(int(score.get())+points)
            #to check for level up
            clvl=int(lvl.get())
            if int(score.get())>(clvl**3+clvl+1)*50:
                messagebox.showinfo(message='Level Up! Good work so far,get ready to face some tougher questions.')
                lvl.set(clvl+1)
                
                #To update extra qns
                mydb=mysql.connector.connect(host='localhost',user=db[0],password=db[1],database='CosYnot')
                mycursor=mydb.cursor()
                mycursor.execute('select * from extraqn where lvl ={};'.format(clvl+1))
                for i in extraqns:
                    if i[0]==clvl-1:
                        extraqns.remove(i)
                extraqns.extend(list(mycursor.fetchall()))
                mydb.close()
        else:
            messagebox.showinfo(message='Wrong Answer...Try to be more careful next time(lives decreased by 2)')
            if int(lives.get())<3:
                messagebox.showinfo(message='Game Over...Final Score:'+str(score.get())+'.\nIn the help section,you can find ways to solve different types of questions.')
                self.ret_back()
                return
            lives.set(int(lives.get())-2)

        self.qn_set()
        stoptime=False
        

    #extra
    def checkinrange(self,x,y,margin=0.005):
        if y-margin<=x<=y+margin:
            return True
        else:
            return False



    def start(self):#sets the ui for the game
        controller.title('CosYnot Quiz')
        
        global lvl,qno,qn,xlbl,ylbl,ans1,ans_box1,ans2,ans_box2,tleft,tlbl,lives,liveslbl,score
        #Labels(Text),Entryboxes

        ttk.Label(self,text='CosYnot!',font=headfont,anchor='center').grid(column=1,row=0,columnspan=4,sticky=(W,E))
        ttk.Label(self,text='Level:').grid(column=0,row=2,sticky=W)
        lvl=StringVar()
        ttk.Label(self,textvariable=lvl).grid(column=1,row=2,sticky=W)
        ttk.Label(self,text='Question:').grid(column=0,row=3,sticky=W)
        qno=StringVar()
        ttk.Label(self,textvariable=qno).grid(column=1,row=3,sticky=W)

        qn=StringVar()
        ttk.Label(self,textvariable=qn,width=30,anchor='center').grid(column=1,row=4,columnspan=4,sticky=(N,S,W,E))

        ttk.Label(self,text='Answer:').grid(column=0,row=5,sticky=W)

        xlbl=ttk.Label(self,text='x=')
        xlbl.grid(column=1,row=5,sticky=W)
        ans1=StringVar()
        ans_box1=ttk.Entry(self,width=7,textvariable=ans1)
        ans_box1.grid(column=2,row=5,sticky=W)

        ylbl=ttk.Label(self,text='y=')
        ylbl.grid(column=3,row=5,sticky=W)
        ans2=StringVar()
        ans_box2=ttk.Entry(self,width=7,textvariable=ans2)
        ans_box2.grid(column=4,row=5,sticky=W)

        ttk.Label(self,text='Timer:').grid(column=0,row=6,sticky=W)
        tleft=StringVar()
        tlbl=ttk.Label(self,textvariable=tleft)
        tlbl.grid(column=0,row=7,sticky=W)


        liveslbl=ttk.Label(self,text='Lives:')
        liveslbl.grid(column=6,row=1,sticky=W)
        lives=StringVar()
        ttk.Label(self,textvariable=lives).grid(column=7,row=1,sticky=W)
        ttk.Label(self,text='Score:').grid(column=6,row=2,sticky=W)
        score=StringVar()
        ttk.Label(self,textvariable=score).grid(column=7,row=2,sticky=W)

        #buttons
        
        ttk.Button(self,text='Submit',command=self.check_ans).grid(column=6,row=5,columnspan=2,sticky=W)
        controller.bind('<Return>',self.check_ans)#enter key=submit button
        
        ans_box1.focus()#for blinking cursor
        
        #this adds space b/w widgets
        for child in self.winfo_children():
            child.grid_configure(padx=5,pady=5)
        #set vriables
        lvl.set(1)
        qno.set(0)
        lives.set(6)
        score.set(0)
        global sgdetails
        if sgdetails:
            lvl.set(sgdetails[0])
            score.set(sgdetails[1])
            lives.set(sgdetails[2])
            qno.set(sgdetails[3])
            sgdetails=None
        self.qn_set()
        controller.after(1000,self.timer)
        global gamerun
        gamerun=True
        
    def end_inst(self):
        canvas.destroy()
        cont.destroy()
        self.start()


    def begin(self):
        global canvas,cont,img
        #checking if played before
        mydb=mysql.connector.connect(host='localhost',user=db[0],password=db[1],database='CosYnot')
        mycursor=mydb.cursor()
        mycursor.execute('select games from players where username="{}";'.format(self.user))
        x=mycursor.fetchone()
        if x[0]==0:
            inst_show=True#enable or disable instructions showing
        else:
            inst_show=False
        #getting player performance details
        mycursor.execute('select ar2faced,ar3faced,linfaced,quadfaced from qnanalysis where username="{}";'.format(self.user))
        x=mycursor.fetchone()
        totalqns.update({'Arithmetic2':x[0],'Arithmetic3':x[1],'LinEqns2':x[2],'Quadratic':x[3]})

        mycursor.execute('select ar2crct,ar3crct,lincrct,quadcrct from qnanalysis where username="{}";'.format(self.user))
        x=mycursor.fetchone()
        crctcount.update({'Arithmetic2':x[0],'Arithmetic3':x[1],'LinEqns2':x[2],'Quadratic':x[3]})
        
        #checking for saved games
        mycursor.execute('select sglvl,sgscore,sglives,sgqno from players where username="{}";'.format(self.user))
        x=mycursor.fetchone()
        if x!=(None,None,None,None):
            if messagebox.askyesno(message='A saved game has been found. Do you want to continue that game?(If no,then a new game will be started)',icon='question',title='Save Found'):
                global sgdetails
                sgdetails=x
                #To update extra qns
                mycursor.execute('select * from extraqn where lvl in ({},{});'.format(x[0]-1,x[0]))
                extraqns.extend(list(mycursor.fetchall()))
            mycursor.execute('update players set sglvl=NULL,sgscore=NULL,sglives=NULL,sgqno=NULL where username="{}";'.format(self.user))
            mydb.commit()
        mydb.close()

        def asksave():
            if messagebox.askyesno(message='Do you want to save this game to continue later?',icon='question',title='Save and Quit'):
                mydb=mysql.connector.connect(host='localhost',user=db[0],password=db[1],database='cosynot')
                mycursor=mydb.cursor()
                mycursor.execute('update players set sglvl={},sgscore={},sglives={},sgqno={} where username="{}";'.format(str(lvl.get()),str(score.get()),str(lives.get()),str(qno.get()),self.user))
                mycursor.execute('update qnanalysis set ar2faced={},ar2crct={},ar3faced={},ar3crct={},linfaced={},lincrct={},quadfaced={},quadcrct={} where username="{}";'.format(totalqns['Arithmetic2'],crctcount['Arithmetic2'],totalqns['Arithmetic3'],crctcount['Arithmetic3'],totalqns['LinEqns2'],crctcount['LinEqns2'],totalqns['Quadratic'],crctcount['Quadratic'],self.user))
                mydb.commit()
                mydb.close()
            controller.destroy()
            gamerun=False
            return
        controller.protocol('WM_DELETE_WINDOW',asksave)
        #Showing instructions at the beginning
        if inst_show==True:
            try:#loading png file works only from tcl 8.6
                controller.title('CosYnot :Instructions')
                img=PhotoImage(file='Instructions.png')
                canvas=Canvas(self,width=550,height=500)
                canvas.grid(column=0,row=0,columnspan=5,sticky=(N,S,W,E))
                canvas.create_image(280,250,image=img)
                cont=ttk.Button(self,text='Continue',command=self.end_inst)
                cont.grid(column=2,row=1,sticky=(W,E))
                cont.grid_configure(padx=5,pady=5)
            except:
                self.start()
        else:
            self.start()

    def ret_back(self):
        for child in self.winfo_children():
            child.destroy()
        global gamerun
        gamerun=False
        extraqns.clear()
        mydb=mysql.connector.connect(host='localhost',user=db[0],password=db[1],database='CosYnot')
        mycursor=mydb.cursor()
        mycursor.execute('update players set games=games+1 where username="{}";'.format(self.user))
        mycursor.execute('update qnanalysis set ar2faced={},ar2crct={},ar3faced={},ar3crct={},linfaced={},lincrct={},quadfaced={},quadcrct={} where username="{}";'.format(totalqns['Arithmetic2'],crctcount['Arithmetic2'],totalqns['Arithmetic3'],crctcount['Arithmetic3'],totalqns['LinEqns2'],crctcount['LinEqns2'],totalqns['Quadratic'],crctcount['Quadratic'],self.user))
        x=localtime()
        mycursor.execute('insert into scores values("{}","{}-{}-{}",{},{});'.format(self.user,x.tm_year,x.tm_mon,x.tm_mday,str(score.get()),str(qno.get())))
        mydb.commit()
        mydb.close()
        def dummy(*args):
            pass
        controller.bind('<Return>',dummy)
        controller.protocol('WM_DELETE_WINDOW',controller.destroy)
        controller.show_frame('Main_menu',parent)


