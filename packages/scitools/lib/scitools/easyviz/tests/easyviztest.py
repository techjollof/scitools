import unittest
import time

from scitools.numpytools import *
from scitools.easyviz import *

import random

hardcopy_counter = 0
psplot = False
prompt = ''
pause = 0.2
clear_figure = False
new_figure = True
screenplot = True
setp(show=screenplot)

def next(clear_figure=False, prompt='', pause=0,
         save_hardcopy=False, new_figure=False):
    if save_hardcopy:
        global hardcopy_counter
        hardcopy('tmp_easyviz_plot%03d.eps' % hardcopy_counter, color=True)
        hardcopy_counter += 1
    if prompt:
        raw_input(prompt)
    if pause:
        time.sleep(pause)
    if clear_figure:
        clf()
    if new_figure:
        figure()
        
n = lambda: next(clear_figure, prompt, pause, psplot, new_figure)


class EasyvizTestCase(unittest.TestCase):
    def get_line_data(self, n=41):
        x = linspace(0, 15, n)
        y = sin(x)*x
        v = sin(x)*sqrt(x)
        w = sin(x)*x**0.33333333
        return x, y, v, w

    def get_format_string_data(self):
        colors = Line._colors
        try: colors.remove('w')  # remove white
        except: pass
        markers = Line._markers
        linestyles = Line._linestyles
        format = []
        for marker in markers:
            format.append(''.join([random.choice(colors), marker,
                                   random.choice(linestyles)]))
        return format
    
    def get_2D_data(self, n=21, sparse=True, memoryorder='yxz'):
        x = y = linspace(-3,3,n)
        xv, yv = meshgrid(x, y, sparse=sparse, memoryorder=memoryorder)
        values = peaks(xv, yv)
        return x, y, xv, yv, values

    def get_3D_data(self, sparse=True, memoryorder='yxz'):
        x = y = z = linspace(-3,3,13)
        xv, yv, zv = meshgrid(x, y, z, sparse=sparse, memoryorder=memoryorder)
        values = xv**exp(-xv**2-yv**2-zv**2)
        return x, y, z, xv, yv, zv, values

    def get_2D_vector_data(self, n=13, sparse=True, memoryorder='yxz'):
        x = y = linspace(-2,2,n)
        xv, yv = meshgrid(x, y, sparse=sparse, memoryorder=memoryorder)
        values = xv*exp(-xv**2-yv**2)
        uv, vv = gradient(values)
        return x, y, xv, yv, values, uv, vv

    def get_3D_vector_data(self, sparse=True, memoryorder='yxz'):
        x = y = z = linspace(-3,3,13)
        xv, yv, zv = meshgrid(x, y, z, sparse=sparse, memoryorder=memoryorder)
        values = xv**exp(-xv**2-yv**2-zv**2)
        
        return x, y, z, xv, yv, zv, values
        