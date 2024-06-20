#simple arithmetic
from random import randint
d={'Q':'','A':None}

#type aob where a and b nos and o is +,-,* or /; dif is the difficulty level
def make_aob(dif,dic=d):
    if dif==1:
        x,y=randint(1,20),randint(1,20)
        op=('+','-')[randint(0,1)]
    elif dif==2:
        op=('+','-','+','-','+','-','+','-','*','*','/')[randint(0,10)]
        if op in ('+','-'):
            x,y=randint(5,50),randint(5,50)
        elif op=='*':
            x,y=randint(2,10),randint(2,10)
        elif op=='/':
            x,y=randint(2,10),randint(2,10)
            x*=y#to prevent decimal answers
    elif dif==3:
        op=('+','-','+','-','+','-','*','*','/')[randint(0,8)]
        if op in ('+','-'):
            x,y=randint(10,100),randint(10,100)
        elif op=='*':
            x,y=randint(2,25),randint(2,25)
        elif op=='/':
            x,y=randint(2,25),randint(2,25)
            x*=y
    else:
        op=('+','-','*','/')[randint(0,3)]
        if op in ('+','-'):
            x,y=randint(10,dif*50),randint(10,dif*50)
        elif op=='*':
            x,y=randint(2,dif*10),randint(2,dif*10)
        elif op=='/':
            x,y=randint(2,dif*10),randint(2,dif*10)
            x*=y
    dic['Q']=str(x)+op+str(y)+' equals'
    dic['A']=eval(str(x)+op+str(y))

#type aoboc
def make_aoboc(dif,dic=d):
    if dif==1:
        x,y,z=(randint(1,20) for i in range(3))
        o1,o2=(('+','-')[randint(0,1)] for i in range(2))
        dic['Q']=str(x)+o1+str(y)+o2+str(z)+' equals'
    elif dif==2:
        o1,o2=(('+','-','+','-','+','-','+','-','*','*','/')[randint(0,10)] for i in range(2))
        if o1 in ('/','*') or o2 in ('/','*'):#different range of values if * or / comes
            x,y,z=(randint(1,10) for i in range(3))
            close=randint(1,2)#to randomly select which operation to be enclosed in brackets
            if close==1:
                dic['Q']='('+str(x)+o1+str(y)+')'+o2+str(z)+' equals'
            elif close==2:
                if o1=='/' and o2=='-' and y==z:#to prevent division by zero
                    y+=1
                dic['Q']=str(x)+o1+'('+str(y)+o2+str(z)+')'+' equals'
        else:
            x,y,z=(randint(5,50) for i in range(3))
            dic['Q']=str(x)+o1+str(y)+o2+str(z)+' equals'
    elif dif==3:
        o1,o2=(('+','-','+','-','+','-','*','*','/')[randint(0,8)] for i in range(2))
        if o1 in ('/','*') or o2 in ('/','*'):
            x,y,z=(randint(2,25) for i in range(3))
            close=randint(1,2)
            if close==1:
                dic['Q']='('+str(x)+o1+str(y)+')'+o2+str(z)+' equals'
            elif close==2:
                if o1=='/' and o2=='-' and y==z:
                    y+=1
                dic['Q']=str(x)+o1+'('+str(y)+o2+str(z)+')'+' equals'
        else:
            x,y,z=(randint(10,100) for i in range(3))
            dic['Q']=str(x)+o1+str(y)+o2+str(z)+' equals'   
    else:
        o1,o2=(('+','-','*','/')[randint(0,3)] for i in range(2))
        if o1 in ('/','*') or o2 in ('/','*'):
            x,y,z=(randint(2,dif*10) for i in range(3))
            close=randint(1,2)
            if close==1:
                dic['Q']='('+str(x)+o1+str(y)+')'+o2+str(z)+' equals'
            elif close==2:
                if o1=='/' and o2=='-' and y==z:
                    y+=1
                dic['Q']=str(x)+o1+'('+str(y)+o2+str(z)+')'+' equals'
        else:
            x,y,z=(randint(10,dif*50) for i in range(3))
            dic['Q']=str(x)+o1+str(y)+o2+str(z)+' equals'    
    dic['A']=eval(dic['Q'][:-7])


