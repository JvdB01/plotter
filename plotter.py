import plotly.plotly as py
import plotly.graph_objs as go
import math
import sympy as sym
import settings

derivative=None
show1=None
dplot=None
option=None
yadd=None
dyadd=None
debug=settings.debug
menu=settings.menu
showdebug=settings.showdebug
minmax=settings.minmax
hardlock=settings.hardlock
verbose=settings.verbose

while menu == True and option != "0" and option != "1":
    print ("\n" * 100)
    if minmax == False: hardlock = False
    if minmax == True: minmaxspaces=1
    else: minmaxspaces=0
    if hardlock == True: hardlockspaces=1
    else: hardlockspaces=0
    if verbose == True: verbosespaces=1
    else: verbosespaces=0
    print("     ┌─────────────────────┐")
    print("     │       M E N U       │")
    if showdebug == True:
        print("     │0) debugging mode    │")
    if showdebug == True:
        print("     │1) normal mode       │")
    else:
        print("     │1) start             │")
    print("     │2) min-max:   ", minmax,  (" " * minmaxspaces) + "│")
    print("     │3) hardlock:  ", hardlock, (" " * hardlockspaces) + "│")
    print("     │4) verbose:   ", verbose, (" " * verbosespaces) + "│")
    print("     │q) quit              │")
    print("     └─────────────────────┘")
    option=input("option: ")
    if option == "0" and showdebug == True: debug = True
    if option == "0" and showdebug == False: option = "nope"
    if option == "1": debug = False
    if option == "2": minmax = not minmax
    if option == "3": hardlock = not hardlock
    if option == "4": verbose = not verbose
    if option == "q": raise SystemExit(0)
xmin=float(input("insert minimum: "))
xmax=float(input("insert maximum: "))
yminvalue=xmin/settings.yminscale
ymaxvalue=xmax/settings.ymaxscale
yminlist=[]
ymaxlist=[]

if xmax<=xmin:
    print("nice try -_-")
    raise SystemExit(0)

print("ok, making x-axis...")
xdata=[xmin]
xadd =xmin
while xmax>xmin:
    xadd=round(xadd+0.1, 3)
    xdata.append(xadd)
    xmax = round(xmax-0.1, 3)
    if debug == True:
        print("[+] debugging data: ", xadd, xdata, xmax)
for x in xdata:
    yminlist.append(yminvalue)
    ymaxlist.append(ymaxvalue)
print("done!")

formula_raw=input("enter formula: ")
formula_processed=formula_raw.replace("^", "**").replace("sqrt", "math.sqrt").replace("sin", "math.sin").replace("cos", "math.cos").replace("tan", "math.tan").replace("log", "math.log")
print("do you want to plot this graph?")
while show1 != "y" and show1 != "n":
    show1=input("choose(y/n): ")
if show1 == "y":
    print("ok, calculating y-axis...")
    ydata=[]
    for x in xdata:
        try:
            if int(x) == x and verbose == True:
                print("(", x, ", ", eval(formula_processed), ")")
            if debug == True:
                print("[+] debugging data: ", ydata)
            yadd=eval(formula_processed)
            if hardlock == True:
                if yadd < yminvalue:
                    yadd=yminvalue
                if yadd > ymaxvalue:
                    yadd=ymaxvalue
        except ZeroDivisionError:
            if verbose == True:
                print("division by zero, ignoring")
        except ValueError:
            if verbose == True:
                print("value error, ignoring")
        if yadd == None:
            ydata.append(yadd)
        else:
            ydata.append(yadd.real)

while derivative == None:
    print("do you want a derivative?")
    derivative=input("choose(y/n): ")
    if derivative == "y":
        x, t, z, nu = sym.symbols('x t z nu')
        print("ok, calculating derivative...")
        dformula_simple=str(sym.diff(sym.sympify(formula_raw), x))
        dformula=str(sym.diff(sym.sympify(formula_raw), x)).replace("^", "**").replace("sqrt", "math.sqrt").replace("sin", "math.sin").replace("cos", "math.cos").replace("tan", "math.tan").replace("log", "math.log")
        print("the derivative formula is: ", dformula_simple)
        print("do you want to plot it?")
        while dplot != "y" and dplot != "n":
            dplot=input("choose(y/n): ")
        if dplot == "y":
            print("ok, plotting...")
            dydata=[]
            for x in xdata:
                try:
                    if int(x) == x and verbose == True:
                        print("(", x, ", ", eval(dformula), ")")
                    if debug == True:
                        print("[+] debugging data: ", dydata)
                    dyadd=eval(dformula)
                    if hardlock == True:
                        if dyadd.real < yminvalue:
                            dyadd=yminvalue
                        if dyadd.real > ymaxvalue:
                            dyadd=ymaxvalue
                except ZeroDivisionError:
                    print("division by zero, ignoring")
                except ValueError:
                    print("value error, ignoring")
                if dyadd == None:
                    dydata.append(dyadd)
                else:
                    dydata.append(dyadd.real)
            print("alright, finishing up...")
    else:
        if derivative == "n":
            dplot="n"
            print("ok, plotting...")
        else:
            derivative=None

if show1 == "n" and dplot == "n":
    print("ok, bye!")
    raise SystemExit(0)

if show1 == "y":
    f1 = go.Scatter(
        x=xdata,
        y=ydata
    )

if dplot == "y":
    f2 = go.Scatter(
        x=xdata,
        y=dydata
    )

top = go.Scatter(
    x=xdata,
    y=ymaxlist
)

bottom = go.Scatter(
    x=xdata,
    y=yminlist
)


if minmax == True:     
    if show1 == "y":
        data=[f1,top,bottom]

    if dplot == "y":
        data=[f2,top,bottom]

    if show1 == "y" and dplot == "y":
        data=[f1,f2,top,bottom]

if minmax == False:     
    if show1 == "y":
        data=[f1]

    if dplot == "y":
        data=[f2]

    if show1 == "y" and dplot == "y":
        data=[f1,f2]

py.plot(data,filename = 'f1', auto_open=True)
