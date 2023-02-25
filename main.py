import sqlite3
import tkinter
from tkinter import  *
try:
    cnt=sqlite3.connect('shop.db')
    #print("opened database succsesfully")
except:
    print("an error occured in db connection")
#---------------------CREATE users TABLE----------------------
# query='''CREATE TABLE users
#     (ID INTEGER PRIMARY KEY,
#     user CHAR(25) NOT NULL,
#     pass CHAR(25) NOT NULL,
#     addr CHAR(50)  NOT NULL,
#     comment CHAR(50)
# )'''
# cnt.execute(query)
# print("Table created succsesfully")
# cnt.close()
#---------------------CREATE FAINALSHOP TABLE----------------------
# query='''CREATE TABLE finalshop
# (ID INTEGER PRIMARY KEY,
# uid int NOT NULL,
# pid int NOT NULL,
# qnt int NOT NULL
# )'''
# cnt.execute(query)
# print("table created")
# cnt.close()
#---------------------Insert----------------------------------------
# query='''INSERT INTO users(user,pass,addr)
# VALUES("admin","123456789","rasht")'''
# cnt.execute(query)
# cnt.commit()
# cnt.close()
#--------------------------create producte table---------------
# query='''CREATE TABLE products
#     (ID INTEGER PRIMARY KEY,
#     pname CHAR(25) NOT NULL,
#     price int NOT NULL,
#     qnt int NOT NULL
# )'''
# cnt.execute(query)
# print("Table created succsesfully")
# cnt.close()

#---------------------Insert----------------------------------------
# query='''INSERT INTO products(pname,price,qnt)
# VALUES("nokia n95","100","20")'''
# cnt.execute(query)
# cnt.commit()
# cnt.close()

#--------------------------------functions---------------------------------
def login():
    global userID
    global user
    user=user_txt.get()
    pas=pass_txt.get()
    query='''SELECT id FROM users WHERE user==? AND pass==?'''
    result=cnt.execute(query,(user,pas))
    rows=result.fetchall()
    if len(rows)<1:
        msg_lbl.configure(text="wrong username or password",fg="red")
        return
    if user=="admin":
        btn_adminpanel.configure(state="active")

    userID = rows[0][0]
    msg_lbl.configure(text="welcome to your accont", fg="green")
    btn_login.configure(state="disabled")
    btn_logout.configure(state="active")
    btn_shop.configure(state="active")
    user_txt.delete(0,"end")
    pass_txt.delete(0,"end")

    user_txt.configure(state="disabled")
    pass_txt.configure(state="disabled")
def logout():
    msg_lbl.configure(text="you are logged out now", fg="green")
    btn_login.configure(state="active")
    btn_logout.configure(state="disabled")
    btn_shop.configure(state="disabled")
    user_txt.configure(state="normal")
    pass_txt.configure(state="normal")

def shop():
    global txt_id
    global txt_qnt
    global lbl_msg2
    global rows
    shop_win=tkinter.Toplevel(win)
    shop_win.geometry("500x500")
    shop_win.title("shopping panel")
    shop_win.resizable(False,False)   #برای اینکه نتواند پنجره ویندورز را بزرگ کند
# ----------------------------------fetch all prodouct-----------------------
    query = '''SELECT * FROM products'''
    result = cnt.execute(query)
    rows = result.fetchall()
#-----------------------------------list Box--------------------------------
    lstbox=tkinter.Listbox(shop_win,width=50)
    lstbox.pack(pady=10)
    for items in rows:
        #msg=str(items[0])+"    "+items[1]+"    "+"price:"+str(items[2])+"     "+"QNT:"+str(items[3])
        msg=f"{items[0]}----{items[1]}-----price:{items[2]}----QNT:{items[3]}"
        lstbox.insert("end",msg)
    #lstbox.insert("end","TEST")
