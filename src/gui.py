from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from colour import Color
from . import guihelper


current_widget = None
draggingCard = None
framedict = {}

window = Tk()
window.configure(background="red")
window.title("Timeline Manager")

PADDING = 5
DATE_DIM = 200
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1000
scrollinc = DATE_DIM/4
scrolledLast = False
yearOffset = 1

guihelper.dark_title_bar(window)

def save():
    guihelper.save(yearOffset, lst)
def load():
    global lst
    global yearOffset
    firstyear, replst = guihelper.load()
    for x in lst:
        for child in x.yearframe.winfo_children():
            child.destroy()
        x.yearframe.destroy()
    lst = []
    yearOffset = -firstyear + 1
    print("yearOffset: ", yearOffset)
    for i in range(len(replst)):
        lst.append(DateContainer(firstyear+i, mainframe))
        for j in replst[i]:
            lst[i].addChild(j)
    rightAdder.grid(column=len(lst)+1)
    

def trim():
    global yearOffset
    global lst
    i = 0
    while i < len(lst) and len(lst[i].children) == 0:
        i+=1
    if(i == len(lst)):
        for x in lst:
            for child in x.yearframe.winfo_children():
                child.destroy()
            x.yearframe.destroy()
        lst = []
        yearOffset = 1
        rightAdder.grid(column=1)
        return
    j = len(lst)-1
    while len(lst[j].children) == 0:
        j-=1
        
    q = len(lst) -j
    for x in range(len(lst)-1, j, -1):
        for child in lst[x].yearframe.winfo_children():
            child.destroy()
        lst[x].yearframe.destroy()
        lst.pop()
    for x in range(i):
        for child in lst[0].yearframe.winfo_children():
            child.destroy()
        lst[0].yearframe.destroy()
        lst.pop(0)
    yearOffset = -lst[0].year+1
    for yr in lst:
        print(yearOffset)
        yr.regrid()

        
    rightAdder.grid(column=rightAdder.grid_info()["column"]-q -i +2)

popupyears = None
label  = None
def setyear():
    global popupyears
    global label
    popupyears = Toplevel()
    popupyears.title("Custom Popup")

    instructions = Label(popupyears, text="Enter the first year:")

    instructions.pack(side=TOP, padx=20, pady=20)

    label = Entry(popupyears)
    label.pack(padx = 20, pady=20)

    button = Button(popupyears, text="Close", command=destroyyearpopup)
    button.pack()
    
def destroyyearpopup():
    global popupyears
    global label
    global yearOffset
    s = label.get()
    print("destroying")
    if guihelper.represents_int(s):
        yearOffset = -int(s) +1
    else : return
    for l in range(len(lst)):
        print(l)
        lst[l].reyear(l)
    popupyears.destroy()




def popup(event):
        try:
            popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            popup.grab_release()



window.geometry('{}x{}'.format(SCREEN_WIDTH, SCREEN_HEIGHT))


def mousedown(event):
    global current_widget
    global draggingCard
    widget = event.widget.winfo_containing(event.x_root, event.y_root)
    if widget.winfo_class() == "Labelframe":
        parent = framedict[widget.master.master.master]
        current_widget = parent
        draggingCard = parent.children[parent.eventsdict[widget]]
        parent.mouseDown(widget)
    else: current_widget = widget
    print("mousedown: ", current_widget)

def drag(event):
    global current_widget
    global scrolledLast
    print(event.x_root)
    global draggingCard
    widget = event.widget.winfo_containing(event.x_root, event.y_root)
    if ((widget.winfo_class() == "Labelframe" or (widget.winfo_class()=="Button" and widget.master.master.master.winfo_class()=="Frame"))and draggingCard!=None):
        print("Dragging Card: ", draggingCard==None)
        parent = framedict[widget.master.master.master]
        if current_widget != parent:
            draggingCard = parent.enter(widget, draggingCard.card, draggingCard.text['text'])
            current_widget.leave()
        elif widget.winfo_class()!="Button":
            parent.drag(widget, draggingCard.card)
        if event.x_root < window.winfo_x()+40 and not scrolledLast:
            canvas.xview_scroll(-1, 'units')
            scrolledLast = True
        elif  event.x_root > window.winfo_x() + window.winfo_width()-20 and not scrolledLast:
            canvas.xview_scroll(1, 'units')
            scrolledLast = True
        else: scrolledLast = False
    
        current_widget = parent
    elif draggingCard==None:
        
        print(current_widget.winfo_class())

