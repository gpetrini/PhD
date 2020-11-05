import sympy as sp
from sympy import Eq, Symbol, symbols, pprint, latex

# Variables
R, pi, phi_0, phi_1, r, w = symbols('R pi phi_0 phi_1 r_m omega')

# Values

R_, pi_, phi_0_, phi_1_, r_, w_ = 0.7, 0.05, 0.025, 0.1, 0.01, 0.024

dict = {
    R :R_,
    pi:pi_,
    phi_0:phi_0_,
    phi_1:phi_1_,
    r:r_,
    w:w_
}

dk_dw = ((R-1)*(1+pi)*(phi_0*(1+pi) + phi_1*(pi-r)))/((R*((w+phi_0-1)*(1+pi) + phi_1*(pi-r)) + (1+pi)*(1-w))**2)
pprint(dk_dw)

dk_dw = dk_dw.subs(pi, 0).collect(w).simplify()
pprint(dk_dw)


dk_dw = dk_dw.subs(dict)
pprint(dk_dw)

dk_dr = (phi_1*(R-1)*(pi+1)*(w-1))/((R*(pi*w + pi*phi_0+ pi*phi_1 - pi + w + phi_0 - phi_1*r - 1) - pi*w + pi - w + 1)**2)
pprint(dk_dr)

dk_dr = dk_dr.subs(pi, 0).collect(w-1).simplify()
pprint(dk_dr)


dk_dr = dk_dr.subs(dict)
pprint(dk_dr)

dk_dp0 = (-(R-1)*(pi+1)**2*(w-1))/((R*(pi*w + pi*phi_0+ pi*phi_1- pi + w + phi_0- phi_1*r - 1) - pi*w + pi - w + 1)**2)
pprint(dk_dp0)

dk_dp0 = dk_dp0.subs(pi, 0).collect(-w+1).simplify()
pprint(dk_dp0)


dk_dp0 = dk_dp0.subs(dict)
pprint(dk_dp0)


dk_dpi = (-phi_1*(1-R)*(1-w)*(1+r))/((R*((1+pi)*(w + phi_0+ phi_1*r - 1) + phi_1*pi*(1-r)) + (-w+1)*(1+pi))**2)
pprint(dk_dpi)

dk_dpi = dk_dpi.collect(pi+1).collect(w-1).simplify()
pprint(dk_dpi)


dk_dpi = dk_dpi.subs(dict)
pprint(dk_dpi)
