from tkinter import *
import tkinter.messagebox
import sqlite3
#-----------------------------------------------------------------------------------------------------------------------------------

conn=sqlite3.connect('test.db')
print("CONNECTED!!!")


conn.execute("CREATE TABLE IF NOT EXISTS ENTRIES \
     (NAME  TEXT  PRIMARY KEY NOT NULL, \
     CONTACT INT NOT NULL, \
     SOURCE TEXT NOT NULL, \
     DESTINATION TEXT NOT NULL, \
     NOFDAYS INT);")
print("Table created successfully")
conn.execute("DELETE FROM ENTRIES")



avail_car = {'CAR':6,'7-SEATER':5,'SUV':4,'9-SEATER':3,'MINI BUS':2,'BUS':2}

def create_table():
    register_query=str("CREATE TABLE IF NOT EXISTS register(register_username VARCHAR,"+
                     "register_password VARCHAR,"+
                     "register_rpassword VARCHAR,"+
                     "register_email VARCHAR PRIMARY KEY,"+
                     "register_mobile INTEGER)")
                     
    conn.execute(register_query)
    print("created client table")
#----------------------------------------------------------------------------------------------------------------------------------

class project:

    def insertdetails(self):
            username=self.e_rusername.get()
            email=self.e_email.get()
            mobile=self.e_mobile.get()
            password=self.e_rpassword.get()
            rpassword=self.e_rpass.get()
            if(username=='' or email==''or mobile==''or password==''or rpassword==''):
                tkinter.messagebox.showinfo("Error", "Please Enter all the details")
            else:
                
                    try:
                        query=str("INSERT INTO register(register_username, register_password, register_rpassword, register_email, register_mobile) VALUES(?,?,?,?,?)")
                        conn.execute(query,(username,password,rpassword,email,mobile,))
                        conn.commit()
                    except sqlite3.IntegrityError:
                        tkinter.messagebox.showinfo("Error", "The entered EMAIL ID is already present")
                    else:
                        if(rpassword==password):
                            print("registered")
                            tkinter.messagebox.showinfo("SUCCESSFUL", "REGISTRATION DONE SUCCESSFULLY")
                            self.login()
                        else:
                            tkinter.messagebox.showinfo("Error", "The re-entered password doesnt match previous password")
    def login(self):
        self.frame.destroy()
        self.frame = Frame(root, height=500, width=700,bd=8,relief="raise",bg="black")
        self.frame.pack()
            #labels
        lbl = Label(self.frame,font=('arial',16,'bold'),text="Enter your EMAIL ",bd=16,anchor='w',fg='red',bg='black')
        lbl.grid(row=0, column=0, padx=5, pady=5)
        lb2 = Label(self.frame,font=('arial',16,'bold'),text="Enter password",bd=16,bg="black",anchor='w',fg='red')
        lb2.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        #entry fields
        self.e_username = Entry(self.frame,font=('arial',16),fg="white",bg='black',bd=5,insertwidth=10,justify='left')
        self.e_username.grid(row=0, column=1, padx=5, pady=5)
        self.e_password = Entry(self.frame,font=('arial',16),show="*",fg="white",bd=5,insertwidth=10,justify='left',bg='black')
        self.e_password.grid(row=1, column=1, padx=5, pady=5)
            #button
        self.b = Button(self.frame,font=('arial',16,'bold'),text="LOGIN",bg="black",command=self.checkLogin,fg='red')
        self.b.grid(row=2, column=0, columnspan=2)
        self.frame.grid_propagate(0)    

    def checkLogin(self):
            if(self.e_username.get()=="" or self.e_password.get()==""):
                    tkinter.messagebox.showinfo("Error", "PLEASE FILL ALL THE CREDENTIALS")
            r=conn.execute("SELECT * FROM register WHERE register_email=? AND register_password=?",(self.e_username.get(),self.e_password.get(),)) 
            for i in r:
                if(self.e_username.get()==i[3] or self.e_password.get()==i[1]):
                    self.booking_page()
                else:
                    tkinter.messagebox.showinfo("Wrong Credentials!" , "INVALID EMAIL OR PASSWORD")



    def book_car(self):
        if(self.txtCustomerName=='' or self.txtNoOfDaysRented=='' or self.txtSource=='' or self.txtDestination=='' or self.txtContactNo==''):
                tkinter.messagebox.showinfo("Error","PLEASE FILL ALL DETAILS BEFORE BOOKING")
        if(self.var.get()==''):
                tkinter.messagebox.showinfo("Error","SELECT A VEHICLE BEFORE BOOKING")
        else:
            print(str(self.var.get()))
            if(avail_car[self.var.get()]!=0):
                self.RentalCost()
                avail_car[self.var.get()]=int(avail_car[self.var.get()])-1
                print(avail_car[self.var.get()])
                tkinter.messagebox.showinfo("SUCCESSFUL", "BO0KING DONE")
            else:
                tkinter.messagebox.showinfo("VEHICLE NOT AVAILABLE", "TRY BOOKING LATER SELECTED VEHICLE IS NOT AVAILABLE")


                
    '''def qexit(self):
        self.root.destroy()
        qexit=tkinter.messagebox.askyesno("LOGOUT","Do you want to log out?")
        if qexit>0:
            self.login()
       '''
    def qexit(self):
        qexit=tkinter.messagebox.askyesno("Exit the system","Do you want to quit?")
        if qexit>0:
            root.destroy()
        return 

    def RentalCost(self):
        noOfDays=int(self.txtNoOfDaysRented.get())

        if(self.var.get()=="CAR"):
           rent=noOfDays*500
        elif(self.var.get()=="7-SEATER"):
           rent=noOfDays*650
        elif(self.var.get()=="SUV"):
           rent=noOfDays*700
        elif(self.var.get()=="9-SEATER"):
           rent=noOfDays*800
        elif(self.var.get()=="MINI BUS"):
           rent=noOfDays*1000
        else:
            rent=noOfDays*1500

        self.txtTotal.delete(0,tkinter.END)
        self.txtTotal.insert(0,rent)
        return
    
    


    def insert(self):
        if(self.txtCustomerName.get()=='' or self.txtContactNo.get()==0 or self.txtSource.get()=='' or self.txtDestination.get()=='' or self.txtNoOfDaysRented.get()==0):
            tkinter.messagebox.showinfo("Error", "Please Enter all the details")
        else:
            try:
                conn.execute("INSERT INTO ENTRIES (NAME,CONTACT,SOURCE,DESTINATION,NOFDAYS) \
                  VALUES (?,?,?,?,?)",(self.txtCustomerName.get(),self.txtContactNo.get(),self.txtSource.get(),self.txtDestination.get(),self.txtNoOfDaysRented.get(),))

                conn.commit()
            except sqlite3.IntegrityError:
                tkinter.messagebox.showinfo("Error", "The entered ID is already present")
            else:
                tkinter.messagebox.showinfo("SUBMIT", "SUBMITED!!")
                self.txtCustomerName.delete(0,END)
                self.txtContactNo.delete(0,END)
                self.txtSource.delete(0,END)
                self.txtDestination.delete(0,END)
                self.txtNoOfDaysRented.delete(0,END)
                self.txtTotal.delete(0,END)


        
    def display(self):
        self.book_car()
        self.insert()
        print("Details:")
        
        winddisplay=Tk()
        winddisplay.title("DISPLAY")
        winddisplay.geometry('1300x700+100+50')
        label1=Label(winddisplay)
        label1.config(text="NAME:",width=20,bg='ivory1',fg='royalblue')
        label1.place(x=100,y=100)
        
        label2=Label(winddisplay)
        label2.config(text="CONTACT NO.",width=20,bg='ivory1',fg='royalblue')
        label2.place(x=250,y=100)

        label3=Label(winddisplay)
        label3.config(text="SOURCE",width=20,bg='ivory1',fg='royalblue')
        label3.place(x=380,y=100)

        label4=Label(winddisplay)
        label4.config(text="DESTINATION",width=20,bg='ivory1',fg='royalblue')
        label4.place(x=480,y=100)

        label5=Label(winddisplay)
        label5.config(text="NO. OF DAYS",width=20,bg='ivory1',fg='royalblue')
        label5.place(x=600,y=100)

        '''label6=Label(winddisplay)
        label6.config(text="VEHICLE RENTED",width=20,bg='ivory1',fg='royalblue')
        label6.place(x=700,y=100)
        '''
        
        cursor=conn.execute("SELECT NAME,CONTACT,SOURCE,DESTINATION,NOFDAYS from ENTRIES")
        data=cursor.fetchall()
        #print("NAME\t    CONTACT\t  SOURCE\t  DESTINATION\t  \tNOFDAYS")
        
        ax=125
        for row in data:
            text1=Label(winddisplay)
            text1.config(text=str(row[0]),width=20,bg='lavenderblush1',fg='hotpink',padx=5)
            text1.place(x=100,y=ax)
            
            text2=Label(winddisplay)
            text2.config(text=row[1],width=20,bg='lavenderblush1',fg='hotpink',padx=5)
            text2.place(x=250,y=ax)
            
            text3=Label(winddisplay)
            text3.config(text=str(row[2]),width=20,bg='lavenderblush1',fg='hotpink',padx=5)
            text3.place(x=380,y=ax)
            
            text4=Label(winddisplay)
            text4.config(text=str(row[3]),width=20,bg='lavenderblush1',fg='hotpink',padx=5)
            text4.place(x=480,y=ax)
            
            text5=Label(winddisplay)
            text5.config(text=row[4],width=20,bg='lavenderblush1',fg='hotpink',padx=5)
            text5.place(x=600,y=ax)

            ax=ax+25
            
         #  print("%s\t %d\t\t %s\t %s\t\t %d\t"%(row[0],row[1],row[2],row[3],row[4]))
        
        tkinter.messagebox.showinfo("BOOKING WINDOW", "BOOKED!!")
        


    def register(self):
        self.frame.destroy()
        self.frame = Frame(root, height=500, width=700,bd=8,relief="raise",bg="black")
        self.frame.pack()
            #labels
        lbl = Label(self.frame,font=('arial',16,'bold'),text="Enter username",bd=16,bg="black",anchor='w',fg='red')
        lbl.grid(row=0, column=0, padx=5, pady=5)
        lb2 = Label(self.frame,font=('arial',16,'bold'),text="Enter password",bd=16,bg="black",anchor='w',fg='red')
        lb2.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        lb3 = Label(self.frame,font=('arial',16,'bold'), text="Re-Enter password",bd=16,bg="black",anchor='w',fg='red')
        lb3.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        lbl4= Label(self.frame,font=('arial',16,'bold'),text='Email',bd=16,bg="black",anchor='w',fg='red')
        lbl4.grid(row=3,column=0)
        lbl5= Label(self.frame,font=('arial',16,'bold'),text='Mobile',bd=16,bg="black",anchor='w',fg='red')
        lbl5.grid(row=4,column=0)
            #entry fields
        self.e_rusername= Entry(self.frame,font=('arial',16),fg="white",bd=5,insertwidth=10,bg="black",justify='left')
        self.e_rusername.grid(row=0, column=1, padx=5, pady=5)
        self.e_rpassword = Entry(self.frame,font=('arial',16),show="*",fg="white",bd=5,insertwidth=10,bg="black",justify='left')        
        self.e_rpassword.grid(row=1, column=1, padx=5, pady=5)
        self.e_rpass= Entry(self.frame,font=('arial',16),show="*",fg="white",bd=5,insertwidth=10,bg="black",justify='left')
        self.e_rpass.grid(row=2, column=1, padx=5, pady=5)
        self.e_email=Entry(self.frame,font=('arial',16),fg="white",bd=5,insertwidth=10,bg="black",justify='left')
        self.e_email.grid(row=3,column=1)
        self.e_mobile=Entry(self.frame,font=('arial',16),fg="white",bd=5,insertwidth=10,bg="black",justify='left')
        self.e_mobile.grid(row=4,column=1)
            #register button
        b = Button(self.frame,font=('arial',16,'bold'),text="REGISTER",bg="black",fg='red',command=self.insertdetails)
        b.grid(row=5,column=0,columnspan=2)
        self.frame.grid_propagate(0)

    def yReset(self):
        self.var1.set(0)
        self.var2.set(0)
        self.var3.set(0)


        self.txtCustomerName.delete(0,tkinter.END)
        self.txtNoOfDaysRented.delete(0,tkinter.END)
        self.txtSource.delete(0,tkinter.END)
        self.txtDestination.delete(0,tkinter.END)
        self.txtTotal.delete(0,tkinter.END)
        self.txtContactNo.delete(0,tkinter.END)
        self.txtSuggestion.delete(0,tkinter.END)


    def booking_page(self):
        self.frame.destroy()
        
        self.leftf = Frame(root,width=800,height=650,bd=8,relief="raise",bg='cyan')
        self.leftf.pack(side=LEFT)

        self.leftf1 = Frame(self.leftf,width=1000,height=325,bd=8,relief="raise",bg='black')
        self.leftf1.pack(side=TOP),
        self.leftf2= Frame(self.leftf,width=1000,height=225,bd=8,relief="raise",bg='black')
        self.leftf2.pack(side=TOP)
        self.leftf3= Frame(self.leftf,width=1000,height=100,bd=8,relief="raise",bg='black')
        self.leftf3.pack(side=TOP)


        lblCustomerName=Label(self.leftf1,font=('arial',10,'bold'),text='CUSTOMER NAME',bd=8,fg='red',bg='black')
        lblCustomerName.grid(row=1,column=0)
        self.txtCustomerName=Entry(self.leftf1,font=('arial',10,'bold'),bd=8,width=31,justify='left')
        self.txtCustomerName.grid(row=1,column=1)

        lblNoOfDaysRented=Label(self.leftf2,font=('arial',10,'bold'),text='NO. OF DAYS RENTED',bd=8,fg='red',bg='black')
        lblNoOfDaysRented.grid(row=1,column=2)
        self.txtNoOfDaysRented=Entry(self.leftf2,font=('arial',10,'bold'),bd=8,width=31,justify='left')
        self.txtNoOfDaysRented.grid(row=1,column=3)

        lblSource=Label(self.leftf2,font=('arial',10,'bold'),text='SOURCE',bd=8,fg='red',bg='black')
        lblSource.grid(row=1,column=0)
        self.txtSource=Entry(self.leftf2,font=('arial',10,'bold'),bd=8,width=31,justify='left')
        self.txtSource.grid(row=1,column=1)

        lblDestination=Label(self.leftf2,font=('arial',10,'bold'),text='DESTINATION',bd=8,fg='red',bg='black')
        lblDestination.grid(row=2,column=0)
        self.txtDestination=Entry(self.leftf2,font=('arial',10,'bold'),bd=8,width=31,justify='left')
        self.txtDestination.grid(row=2,column=1)

        lblContactNo=Label(self.leftf1,font=('arial',10,'bold'),text='CONTACT NO.',bd=8,fg='red',bg='black')
        lblContactNo.grid(row=2,column=0)
        self.txtContactNo=Entry(self.leftf1,font=('arial',10,'bold'),bd=8,width=31,justify='left')
        self.txtContactNo.grid(row=2,column=1)

        lblTotal=Label(self.leftf2,font=('arial',10,'bold'),text='TOTAL',bd=8,fg='red',bg='black')
        lblTotal.grid(row=2,column=2,sticky=W)
        self.txtTotal=Entry(self.leftf2,font=('arial',10,'bold'),bd=8,width=31,justify='left')
        self.txtTotal.grid(row=2,column=3)

        self.var=StringVar(root)
        option=OptionMenu(self.leftf1,self.var,'CAR','7-SEATER','BUS','SUV','MINI BUS','9-SEATER')
        #self.var.set('CAR')
        option.grid(row=3,column=1)
        lbltype=Label(self.leftf1,font=('arial',10,'bold'),text='SELECT TYPE OF VEHICLE',bd=4,fg='red',bg='black')
        lbltype.grid(row=3,column=0)

        w=Message(self.leftf1,text="WELCOME TO VEHICLE RENTAL SYSTEM!!! ",anchor='center',font=('calibri',20,'bold'),width=1000,fg='red',bg='black')
        w.grid(row=0)


        btnTotal=Button(self.leftf3,text='TOTAL',padx=4,pady=4,bd=16,fg='red',bg='black',
                font=('arial',12,'bold'),width=14,height=1,command=self.RentalCost).grid(row=0,column=1)

        btnBook=Button(self.leftf3,text='BOOK',padx=4,pady=4,bd=16,fg='red',bg='black',
            font=('arial',12,'bold'),width=14,height=1,command=self.display).grid(row=0,column=2)
        '''btnSubmit=Button(self.leftf3,text='SUBMIT',padx=4,pady=4,bd=16,fg='red',bg='black',
            font=('arial',12,'bold'),width=14,height=1,command=self.insert).grid(row=0,column=2)'''
        btnExit=Button(self.leftf3,text='LOG OUT',padx=4,pady=4,bd=16,fg='red',bg='black',
            font=('arial',12,'bold'),width=14,height=1,command=self.qexit).grid(row=0,column=3)
        #self.leftf3.grid_propagate(0)

    