def release(event):
    global current_widget
    global draggingCard
    if not draggingCard == None:
        current_widget.release()
    current_widget = None
    draggingCard = None


    """if current_widget != widget:
        if current_widget:
            current_widget.event_generate("<<B1-Leave>>")
        current_widget = widget
        current_widget.event_generate("<<B1-Enter>>")"""
    



window.bind_all("<B1-Motion>", drag)
window.bind_all("<Button-1>", mousedown)
window.bind_all("<ButtonRelease-1>", release)
window.bind_all("<Button-3>", popup)

img = Image.open('img/plussign.png')
img2 = img.resize((DATE_DIM,SCREEN_HEIGHT-50) , Image.LANCZOS)
img = img.resize((DATE_DIM, DATE_DIM), Image.LANCZOS)

#This code is adapted from the answer to this stackoverflow question: https://stackoverflow.com/questions/71563715/python-tkinter-double-click-to-edit-text
class EditableLabel(Message):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.entry = Text(parent)
        self.bind("<Double-1>", self.edit_start)
        self.entry.bind("<Return>", self.edit_stop)
        self.entry.bind("<FocusOut>", self.edit_stop)
        self.entry.bind("<Escape>", self.edit_cancel)

    def edit_start(self, event=None):
        self.entry.place(relx=.5, rely=.5, relwidth=1.0, relheight=1.0, anchor="center")
        self.entry.focus_set()

    def edit_stop(self, event=None):
        self.configure(text=self.entry.get("1.0", END))
        self.entry.place_forget()

    def edit_cancel(self, event=None):
        self.entry.delete(0, "end")
        self.entry.place_forget()




def myfunction(event):
    bbox = (canvas.bbox("all")[0],canvas.bbox("all")[1],canvas.bbox("all")[2]+100,canvas.bbox("all")[3])
    canvas.configure(scrollregion=bbox,width=200,height=200)

def colorFromYear(year): 
    rgb = [0,3,6]

    j = 0
    for i in rgb:
        a = (i+year)%9
        a = (-abs(a-5)) + 3
        if a < 0:
            a= 0
        rgb[j] = a/3
        j+=1
    return (rgb[0], rgb[1], rgb[2])