#--------------------------------shop widgets--------------------------
    lbl_id=tkinter.Label(shop_win,text="product ID:")
    lbl_id.pack()

    txt_id=tkinter.Entry(shop_win,width=20)
    txt_id.pack()

    lbl_qnt = tkinter.Label(shop_win, text="product QNT:")
    lbl_qnt.pack()
    txt_qnt = tkinter.Entry(shop_win, width=20)
    txt_qnt.pack()

    lbl_msg2=tkinter.Label(shop_win,text="")
    lbl_msg2.pack()

    btn_fainal_shop=tkinter.Button(shop_win,text="SHOP NOW!",fg="yellowgreen",command=final_shop)
    btn_fainal_shop.pack(pady=10)

    shop_win.mainloop()
def final_shop():
    pid=txt_id.get()
    pqnt=txt_qnt.get()
    if pid=="" or pqnt=="":
        lbl_msg2.configure(text="Please Fill All The Blanks",fg="orange")
        return
    query='''SELECT * FROM products WHERE id=?'''
    result=cnt.execute(query,(pid,))
    rows=result.fetchall()
    if len(rows)==0:
        lbl_msg2.configure(text="Wrong product id", fg="red")
        return

    real_pqnt=rows[0][3]
    if int(pqnt)>real_pqnt:
        lbl_msg2.configure(text="Not enough product quantity", fg="red")
#--------------------------INSERT in to Finalshop Table----------------------
    query = '''INSERT INTO finalshop(uid,pid,qnt)
    VALUES(?,?,?)'''
    cnt.execute(query,(userID,pid,pqnt))
    cnt.commit()
#--------------------------Update product Table----------------------------
    new_qnt=real_pqnt-int(pqnt)
    query='''UPDATE products SET qnt=? WHERE id=?'''
    cnt.execute(query,(new_qnt,pid))
    cnt.commit()
    lbl_msg2.configure(text="successfully added to cart", fg="green")
    txt_id.delete(0,"end")
    txt_qnt.delete(0,"end")
    # for item in rows:
    #     if int(pqnt)<=item[3]:
    #         lbl_msg2.configure(text="you can shop now", fg="green")                  روش دیگرحل این قسمت
    #     else:
    #         lbl_msg2.configure(text="Not enough product quantity", fg="red")
    #         return
#------------------------------submit-------------------------------------
def submit():
    global  txt_ownpas
    global txt_ownuser
    global txt_cpas
    global txt_addr
    global msgsub_lbl
    submit = tkinter.Toplevel(win)
    submit.geometry("300x250")
    submit.title("submit")
    msgsub_lbl = tkinter.Label(submit, text="")
    msgsub_lbl.pack()
    lbl_ownuser = tkinter.Label(submit, text="username:")
    lbl_ownuser.pack()

    txt_ownuser = tkinter.Entry(submit, width=20)
    txt_ownuser.pack()

    lbl_ownpas = tkinter.Label(submit, text="password:")
    lbl_ownpas.pack()
    txt_ownpas = tkinter.Entry(submit, width=20)
    txt_ownpas.pack()

    lbl_cpas = tkinter.Label(submit, text="confirm password:")
    lbl_cpas.pack()
    txt_cpas = tkinter.Entry(submit, width=20)
    txt_cpas.pack()

    lbl_addr = tkinter.Label(submit, text="address:")
    lbl_addr.pack()
    txt_addr = tkinter.Entry(submit, width=20)
    txt_addr.pack()

    btn_submit = tkinter.Button(submit, text="submit Now!", command=submit_now)
    btn_submit.pack(pady="10")

def submit_now():
    new_user =txt_ownuser.get()
    new_pas = txt_ownpas.get()
    cpas=txt_cpas.get()
    addr=txt_addr.get()
    query = '''SELECT * FROM users'''
    result = cnt.execute(query)
    rows = result.fetchall()
    if (len(new_pas) < 8):
        msgsub_lbl.configure(text="your password must upper than 8 charachters", fg="red")
        return

    if new_pas!=cpas:
        msgsub_lbl.configure(text="ERROR:Miss match", fg="red")
        return
    txt_ownuser.delete(0, "end")
    txt_ownpas.delete(0, "end")
    txt_cpas.delete(0, "end")

    msgsub_lbl.configure(text="submit done!!!", fg="green")


    query = '''INSERT INTO users(user,pass,addr)
        VALUES(?,?,?)'''
    cnt.execute(query, (new_user,new_pas,addr))
    cnt.commit()
