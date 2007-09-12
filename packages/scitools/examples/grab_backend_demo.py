#!/usr/bin/env python

"""
Demonstration on how to grab the backend after some Easyviz commands
and add some backend specific commands. The example is based on the
legend_demo.py file from Matplotlib.
"""

from scitools.all import *

a = linspace(0,3,150)
b = linspace(0,3,150)
c = exp(a)
d = c.tolist()
d.reverse()
d = array(d)

setp(interactive=False)
plot(a,c,'k--',a,d,'k:',a,c+d,'k')
legend('Model length', 'Data length', 'Total message length')
ylim([-1,20])
xlabel('Model complexity --->')
ylabel('Message length --->')
title('Minimum Message Length')
show()

print "Let us now tune the plot by grabbing the backend."
raw_input('press enter to continue')

# Grab the backend and fine tune the plot:
g = get_backend()
if backend == 'matplotlib':
    ax = g.gca()
    # Remove tick labels:
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    # The arrows in the x and y labels does not look good. Here we use
    # some LaTeX arrows instead:
    ax.set_xlabel(r'Model complexity $\longrightarrow$')
    ax.set_ylabel(r'Message length $\longrightarrow$')
    # Change legend box location:
    l = ax.get_legend()
    l._loc = 9  # upper center (is there a better way to set location?)
    # Add shadow to legend box:
    l.shadow = True
    g.draw()
elif backend == 'gnuplot':
    # Remove tick labels:
    g('set xtics ("" 0, "" 0.5, "" 1, "" 1.5, "" 2, "" 2.5, "" 3)')
    g('set ytics ("" 0, "" 5, "" 10, "" 15, "" 20)')
    # Change location of legends:
    g('set key top center')
    # Create a box around the legends:
    g('set key box lt -1 lw 1 height 1 width 1')
    # Make the axes frame nice and thick:
    g('set border 1+2+4+8+16 linetype -1 linewidth 2')
    g.replot()
elif backend == 'veusz':
    # Remove tick labels:
    g.Set('/page1/graph1/x/TickLabels/hide', True)
    g.Set('/page1/graph1/y/TickLabels/hide', True)
    # Turn off minor tick marks:
    g.Set('/page1/graph1/x/MinorTicks/hide', True)
    g.Set('/page1/graph1/y/MinorTicks/hide', True)
    # Change legend box location:
    g.Set('/page1/graph1/key1/horzPosn', 'centre')
    g.Set('/page1/graph1/key1/vertPosn', 'top')
    # Adjust the placement of the title:
    g.Set('/page1/graph1/label1/xPos', 0.3)
    g.Set('/page1/graph1/label1/yPos', 1.02)
    g.window.showNormal()
    # We could also have done the changes interactively by saving the
    # session to a native Veusz file (.vsz) and open the file in Veusz:
    #save('tmp1.vsz')
    #os.system('veusz tmp1.vsz')
elif backend == 'grace':
    # In Grace we can do the changes interactively in the GUI.
    pass
elif backend == 'matlab':
    # Remove tick labels:
    g.set_(g.gca(), 'XTickLabel', [], 'YTickLabel', [], nout=0)
    # Change legend location:
    h = g.findobj('Tag', 'legend', nout=1)  # find the legend handle
    g.set_(h, 'Location', 'North', nout=0)
elif backend == 'matlab2':
    s = get_script()
    # Remove tick labels:
    s += "set(gca, 'XTickLabel', [], 'YTickLabel', [])\n"
    # Change legend location:
    s += "set(findobj('Tag', 'legend'), 'Location', 'North')\n"
    # Save the Matlab commands to a Matlab .m file:
    save('tmp1.m')
    # We can now open this file in Matlab (if Matlab is available):
    #os.system('matlab -r tmp1')
elif backend == 'pyx':
    # There is currently no way to change properties in the PyX backend
    # afterwards. It is only possible to add new stuff.
    pass
elif backend == 'blt':
    pass

print "Now we store a hardcopy of the tuned plot."
raw_input('press enter to continue')

#hardcopy('grab_backend1.eps')  # Will destroy all changes!
#hardcopy('grab_backend1.png')  # Will destroy all changes!

# Since we have made changes in the backend directly, a call to hardcopy in
# Easyviz would normally destroy all these changes. However, setting the
# keyword argument replot to False in the hardcopy function will make sure
# that the changes is not destroyed:
if backend == 'gnuplot':
    # Unfortunately, setting replot to False does not currently work in the
    # Gnuplot backend. So, in this case we must use the hardcopy command from
    # the Gnuplot.py module:
    g.hardcopy(filename='grab_backend1.eps', terminal='postscript', mode='eps')
    g.hardcopy(filename='grab_backend1.png', terminal='png')
else:
    hardcopy('grab_backend1.eps', replot=False)
    if not backend == 'pyx':
        hardcopy('grab_backend1.png', replot=False)