class DateContainer:
    def __init__(self, year, parent):
        self.eventsdict = {}
        

        brgb, clr, hdrclr = self.color(year)
        self.draggingIndex = -1


        self.parent = parent
        self.year = year
        self.yearframe = Frame(parent, height=SCREEN_HEIGHT-50, width=DATE_DIM+20, background = clr.get_hex())
        framedict[self.yearframe] = self
        self.yearframe.pack_propagate(False)
        self.yearframe.grid(row = 0, column=year+yearOffset, sticky=(N))
        self.yearcanvas = Canvas(self.yearframe, bg=clr.get_hex(), width = DATE_DIM)
        self.eventsframe = Frame(self.yearcanvas, pady=PADDING)
        self.yearheader = Label(self.yearframe, text = str(year), bg = hdrclr.get_hex(), fg="white")
        self.yearheader.pack(side="top", fill="x")
        self.yearcanvas.pack(side="left",anchor=NW)
        self.yearcanvas.create_window((0,0), window=self.eventsframe, anchor='nw', tags='eventsframe')
        self.img = ImageTk.PhotoImage(img)

        self.children = []
   
        self.eventSpawner = Button(self.eventsframe, image= self.img, width=DATE_DIM, height=DATE_DIM, bg=clr.get_hex(), command = self.addChildSmall)
        self.eventSpawner.grid(row = 0, column=0)

        self.placeholder = Canvas(self.eventsframe, width = DATE_DIM, height = DATE_DIM, bg=clr.get_hex())

        self.vsb = Scrollbar(self.yearframe, orient="vertical", command=self.yearcanvas.yview, jump=True)
        self.vsb.pack(side="right", fill="y")
        self.yearcanvas.configure(yscrollcommand=self.vsb.set, yscrollincrement=scrollinc, scrollregion=self.yearcanvas.bbox("all"))

    def color(self, year):
        brgb = colorFromYear(year)
        clr = Color(rgb=brgb)
        clr.set_saturation(clr.get_saturation()/4)
        clr.set_luminance(clr.get_luminance()/2)
        hdrclr  = Color(rgb=brgb)
        hdrclr.set_luminance(hdrclr.get_luminance()/3)
        return brgb, clr, hdrclr

    def regrid(self):
        self.yearframe.grid(column=self.year+yearOffset)

    def reyear(self, index):
        self.year = index-yearOffset+1
        brgb, clr, hdrclr = self.color(self.year)
        self.yearheader.configure(text=str(self.year), bg=hdrclr.get_hex())
        self.yearframe.configure(background=clr.get_hex())
        self.yearcanvas.configure(bg=clr.get_hex())
        self.eventSpawner.configure(bg=clr.get_hex())
        for c in self.children:
            c.reyear(self.year)

    def addChildSmall(self):
        self.eventSpawner.grid(row = len(self.children)+1)
        self.children.append(Date(self.year, self.eventsframe, len(self.children)))
        self.children[-1].card.grid(row=(len(self.children)-1), column=0)
        self.yearcanvas.configure(height=self.eventsframe.grid_size()[1]*(DATE_DIM + PADDING))
        self.eventsdict[self.children[-1].card]= len(self.children)-1
        bbox = self.yearcanvas.bbox("all")
        bbox2 = (bbox[0],bbox[1],bbox[2],bbox[3]+DATE_DIM*2)
        self.yearcanvas.configure(yscrollcommand=self.vsb.set, yscrollincrement=scrollinc, scrollregion=bbox2)

    def addChild(self, text):
        self.eventSpawner.grid(row = len(self.children)+1)
        self.children.append(Date(self.year, self.eventsframe, text))
        self.children[-1].card.grid(row=(len(self.children)-1), column=0)
        self.yearcanvas.configure(height=self.eventsframe.grid_size()[1]*(DATE_DIM + PADDING))
        self.eventsdict[self.children[-1].card]= len(self.children)-1
        bbox = self.yearcanvas.bbox("all")
        bbox2 = (bbox[0],bbox[1],bbox[2],bbox[3]+DATE_DIM*2)
        self.yearcanvas.configure(yscrollcommand=self.vsb.set, yscrollincrement=scrollinc, scrollregion=bbox2)

    def mouseDown(self, widget):
        self.draggingIndex = self.eventsdict[widget]


    def enter(self, widget, dragCard, text):
        if(widget!=self.eventSpawner):
            self.draggingIndex = self.eventsdict[widget]
            i = self.draggingIndex
        else:
            self.draggingIndex = len(self.children)
            i= len(self.children)
        self.children.insert(i, Date(self.year, self.eventsframe, i))
        self.children[i].setText(text)
        while i < len(self.children):
            self.eventsdict[self.children[i].card] = i
            self.children[i].newIndex(i)
            i+=1
        self.eventSpawner.grid(row=len(self.children))
        self.yearcanvas.configure(height=self.eventsframe.grid_size()[1]*(DATE_DIM + PADDING))
        self.eventsdict[self.children[-1].card]= len(self.children)-1
        bbox = self.yearcanvas.bbox("all")
        bbox2 = (bbox[0],bbox[1],bbox[2],bbox[3]+DATE_DIM*2)
        self.yearcanvas.configure(yscrollcommand=self.vsb.set, yscrollincrement=scrollinc, scrollregion=bbox2)
        return self.children[self.draggingIndex]


        
    def leave(self):
        print(self.draggingIndex)
        self.eventsdict.pop(self.children[self.draggingIndex].card)
        i = self.draggingIndex
        w = self.children.pop(i)
        while i < len(self.children):
            self.eventsdict[self.children[i].card] = i
            self.children[i].newIndex(i)
            i+=1
        self.draggingIndex=-1
        w.card.destroy()

    def drag(self, switch, dragCard):
        if switch!= dragCard:
            i, j = self.eventsdict[switch], self.eventsdict[dragCard]
            self.eventsdict[switch],self.eventsdict[dragCard] = j, i
            print(i, j)
            self.children[i].newIndex(j)
            self.children[j].newIndex(i)
            self.children[i], self.children[j] = self.children[j], self.children[i]
            self.draggingIndex = i
            print(i, j)

    def release(self):
        self.draggingIndex=-1

    """def enter(self, event):
        global draggingCard
        if self.draggingHere and index != self.draggingIndex and draggingCard:
            print("here")
            draggedCard = self.children[self.draggingIndex]
            switchedCard = self.children[index]

            self.children[self.draggingIndex], self.children[index] = self.children[index], self.children[self.draggingIndex]

            draggedCard.newIndex(index)
            switchedCard.newIndex(self.draggingIndex)
            self.draggingIndex = index"""

        #todo: shrink canvas scrollable bbox