#-----------------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self,root):
        self.frame=Frame(root,height=500,width=700,bg="black")
        self.frame.pack()
        #labels
        self.title=Label(self.frame,font=('arial',20,'bold'),text="FLASH VEHICLE RENTAL SERVICE",bg="black",fg="red")
        self.title.pack(side=TOP)
        self.title2=Label(self.frame,font=('arial',10,'bold','italic'),text="FLEXIBLE.ACCESSIBLE.AFFORDABLE",bg="black",fg="red")
        self.title2.pack(side=TOP)
        #buttons
        self.login_button=Button(self.frame,font=('arial',16,'bold'),text="LOGIN",fg="red",bg="black",command=self.login)
        self.login_button.pack(side=BOTTOM,fill=X,padx=10,pady=10)
        self.reg_button=Button(self.frame,font=('arial',16,'bold'),text="REGISTER",fg="red",bg="black",command=self.register)
        self.reg_button.pack(side=BOTTOM,fill=X,padx=10,pady=10)
        self.frame.pack_propagate(0)

        
#--------------------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------------------

    

#main
create_table()

root=Tk()
c=project(root)
root.mainloop()
#-------------------------------------------------------------------------------------------------------------
"""def exit1():
    conn.close()
    exit()"""



        


'''root=Tk()


root.title("CAR RENTAL SYSTEM")
root.geometry('1100x700')
leftf = Frame(root,width=800,height=650,bd=8,relief="raise",bg='cyan')
leftf.pack(side=LEFT)

rightf=Frame(root,width=300,height=650,bd=8,relief="raise",bg='cyan')
rightf.pack(side=RIGHT)

leftf1 = Frame(leftf,width=1000,height=325,bd=8,relief="raise",bg='black')
leftf1.pack(side=TOP),
leftf2= Frame(leftf,width=1000,height=225,bd=8,relief="raise",bg='black')
leftf2.pack(side=TOP)
leftf3= Frame(leftf,width=1000,height=100,bd=8,relief="raise",bg='black')
leftf3.pack(side=TOP)


rightf1=Frame(rightf,width=350,height=325,bd=8,relief="raise",bg='black')
rightf1.pack(side=TOP)

rightf2=Frame(rightf,width=350,height=325,bd=8,relief="raise",bg='black')
rightf2.pack(side=BOTTOM)

#----------------------------------------------------------

lblCustomerName=Label(leftf1,font=('arial',10,'bold'),text='CUSTOMER NAME',bd=8,fg='red',bg='black')
lblCustomerName.grid(row=1,column=0)
txtCustomerName=Entry(leftf1,font=('arial',10,'bold'),bd=8,width=31,justify='left')
txtCustomerName.grid(row=1,column=1)

lblNoOfDaysRented=Label(leftf2,font=('arial',10,'bold'),text='NO. OF DAYS RENTED',bd=8,fg='red',bg='black')
lblNoOfDaysRented.grid(row=1,column=2)
txtNoOfDaysRented=Entry(leftf2,font=('arial',10,'bold'),bd=8,width=31,justify='left')
txtNoOfDaysRented.grid(row=1,column=3)

lblSource=Label(leftf2,font=('arial',10,'bold'),text='SOURCE',bd=8,fg='red',bg='black')
lblSource.grid(row=1,column=0)
txtSource=Entry(leftf2,font=('arial',10,'bold'),bd=8,width=31,justify='left')
txtSource.grid(row=1,column=1)

lblDestination=Label(leftf2,font=('arial',10,'bold'),text='DESTINATION',bd=8,fg='red',bg='black')
lblDestination.grid(row=2,column=0)
txtDestination=Entry(leftf2,font=('arial',10,'bold'),bd=8,width=31,justify='left')
txtDestination.grid(row=2,column=1)

lblContactNo=Label(leftf1,font=('arial',10,'bold'),text='CONTACT NO.',bd=8,fg='red',bg='black')
lblContactNo.grid(row=2,column=0)
txtContactNo=Entry(leftf1,font=('arial',10,'bold'),bd=8,width=31,justify='left')
txtContactNo.grid(row=2,column=1)

lblTotal=Label(leftf2,font=('arial',10,'bold'),text='TOTAL',bd=8,fg='red',bg='black')
lblTotal.grid(row=2,column=2,sticky=W)
txtTotal=Entry(leftf2,font=('arial',10,'bold'),bd=8,width=31,justify='left')
txtTotal.grid(row=2,column=3)

lblSuggestion=Label(rightf2,font=('arial',10,'bold'),text='SUGGESTION BOX',bd=8,fg='red',bg='black')
lblSuggestion.grid(row=0,column=0)
txtSuggestion=Text(rightf2,height=6,width=30,bd=8,font=('arial',12,'bold')).grid(row=1,column=0)

var=StringVar(root)
option=OptionMenu(leftf1,var,'CAR','7 SEATER','BUS')
var.set('CAR')
option.grid(row=3,column=1)
lbltype=Label(leftf1,font=('arial',10,'bold'),text='SELECT TYPE OF VEHICLE',bd=4,fg='red',bg='black')
lbltype.grid(row=3,column=0)

w=Message(leftf1,text="WELCOME TO VEHICLE RENTAL SYSTEM!!! ",anchor='center',font=('calibri',20,'bold'),width=1000,fg='red',bg='black')
w.grid(row=0)
#------------------------------------------------------------
def CarRentalCost():
    noOfDays=int(txtNoOfDaysRented.get())
    rent=noOfDays*500
    txtTotal.delete(0,tkinter.END)
    txtTotal.insert(0,rent)
    return 
#------------------------------------------------------------

var1=IntVar()
var2=IntVar()
var3=IntVar()

CustomerName=StringVar()
NoOfDaysRented=StringVar()
Source=StringVar()
Destination=StringVar()
Total=StringVar()
ContactNo=StringVar()
txtSuggestion=StringVar()


#--------------------------------------------------------------
def qexit():
    qexit=tkinter.messagebox.askyesno("Exit the system","Do you want to quit?")
    if qexit>0:
        root.destroy()
        return 
#--------------------------------------------------------------

w=Message(rightf1,text="CHOOSE NO. OF MEMBERS ",anchor='center',font=('ARIAL',14,'bold'),width=500,fg='red',bg='black')
w.grid(row=0)

twoAdults = Checkbutton(rightf1,text='2 ADULTS\t',onvalue=1,offvalue=0,fg='red',bg='black',font=('arial',11,'bold')).grid(row=1,sticky=W)
fourAdults = Checkbutton(rightf1,text='4 ADULTS\t',onvalue=1,offvalue=0,fg='red',bg='black',font=('arial',11,'bold')).grid(row=2,sticky=W)
oneChild = Checkbutton(rightf1,text='1 CHILD\t',onvalue=1,offvalue=0,fg='red',bg='black',font=('arial',11,'bold')).grid(row=3,sticky=W)
twoChildren = Checkbutton(rightf1,text='2 CHILDREN\t',onvalue=1,offvalue=0,fg='red',bg='black',font=('arial',11,'bold')).grid(row=4,sticky=W)
moreThanfourAd = Checkbutton(rightf1,text='MORE THAN 4 ADULTS\t',onvalue=1,offvalue=0,fg='red',bg='black',font=('arial',11,'bold')).grid(row=5,sticky=W)
moreThantwoCh = Checkbutton(rightf1,text='MORE THAN 2 CHILDREN\t',onvalue=1,offvalue=0,fg='red',bg='black',font=('arial',11,'bold')).grid(row=6,sticky=W)

#--------------------------------------------------------------

def yReset():
    var1.set(0)
    var2.set(0)
    var3.set(0)


    txtCustomerName.delete(0,tkinter.END)
    txtNoOfDaysRented.delete(0,tkinter.END)
    txtSource.delete(0,tkinter.END)
    txtDestination.delete(0,tkinter.END)
    txtTotal.delete(0,tkinter.END)
    txtContactNo.delete(0,tkinter.END)
    txtSuggestion.delete(0,tkinter.END)

#-----------------------------------------------------------




btnTotal=Button(leftf3,text='TOTAL',padx=4,pady=4,bd=16,fg='red',bg='black',
            font=('arial',12,'bold'),width=14,height=1,command=CarRentalCost).grid(row=0,column=0)
btnBook=Button(leftf3,text='BOOK',padx=4,pady=4,bd=16,fg='red',bg='black',
            font=('arial',12,'bold'),width=14,height=1,command=display).grid(row=0,column=1)
btnSubmit=Button(leftf3,text='SUBMIT',padx=4,pady=4,bd=16,fg='red',bg='black',
            font=('arial',12,'bold'),width=14,height=1,command=insert).grid(row=0,column=2)
btnExit=Button(leftf3,text='EXIT',padx=4,pady=4,bd=16,fg='red',bg='black',
            font=('arial',12,'bold'),width=14,height=1,command=qexit).grid(row=0,column=3)



root.mainloop()
'''
