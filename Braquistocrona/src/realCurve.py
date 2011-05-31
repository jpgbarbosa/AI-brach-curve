from math import sin, cos, pi

def brachistochroneReal(x0, y0, x1, y1, n):
    dy = y0 - y1
    prec=10.0**-12

    t1=0.0
    t2=2*pi

    xm=x0
    while abs(xm-x1) > prec:
        tm = (t1+t2)/2
        
        if (1-cos(tm)==0):
            continue
        
        rm = dy / (1 - cos(tm))
        xm = x0 + rm * (tm - sin(tm))
        
        if (xm > x1):
            #pag 258
            t2 = tm
        else:
            t1 = tm

    L=[]
    L2=[]
    r=rm
    for i in xrange(n+1):
        t=tm*i/n
        L.append ( (x0+r*(t-sin(t)), y0-r*(1-cos(t))) )
        L2.extend ( (x0+r*(t-sin(t)), y0-r*(1-cos(t))) )
    #print(r, L[-1])
    
    return L, L2

