#! /usr/bin/env python3
"""Dieses Programm fuehrt ein chi**2 Fit durch.
"""
import sys
import argparse

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize

##_Modify your Plot_##

# NOTICE: Do always read foreign code before exectuing! You can never know what some nasty people wrote in the code...
# Just cause this version is simpler to modify doesn't mean that you don't need to understand whats happening!

#Change the string following text to set yout plot labels 
#Warning: Make sure to keep the "%-Arguments" like %.2f untouched by changing you text!

#Set your Axis Labels
#Set an empty string "" to not show that option
plot_title = "MyPlot.pdf"

y_label = "y_change_me"
x_label = "x_change_me"

vals_legend = r"Meassured Values"
fit_lengend = r"Fitted Graph"

#Set Chi-Formula (TeX-natation)
chi_formula = "$\chi^2=\sum\\frac{(y_i-f(x_i,\\vec{a}))^2}{s_i^2}=%.2f$"

#Set your Function Name
func_name = "$f(x)=%.2f x"

#Set Name of your Graphs parameters
first_param = "$a = %.2f"
second_param =  "b = %.2f"

#Please visit the matplotlib documentation for more options on the following parameters
#You might need some tries to figure the perfect positions out

#Set Color and format of your graphs
#Color of the dots that represent your values
val_color = 'r.'
fit_color = "g"

#Set fontsizes of formulas in the plot (simply a number)
y_size = 16
x_size = 16

chi_size = 15
fx_size = 15
a_b_size = 15

#Positions
#Position of the label
pos_legend = "upper left"

#Precise positioning of the Formulas
#Please remember control-z for undo changes

chi_x_anker = 0.95
fx_x_anker = 0.95
a_b_x_anker = 0.95

chi_y_anker = 0.25
fx_y_anker = 0.15
a_b_y_anker = 0.05

#Positions of Formulas (vertical)
chi_vert = "bottom"
fx_vert = "bottom"
a_b_vert = "bottom"

#Positions of Formulas (horizontal)
chi_hor = "right"
fx_hor = "right"
a_b_hor = "right"

#resolution
plt_size = 300

#Want the old Version without input file? - Scroll down to "##__For old Version commment out from here__##" and comment out
#to "##__until here__##". The old input code is right below that message. All other features should still work.


# Deklariere eine neue Funktion
def f(x,a,b):
    return a*x + b

def chi2(x, y, s, f, a, b):
    chi = (y - f(x,a,b))/s
    return np.sum(chi**2)

