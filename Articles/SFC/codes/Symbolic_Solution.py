base = model()
df = SolveSFC(base, time=1000)

base_eq = model()
SolveSFC(base_eq, time=1, table = False)
t = sp.Symbol('t')
initials = {
    key: base_eq.evaluate(key) for key in base_eq.parameters
}
initials.update({key: base_eq.evaluate(key) for key in base_eq.variables})

for i in base_eq.variables:
  globals()["_" + i] = sp.Function(i)
  
for i in base_eq.parameters:
  globals()[i] = sp.symbols(i, positive=True)
  globals()['infla'] = sp.symbols('infla')

Y = _C(t) + _I_t(t)
pprint(sp.Eq(_Y(t), Y))
C = _Cw(t) + _Ck(t)
pprint(sp.Eq(_C(t), C))
I = _I_f(t) + _I_h(t)
pprint(sp.Eq(_I_t(t), I))
Yk = _K_f(t)/v
pprint(sp.Eq(_Yk(t), Yk))
u = _Y(t)/_Yk(t)
pprint(sp.Eq(_u(t), u))
Z = _I_h(t)
pprint(sp.Eq(_Z(t), Z))
W = omega*_Y(t)
pprint(sp.Eq(_W(t), W))
K = _K_HD(t) + _K_f(t)
pprint(sp.Eq(_K(t), K))
Z = _Ck(t) + _I_h(t)
pprint(sp.Eq(_Z(t), Z))

Cw = alpha*_W(t)
pprint(sp.Eq(_Cw(t), Cw))
YDw = _W(t)
pprint(sp.Eq(_YDw(t), YDw))
S_hw = _YDk(t) - _Cw(t)
pprint(sp.Eq(_S_hw(t), S_hw))
NFW_hw = _S_hw(t)
pprint(sp.Eq(_NFW_hw(t), NFW_hw))

Ck = R*_Z(t)
pprint(sp.Eq(_Ck(t), Ck))
dLk = _Ck(t)
pprint(sp.Eq(_Lk(t) - _Lk(t-1), dLk))
YDk = _FD(t) + rm*_M_h(t-1) - _rmo(t)*_MO(t-1) - _rl(t)*_Lk(t-1)
pprint(sp.Eq(_YDk(t), YDk))
S_hk = _YDk(t) - _Ck(t)
pprint(sp.Eq(_S_hk(t), S_hk))
dMO = _I_h(t)
pprint(sp.Eq(_MO(t) - _MO(t-1), dMO))
dM_h = _S_hk(t) + (_Lk(t) - _Lk(t-1))
pprint(sp.Eq((_M_h(t) - _M_h(t-1)), dM_h))
V_h = _M_h(t) + _K_HD(t)*_ph(t) - _MO(t) - _Lk(t)
pprint(sp.Eq(_V_h(t), V_h))
V_hr = _M_h(t) + _K_HD(t) - _MO(t) - _Lk(t)
pprint(sp.Eq(_V_hr(t), V_hr))
NFW_h = _S_hk(t) - _I_h(t)
pprint(sp.Eq(_NFW_h(t), NFW_h))
M_h = _S_hk(t) + (_Lk(t) - _Lk(t-1))
pprint(sp.Eq(_M_h(t), M_h))

I_f = _h(t)*_Y(t)
pprint(sp.Eq(_I_f(t), I_f))
dK_f = _I_f(t)
pprint(sp.Eq(_K_f(t) - _K_f(t-1), dK_f))
Lf = _I_f(t) - _FU(t) + _Lf(t-1)
pprint(sp.Eq(_Lf(t), Lf))
FT = _FU(t) + _FD(t)
pprint(sp.Eq(_FT(t), FT))
FU = gamma_F*(_FT(t) - _rl(t)*_Lf(t-1))
pprint(sp.Eq(_FU(t), FU))
FD = (1 - gamma_F)*(_FT(t) - _rl(t)*_Lf(t-1))
pprint(sp.Eq(_FD(t), FD))
h = _h(t-1)*gamma_u*(_u(t)-un) + _h(t-1)
pprint(sp.Eq(_h(t), h))
NFW_f = _FU(t) - _I_f(t)
pprint(sp.Eq(_NFW_f(t), NFW_f))
V_f = _K_f(t) - _Lf(t)
pprint(sp.Eq(_V_f(t), V_f))

L = _Lf(t) + _Lk(t)
pprint(sp.Eq(_L(t), L))
M = (_L(t) - _L(t-1)) + (_MO(t) - _MO(t-1)) + _M(t-1)
pprint(sp.Eq(_M(t), M))
rmo = (1+ spread_mo)*rm
pprint(sp.Eq(_rmo(t), rmo))
rl = (1+ spread_l)*rm
pprint(sp.Eq(_rl(t), rl))
V_b = _L(t) + _MO(t) - _M(t)
pprint(sp.Eq(_V_b(t), V_b))
NFW_b = _rl(t)*_L(t-1) + _rmo(t)*_MO(t-1) - rm*_M(t-1)
pprint(sp.Eq(_NFW_b(t), NFW_b))

_own = sp.Function('own')

K_HS = _K_HD(t)
pprint(sp.Eq(_K_HS(t), K_HS))
Is = _I_h(t)
pprint(sp.Eq(_Is(t), Is))
dK_HD = _I_h(t)
pprint(sp.Eq(_K_HD(t) - _K_HD(t-1), dK_HD))
I_h = (1+_g_Z(t))*_I_h(t-1)
pprint(sp.Eq(_I_h(t), I_h))
K_k = _K_HD(t)/(_K(t))
pprint(sp.Eq(_K_k(t), K_k))
ph = (1+infla)*_ph(t-1)
pprint(sp.Eq(_ph(t), ph))
own = ((1+_rmo(t))/(1+infla))-1
pprint(sp.Eq(_own(t), own))
g_Z = phi_0 - phi_1*_own(t)
pprint(sp.Eq(_g_Z(t), g_Z))