#--------------------------------------Admin Panel------------------------------
def admin():
    global txt_pname
    global txt_price
    global txt_qnt1
    global msgadd_lbl
    admin = tkinter.Toplevel(win)
    admin.geometry("300x250")
    admin.title("adminpanel")
    msgadd_lbl = tkinter.Label(admin, text="")
    msgadd_lbl.pack()
    lbl_pname = tkinter.Label(admin, text="product name:")
    lbl_pname.pack()

    txt_pname = tkinter.Entry(admin, width=20)
    txt_pname.pack()

    lbl_price = tkinter.Label(admin, text="price:")
    lbl_price.pack()
    txt_price = tkinter.Entry(admin, width=20)
    txt_price.pack()

    lbl_qnt1 = tkinter.Label(admin, text="quantity:")
    lbl_qnt1.pack()
    txt_qnt1 = tkinter.Entry(admin, width=20)
    txt_qnt1.pack()
    btn_insert = tkinter.Button(admin, text="Insert", command=insert)
    btn_insert.pack(pady="5")
def insert():
    producte = txt_pname.get()
    price = txt_price.get()
    qnt = txt_qnt1.get()
    query = '''INSERT INTO products(pname,price,qnt)
           VALUES(?,?,?)'''
    cnt.execute(query, (producte,price,qnt))
    cnt.commit()
    msgadd_lbl.configure(text="succsesfully!!!", fg="green")

#---------------------------------myshop-------------------------------
def myshop():
    myshop=tkinter.Toplevel(win)
    myshop.geometry("300x250")
    myshop.title("my shop")
    myshop.configure(background="silver")
    lab=Label(myshop,text="Your shopping table",fg="black",bg="teal").pack(side="top")
    query=''' SELECT id FROM users where user==?'''
    result=cnt.execute(query,(user,))
    row=result.fetchone()
    query='''SELECT pid,qnt FROM finalshop where uid=?'''
    final_resulte=cnt.execute(query,(row[0],))
    rows=final_resulte.fetchall()

    for i in rows:
        query='''SELECT pname,price from products where id=?'''
        result3 = cnt.execute(query,(i[0],))
        row1= result3.fetchall()
    lstbox=tkinter.Listbox(myshop,width=30)
    lstbox.pack(pady="5")
    for i in row1:
        msg=f"Name:{i[0]}-----price:{i[1]}"
        lstbox.insert("end",msg)





#-------------------------------Main---------------------------------------
win=tkinter.Tk()
win.geometry("500x400")
win.title("Shopping Center")
lab=Label(win,text="Welcome to our Shopping Center",fg="black",bg="skyblue").pack(side="top")

user_lbl=tkinter.Label(win,text="username:")
user_lbl.pack()

user_txt=tkinter.Entry(win,width=25)
user_txt.pack()

pass_lbl=tkinter.Label(win,text="password:")
pass_lbl.pack()

pass_txt=tkinter.Entry(win,width=25)
pass_txt.pack()

msg_lbl=tkinter.Label(win,text="")
msg_lbl.pack()

btn_login=tkinter.Button(win,text="login",command=login)
btn_login.pack(pady="5")

btn_logout=tkinter.Button(win,text="logout",state="disabled",command=logout)
btn_logout.pack(pady="5")

btn_shop=tkinter.Button(win,text="shop",state="disabled",command=shop)
btn_shop.pack(pady="5")

btn_submit=tkinter.Button(win,text="submit",command=submit)
btn_submit.pack(pady="5")

btn_adminpanel=tkinter.Button(win,text="adminPanel",state="disabled",command=admin)
btn_adminpanel.pack(pady="5")

btn_myshop=tkinter.Button(win,text="myshop",command=myshop)
btn_myshop.pack(pady="5")



win.mainloop()