##__For old Version commment out from here__##
# Fileinput like in chi2FitXYErr.py
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
DESCRIPTION:
  This Script is a modified version of "chi2Fit.py"

  Input is a file (command line option -i) with five columns:
  x, error_x, y, error_y, sigma

  Column 2 is ignored, this is needed for chi2FitXYErr.py.
  You can put any random number at this columns.

  The input file may contaion comment lines starting with a hash (#).


EXAMPLES:

  - ./chi2Fit.py -i my_values.txt
    Fits a line to the data in 'my_values.txt' and print the fit results to
    screen
  
  - ./chi2Fit.py -i dataxy.txt -o ergebnis.png
    The same as above. In addition, data points and best-fit line
    are shown in the plot 'result.png'.

AUTHOR:
    Unknown & Thomas Erben (terben@astro.uni-bonn.de)
    Modified/Forked by Chris
"""
)
parser.add_argument('-i', '--input_file', nargs=1,
                    required=True, help='Name der Datendatei')
parser.add_argument('-o', '--output_file', nargs=1,
                    help='Name des Ausgabeplots (OPTIONAL)')

args = parser.parse_args()

input_file = args.input_file[0]

# Read data:
data = np.loadtxt(input_file)

# Give meaningful variable names to input data columns:
xdata = data[:,0]
ydata = data[:,2]
sigma = data[:,3]

##__until here__##

##comment in those three lines below and enter your values

# Ihre Messdaten kommen hier hin
#xdata = np.array([0.0,1.0,2.0,3.0,4.0,5.0])
#ydata = np.array([1.1,1.3,2.1,2.7,2.8,3.6])
#sigma = np.array([0.2,0.25,0.3,0.35,0.4,0.45])

# Startwerte fuer die Parameterbestimmung
x0    = np.array([1.0, 0.0])

# Die lineare Regression, so wie in den vorigen Beispielen behandelt,
# beruecksichtigt die Messungenauigkeiten weder fuer die richtige
# Gewichtung der einzelnen Messungen (falls die unterschiedlichen
# Messungen ueber unterschiedliche Unsicherheiten verfuegen), noch
# gehen diese Unsicherheiten direkt in die Abschaetzung der
# Unsicherheit der angepassten Parameter ein.

# Desweiteren ist die lineare Regression auf Modelle beschraenkt, in
# die alle zu bestimmenden Parameter *linear* eingehen. Dies ist
# natuerlich nicht allgemein gegeben. Ein chi2-Fit ist ein Spezialfall
# einer Optimierung mittels der Maximum Likelihood Methode, welche im
# Fall von linearen Abhaengigkeiten der Observablen *um das Minimum
# herum* (aber nicht notwendigerweie ueberall) und im Fall von
# gaussischen Messungenauigkeiten fuer alle Anpassungen angewendet
# werden kann, also auch im Fall unterschiedlicher sigma fuer jede
# Einzelmessung. Auch dafuer gibt es ein Modul in Pyhton. In diesem
# Modul koennen Sie nun *beliebige* Funktionen fitten, also auch
# solche, die nicht nur Parameter linear, sondern in beliebiger
# analytischer oder numerischer Form enthalten.
# Please see the documentation of the curve_fit function for more information:
# 
fitParams, fitCovariances = optimize.curve_fit(f, xdata, ydata, sigma=sigma,
                                               absolute_sigma=True)

# give meaningful names to the results:
slope = fitParams[0]
intercept = fitParams[1]
fitErrors = np.sqrt(np.diag(fitCovariances))
slope_std_err = fitErrors[0]
intercept_std_err = fitErrors[1]

# print result to screen:
print("result of fit:\n")
print("y = a * x + b with")
print("a = %f +/- %f" % (slope, slope_std_err))
print("b = %f +/- %f" % (intercept, intercept_std_err))

# Das ist die wichtigste Lektion in diesem Teil: Vorgefertigter Code
# oder komplette Black-Box-Programme wie Excel sind fuer bestimmte
# Sachen nuetzlich.
# ABER: Es ist nicht immer klar, was dieses Programm/Code genau macht!
# Hier macht curve_fit ganz offensichtlich NICHT, was wir wollen. Und
# wir haetten das auch nicht unbedingt gemerkt! GENAU deshalb sollen
# Sie Rechnungen immer transparent ausfuehren und NIE mit schlecht
# dokumentiertem closed-source black-box Code!


# nun erschaffen wir einen plot
fig = plt.figure()
ax = fig.add_subplot(111)

# Vielleicht wollen Sie noch etwas in den Plot schreiben, z.B. eine Formel?
#f(x)-line
formulaText1 = func_name % slope 
formulaText2 = '+ %.2f$' % intercept
formulaText  = formulaText1 + formulaText2
ax.text(fx_x_anker, fx_y_anker, formulaText, verticalalignment=fx_vert, horizontalalignment= fx_hor, transform=ax.transAxes, fontsize=fx_size)

#a-line
formulaText3 = first_param % slope
formulaText4 = '\pm %.2f' % slope_std_err
formulaTextS = formulaText3 + formulaText4

#b-line
formulaText5 = ",\,\," + second_param % intercept
formulaText6 = '\pm %.2f$' % intercept_std_err
formulaTextI = formulaText5 + formulaText6

#adding a- and b-line
formulaTextErrors = formulaTextS + formulaTextI
ax.text(a_b_x_anker, a_b_y_anker, formulaTextErrors, verticalalignment=a_b_vert, horizontalalignment= a_b_hor, transform=ax.transAxes, fontsize=a_b_size)

#Parts of the follwing text is defined obove 
#Chi_Formula shown in plot image
#formulaTextChi2 = chi_formula % thischi2
#ax.text(chi_x_anker, chi_y_anker, formulaTextChi2, verticalalignment=chi_vert, horizontalalignment= chi_hor, transform=ax.transAxes, fontsize=chi_size)

#title of the plot
plt.title(plot_title)

# Die Achsen brauchen eine Beschriftung
plt.ylabel(y_label, fontsize = y_size)
plt.xlabel(x_label, fontsize = x_size)
plt.xlim(xdata[0]-1,xdata[-1]+1)

# Plotte die Funktion 
t = np.arange(xdata[0]-0.5,xdata[-1]+0.5, 0.02)
plt.plot(t,f(t,slope,intercept), fit_color,label=fit_lengend)
plt.errorbar(xdata, ydata, sigma, fmt=val_color, label=vals_legend)
#creating legend
plt.legend()


#checking for output name and saving plot
if args.output_file != None:
  plotname = args.output_file[0]
  plt.savefig(plotname, bbox_inches=0, dpi=plt_size)
  error_output = False
#if no output name is given, an error will be triggered at the end
else:
	error_output = True
# Zeige den Plot

plt.show()

# Raising an error, if no output name was given
if error_output == True:
	raise Exception(
'''
No output filename name was given, nothing will be saved!
To change that by adding a filename with -o to your command
e.g. [your previous command] -o new-plot 
If this was intended, just ignore that error'''
)