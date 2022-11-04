import math
from sympy import *
from bwrsNEW import _ZTCS_
def jsysjyl(_P_,_T_,_zf_,_Q_,n0,n,a0,a1,a2,nc):
    ZTCS = _ZTCS_(_P_, _T_, _zf_)
    _YSYZ_ = ZTCS[3]
    _KV_ = ZTCS[-3]
    _Q0_ = (_Q_*0.68/ZTCS[2]) * (n0 / n)
    H0 = a0 * (_Q0_/nc) ** 2 + a1 * (_Q0_/nc) + a2
    H = H0 * (n / n0) ** 2
    _Pc_ = ((H *9.8* (((_KV_ - 1)*ZTCS[0]/1000) / (_KV_ * _YSYZ_ * 8.314 * _T_)) + 1) ** (_KV_ / (_KV_ - 1))) * _P_
    return _Pc_,H
def jsysjwd(_T_, _Pc_,_Pj_,_zf_):
    ZTCS = _ZTCS_(_Pc_, _T_, _zf_)
    _KT_ = ZTCS[-2]
    _Tc_= _T_ * (_Pc_ / _Pj_) ** ((_KT_ - 1) / _KT_)
    return min(_Tc_,333)
def jisuanzhuansu(_Pj_,_Pc_,_Tj_,_zf_,_Q_, a0, a1, a2,n0,nc,_MD0_):
    ZTCS = _ZTCS_(_Pj_, _Tj_, _zf_)
    _KV_ = ZTCS[-3]
    _YSYZ_ = ZTCS[3]
    _hhxdfzzl_ = ZTCS[0]
    _MDj_ = ZTCS[2]
    b = (_KV_ - 1) / _KV_
    H = ((((_Pc_ / _Pj_) ** b) - 1) / b) * (1 / 9.8) * ((_YSYZ_ * 8.314 * _Tj_*1000) / _hhxdfzzl_)
    # X = n/n0
    # 0 = a2x**2+a1*Q*x+(a0*Q**2-H)
    a_ = a2
    b_ = a1 * (((_Q_ * _MD0_) / _MDj_) / nc)
    c_ = (a0 * (((_Q_ * _MD0_) / _MDj_) / nc) ** 2 - H)
    d_ = b_ ** 2 - 4 * a_ * c_
    if (d_ < 0):
        print("无解")
    else:
        e_ = math.sqrt(d_)
        x1 = ((-b_ + e_) / (2 * a_))  # 调用math模块中sqrt开平方函数
        x2 = ((-b_ - e_) / (2 * a_))
    if x1 > 0:
        n = x1 * n0
    else:
        n = x2 * n0
    return n
def jsysjgl(_Q_,n0,n,a0,a1,a2,b0,b1,b2,nc,_MD0_):
    _Q0_ = _Q_ * (n0 / n)
    H0 = a0 * (_Q0_ / nc) ** 2 + a1 * (_Q0_ / nc) + a2
    H = H0 * (n / n0) ** 2
    xl = b0*((_Q0_/nc) ** 2)+b1*(_Q0_/nc)+b2
    power = (H*(_Q_*_MD0_)*9.8)/(xl*0.95)
    return power
_P_ =7198041.17037009
_T_ =308.977423912863
_zf_=[97.5, 0, 0.2, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.6, 0.5, 0]
_Q_ =4550 * 10 ** 4 / (60 * 60 * 24)
n0 =9030
n =7000
a0 = -243.41
a1 = 684.18
a2 = 8677.2
nc =2
l=jsysjyl(_P_,_T_,_zf_,_Q_,n0,n,a0,a1,a2,nc)
print(l)
