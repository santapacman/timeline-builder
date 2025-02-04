from tkinter import *
from tkinter import filedialog
import ctypes as ct







def dark_title_bar(window):
    """
    MORE INFO:
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                         ct.sizeof(value))








def clone_widget(widget, master=None):
    """
    Create a cloned version o a widget

    Parameters
    ----------
    widget : tkinter widget
        tkinter widget that shall be cloned.
    master : tkinter widget, optional
        Master widget onto which cloned widget shall be placed. If None, same master of input widget will be used. The
        default is None.

    Returns
    -------
    cloned : tkinter widget
        Clone of input widget onto master widget.

    """
    # Get main info
    parent = master if master else widget.master
    cls = widget.__class__

    # Clone the widget configuration
    cfg = {key: widget.cget(key) for key in widget.configure()}
    cloned = cls(parent, **cfg)

    # Clone the widget's children
    for child in widget.winfo_children():
        child_cloned = clone_widget(child, master=cloned)
        if child.grid_info():
            grid_info = {k: v for k, v in child.grid_info().items() if k not in {'in'}}
            child_cloned.grid(**grid_info)
        elif child.place_info():
            place_info = {k: v for k, v in child.place_info().items() if k not in {'in'}}
            child_cloned.place(**place_info)
        else:
            pack_info = {k: v for k, v in child.pack_info().items() if k not in {'in'}}
            child_cloned.pack(**pack_info)

    return cloned





def save(yearOffset, lst):
    rep = toRepresentation(yearOffset, lst)
    firstyear = rep[0]
    replst = rep[1]
    outfile = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    for i in range(len(replst)):
        outfile.write(str(i+firstyear) +": ")
        for j in replst[i]:
            j.replace("\n", " ")
            j.replace(" ||| ", "")
            outfile.write(j + " ||| ")
        outfile.write("\n")
    
    print(rep)
def load():
    f = filedialog.askopenfile(mode='r', defaultextension=".txt")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    hasFirst = False
    first = 0
    replst = []
    for i in f:
        print(i)
        s = i[i.index(": ")+2: -1: 1]
        if not hasFirst:
            first=int(i[0:i.index(":"):1])
            hasFirst = True
        tmplst = s.split(" ||| ")
        tmplst.pop()
        replst.append(tmplst)
    return (first, replst)



def toRepresentation(yearOffset, lst):
    i = 0
    while(len(lst[i].children)==0):
        i+=1
        if(i==len(lst)):
            return(0, [])
    firstyear = i
    while i < len(lst):
        if(len(lst[i].children)>0):
            lastyear = i
        i+=1
    lastyear +=1
    replist = []
    for i in range(firstyear, lastyear):
        yearlist = []
        j = 0
        while j < len(lst[i].children):
            yearlist.append(lst[i].children[j].text['text'].strip())
            j+=1
        replist.append(yearlist)
        i+=1
    print(lastyear)
    
    return (firstyear-yearOffset+1, replist)
        

def represents_int(s):
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True