def addOne():
    yearOffset = 1
    newYear = DateContainer(0, mainframe)
    lst.append(newYear)
    rightAdder.grid(column=2, row=0)

def addLeft():
    global lst
    if(lst == []):
        addOne()
        return
    global yearOffset
    yearOffset+=1
    newYear = DateContainer(lst[0].year-1, mainframe)
    for i in lst:
        i.regrid()
    lst.insert(0, newYear)
    rightAdder.grid(column = rightAdder.grid_info()['column']+1)

def addRight():
    global lst
    if(lst==[]):
        addOne()
        return
    newYear = DateContainer(lst[-1].year+1, mainframe)
    lst.append(newYear)
    rightAdder.grid(column = rightAdder.grid_info()['column']+1)
    canvas.xview_scroll(DATE_DIM, "units")
    print("mov")




class Date:
    def __init__(self, year, parent, index):
        self.year = year
        self.parent = parent
        brgb = colorFromYear(year)
        colormid = Color(rgb=brgb)
        colormid.set_luminance(colormid.get_luminance()*1.2)
        colormid.set_saturation(colormid.get_saturation()/4)
        colorfinal = colormid.get_hex()
        self.card = LabelFrame(parent, width=DATE_DIM, height=DATE_DIM, bg=colorfinal)
        self.card.grid_propagate(False)
        self.text = EditableLabel(self.card, text=str(index), justify=CENTER, bg = colorfinal)
        self.text.place(relx=0.5, rely=0.5, anchor=CENTER)


    def setText(self, textt):
        print(textt)
        self.text.configure(text=textt)

    def drag(self, event):
        print(str(self.year) + ": " + str(event.y_root - window.winfo_y()))
        gridnums = self.parent.grid_size()
        print(min(gridnums[1], int((event.y_root - window.winfo_y())/DATE_DIM)))
        self.card.grid(row = min(gridnums[1], int((event.y_root - window.winfo_y())/DATE_DIM)), column = min(gridnums[0]-1, int((event.x_root - window.winfo_x())/DATE_DIM)))

    def newIndex(self, index):
        self.index = index
        self.card.grid(row=index, column=0)

    def reyear(self, year):
        self.year = year
        brgb = colorFromYear(year)
        colormid = Color(rgb=brgb)
        colormid.set_luminance(colormid.get_luminance()/1.2)
        colormid.set_saturation(colormid.get_saturation()/2)
        colorfinal = colormid.get_hex()
        self.card.configure(bg=colorfinal)
        self.text.configure(bg=colorfinal)


canvas = Canvas(window, bg="#222222")
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

s = ttk.Style()
s.configure('TFrame', background='#222222')
mainframe = ttk.Frame(canvas, padding="3 3 12 12", style="TFrame")

myscrollbar=Scrollbar(window,orient="horizontal",command=canvas.xview, jump = True)
canvas.configure(xscrollcommand=myscrollbar.set, xscrollincrement=DATE_DIM)





myscrollbar.pack(side='bottom', fill = 'x')
canvas.pack(side='left', fill='both', expand=True)
canvas.create_window((0,0), window=mainframe, anchor='nw', tags='mainframe')
mainframe.bind("<Configure>",myfunction)

popup = Menu(window.winfo_toplevel(), tearoff=0)
popup.add_command(label="Save", command=save)
popup.add_command(label="Load", command=load)
popup.add_command(label="Trim Outside Years", command=trim)
popup.add_command(label="Set first year to...", command = setyear)


imgl = ImageTk.PhotoImage(img2)
imgr = ImageTk.PhotoImage(img2)
leftAdder = Button(mainframe, image= imgl, width=DATE_DIM, height=SCREEN_HEIGHT-50, bg="red", command = addLeft)
rightAdder = Button(mainframe, image= imgr, width=DATE_DIM, height=SCREEN_HEIGHT-50, bg="red", command = addRight)

leftAdder.grid(row=0,column=0)

lst = []
for i in range(20):
    lst.append(DateContainer(i, mainframe))

rightAdder.grid(row=0, column= len(lst)+1)
leftAdder.lift()
rightAdder.lift()

window.mainloop()


def main():
    print()