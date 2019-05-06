import numpy as np
import matplotlib.pyplot as plt

def func(x,a,b,c):
    return a * np.exp(-b * x) + c

def curve_fitter(x,y,order):
    import numpy as np
    '''
    Function which determines order of polynomial fit with the highest R_squared value
    for the input arrays x & y. Tested between 1st and 10th order polynomials.
    '''  
      
    polylist = np.linspace(1,order,order)
    for i in range(len(polylist)):
        coeffs = np.polyfit(x, y, polylist[i])
        p = np.poly1d(coeffs)
   
        f = p(x)                                #fits x-values to curve                       
        ybar = np.sum(y)/len(y)                 #calculates mean y value
        ssres = np.sum((y-f)**2)                #calculates sum of squares of residuals
        sstot = np.sum((y - ybar)**2)           #calculates total sum of squares
        R_squared = 1 - (ssres / sstot)         #calculates R^2 value
        if i == 0:
            R = [R_squared,1]
        else:
            if R_squared > R[0]:
                R = [R_squared,polylist[i]]

    '''
    Calculates polyfit for order of highest R^2 value.
    '''
    coeffs = np.polyfit(x,y,R[1])               
    p = np.poly1d(coeffs)
    x_vals = np.linspace(min(x),max(x),33)
    f = p(x_vals)
    return(x_vals,f,R,coeffs)

x = np.linspace(0,32,17)

y_HIC = [1.0,0.75,0.5,0.4,0.3,0.25,0.2,0.175,0.125,0.1,0.0875,0.06,0.045,0.03,0.015,-0.05,-0.10]
y_UMIC = [1.0,0.95,0.9,0.85,0.75,0.65,0.55,0.44,0.33,0.28,0.23,0.18,0.1275,0.0875,0.0667,0.046,-0.02]
y_LMIC = [1.0,1.1,1.25,1.1,0.95,0.8,0.75,0.7,0.6,0.5,0.4,0.35,0.3,0.25,0.1875,0.0975,0.0]
y_LIC = [1.0,1.3,1.5,1.7,1.45,1.2,1.05,0.9,0.75,0.65,0.55,0.45,0.35,0.3,0.2,0.1,0.05]

emissions_levels = [y_HIC,y_UMIC,y_LMIC,y_LIC]
label_list = ['Upper Income','Upper Middle Income','Lower Middle Income','Low Income']

plt.plot(x,y_HIC)
plt.plot(x,y_UMIC)
plt.plot(x,y_LMIC)
plt.plot(x,y_LIC)

updated_curve = []

plt.figure()
for i, val in enumerate(emissions_levels):
    x_new,y_new,R,coeffs = curve_fitter(x,val,5)
    updated_curve.append(y_new)
    plt.plot(x_new,y_new,label=label_list[i])
plt.show()