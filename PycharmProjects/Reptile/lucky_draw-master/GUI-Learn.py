import tkinter

root = tkinter.Tk()
root.title('窗口标题')
root.geometry('1000x700+0+0')

# label标签，button按钮，Text文本，,输入框控件entry,Canvas画布,place绝对布局，pack相对布局，grid相对布局

label = tkinter.Label(root,text='输入文字：',font=('宋体',20),bg='white',width=10,height=8)
# label.place(x=100,y=100)
label.pack()

var = tkinter.StringVar()
l = tkinter.Label(root, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
l.pack()

on_hit = False
def hit_me():
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('you hit me')
        l2.config(text='11111')
    else:
        on_hit = False
        var.set('')
        l2.config(text='22222')

l2 = tkinter.Label(root, bg='yellow', width=20, text='empty')
l2.pack()

btn = tkinter.Button(root,text='hit me', font=('Arial', 12), width=10, height=1, command=hit_me)
btn.pack()

var2 = tkinter.StringVar()
var2.set((1,2,3,4))
lb = tkinter.Listbox(root, listvariable=var2)
lb.pack()

# 添加菜单栏
menubar = tkinter.Menu(root)
filemenu = tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)

filemenu.add_command(label='New')

root.config(menu=menubar)
root.mainloop()