#Type2 - quadratic eqns

def make_quad(dif,dic=d):
    if dif==1:
        x,y=randint(1,10),randint(1,10)
        op1,op2='-'+str(abs(x+y)),'+'+str(abs(x*y))
    elif dif==2:
        x,y=randint(-10,10),randint(-10,10)
        if (x+y)>0:
            op1='-'+str(abs(x+y))
        elif (x+y)==0:
            op1=''
        else:
            op1='+'+str(abs(x+y))
        if (x*y)>0:
            op2='+'+str(abs(x*y))
        elif (x*y)==0:
            op2=''
        else:
            op2='-'+str(abs(x*y))
    elif dif==3:
        x,y=randint(-15,15),randint(-15,15)
        if (x+y)>0:
            op1='-'+str(abs(x+y))
        elif (x+y)==0:
            op1=''
        else:
            op1='+'+str(abs(x+y))
        if (x*y)>0:
            op2='+'+str(abs(x*y))
        elif (x*y)==0:
            op2=''
        else:
            op2='-'+str(abs(x*y))
    else:
        x,y=randint(-20,20),randint(-20,20)
        if (x+y)>0:
            op1='-'+str(abs(x+y))
        elif (x+y)==0:
            op1=''
        else:
            op1='+'+str(abs(x+y))
        if (x*y)>0:
            op2='+'+str(abs(x*y))
        elif (x*y)==0:
            op2=''
        else:
            op2='-'+str(abs(x*y))
    dic['Q']='Solve: '+'x^2'+op1+'x'+op2+'=0'
    dic['A']=(x,y)

#linear eqns
def make_linear(dif,dic=d):
    if dif>4:
        x=randint(1,2)
        if x==1:
            a1=randint(dif-2,dif*2)
            b1=randint(dif-2,dif*2)
            c1=randint(dif-2,dif*2)
            a2=randint(dif-2,dif*2)
            while True:
                b2=randint(dif-2,dif*2)
                if a2/b2!=a1/b1:
                    break
            c2=randint(dif-2,dif*2)
            
            eq1="{0}x+{1}y+{2}=0".format(a1,b1,c1)
            eq2="{0}x+{1}y+{2}=0".format(a2,b2,c2)

            x=((b1*c2)-(b2*c1))/((a1*b2)-(a2*b1))
            y=((c1*a2)-(c2*a1))/((a1*b2)-(a2*b1))

            dic['Q']='Solve: {}, {}'.format(eq1,eq2)
            dic['A']=(x,y)
            return
    if dif==1:
        xyrange=(1,5)
        abrange=(1,5)
    elif dif==2:
        xyrange=(2,10)
        abrange=(2,10)
    elif dif==3:
        xyrange=(2,10)
        abrange=(4,15)
    elif dif==4:
        xyrange=(4,13)
        abrange=(6,20)
    else:
        xyrange=(dif*2-4,dif*3)
        abrange=(dif*2+2,dif*3+8)
    x=randint(xyrange[0],xyrange[1])
    y=randint(xyrange[0],xyrange[1])
    a1=randint(abrange[0],abrange[1])
    b1=randint(abrange[0],abrange[1])
    a2=randint(abrange[0],abrange[1])
    while True:
        b2=randint(abrange[0],abrange[1])
        if a1/b1!=a2/b2:
            break
    c1=b1*y-a1*x
    c2=b2*y-a2*x
    dic['Q']='Solve: {}x{}y{}=0, {}x{}y{}=0'.format(a1,sign_give(-b1),sign_give(c1),a2,sign_give(-b2),sign_give(c2))
    dic['A']=(x,y)
def sign_give(n):
    if n>0:
        return '+'+str(abs(n))
    elif n<0:
        return '-'+str(abs(n))
    else:
        return '+0'
