import math
from sympy import *
from bwrsNEW import _ZTCS_
def jsyl(_Pj_,_T_, _zf_, _Q_, _BC_, _NJ_,_Ke_,_MD0_):#_P_pa, _M_kg/s, _BC_m, _NJ_m, _T_K, _Q_m³/s，0.6858901029747823标况下的密度
    ZTCS = _ZTCS_(_Pj_, _T_, _zf_)   #
    _YSYZ_ = ZTCS[3]
    hhxdfzzl = ZTCS[0]
    _Rg_ = (8.314/hhxdfzzl)*1000
    _Tpj_ = _T_
    _MCXS_ = (-1/(2*math.log10(_Ke_/3.7*_NJ_)))**2
    _M_ = _Q_*_MD0_
    _Pc_ = ((_Pj_ ** 2) - ((16 * (_M_**2) * _MCXS_ * _YSYZ_ * _Rg_ * _Tpj_ * _BC_) / ((math.pi ** 2) * (_NJ_ ** 5))))**(1/ 2)#Rg*1000单位(J/KG*K)
    Pc_=_Pc_
    return Pc_
def jswd(_Pj_,_Tj_,_zf_,_Q_, _Thj_,_D_,_ZCRXS_, _BC_,_ylc_,_MD0_): #温降公式 ylc压力差
    ZTCS = _ZTCS_(_Pj_, _Tj_, _zf_)
    _Cpp_ = ZTCS[-4]
    hhxdfzzl = ZTCS[0]
    _Cp_ = (_Cpp_/hhxdfzzl)*1000
    _Di_ = ZTCS[-1]*10**(-6)
    _MD_ = ZTCS[2]
    _M_ = _Q_ * _MD0_
    a = ((math.pi * _D_ * _ZCRXS_) / (_M_ * _Cp_)) * _BC_
    _Tc_= _Thj_ + (_Tj_ - _Thj_) * exp(-a) - _Di_ * ((_ylc_/a) * (1 - math.exp(-a)))
    return _Tc_
