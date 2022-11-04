import math
from bwrsNEW import _ZTCS_
from guandao import jsyl    #计算管道压力
from guandao import jswd    #计算管道温度
from yasuoji import jsysjwd #计算压缩机出口温度
from yasuoji import jsysjyl #计算压缩机出口压力
from yasuoji import jisuanzhuansu   #计算压缩机转速
from yasuoji import jsysjgl
R=8.3143
_zf_=[97.5, 0, 0.2, 0, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.6, 0.5, 0]   #组分列表
ZCRXS=1.15#总传热系数
Thj= 298#环境温度
NJ=0.9812#内径
D=1.016 #外径
LP0=[10000000]  #第1个管道起点压力
LP1=[10000000]  #第2个管道起点压力
LP2=[10000000]  #第3个管道起点压力
LP3=[10000000]  #第4个管道起点压力
LP4=[9500000]   #第5个管道起点压力
_LP50_=0
LP5=[_LP50_]    #第6个管道起点压力
_LP60_=0
LP6=[_LP60_]    #第7个管道起点压力
LT0=[333]   #第1个管道起点温度
LT1=[]  #第2个管道温度列表
LT2=[]  #第3个管道温度列表
LT3=[]  #第4个管道温度列表
LT4=[]  #第5个管道温度列表
LT5=[0] #第6个管道温度列表
LT6=[0] #第7个管道温度列表
zs=[]   #转速
power = []  #功率
FQ1 =126.51 #分气点1分出流量
FQ2 = 126.51    #分气点2分出流量
FQ3 = 253.02    #分气点3分出流量
ZQ1 = 506.04    #注气点1分出流量
ZTCS0=_ZTCS_(101325, 293.15, _zf_)
_MD0_=ZTCS0[2]  #工程标况下状态参数
nmax = 9030 #最大转速
for i in range(0, 94):
    if i < 16:
        #计算管道压力温度
        _Q_ = 4550*10**4/(60*60*24) #第一管段流量
        _Pj_ = LP0[-1]  #起点压力
        _Tj_ = LT0[-1]  #起点温度
        ZTCS = _ZTCS_(_Pj_, _Tj_, _zf_) #起点温度压力下的状态参数
        _BC_ = 10000    #管段1步长
        _NJ_ = NJ   #管段1内径
        _Ke_ = 0.017*10**(-3)   #相对粗糙度
        _Pc_ = jsyl(_Pj_, _Tj_, _zf_, _Q_, _BC_, _NJ_,_Ke_,_MD0_)   #终点压力
        LP0.append(_Pc_)    #添加到管段1得压力列表中
        _Tj_ = LT0[-1]  #进点温度=起点温度=上一个得终点温度
        _Thj_ = Thj #环境温度
        _Pj_ = LP0[-1]  ##进点压力=起点压力=上一个得终点压力
        _D_ = D #外径
        _ZCRXS_ = ZCRXS #总传热系数
        _ylc_ = LP0[-2] - LP0[-1]   #管段压力差=上一个管段起点压力-终点压力
        Tc = jswd(_Pj_,_Tj_,_zf_,_Q_, _Thj_,_D_,_ZCRXS_, _BC_,_ylc_,_MD0_)  # _Tj_进口温度K, _Thj_环境温度K, _D_管径m, _Q_体积流量m³/s, _Di_焦汤系数K/Pa, _ZCRXS_总传热系数, _Cp_高压定压比热J/Kg*K, _BC_步长m, _ylc_压力差用Pa
        LT0.append(Tc)  #添加出口温度到管段1得温度列表
        continue
        #压缩机
    elif i >= 16 and i <= 16:
        # 计算转速
        a0 = -243.41
        a1 = 684.18
        a2 = 8677.2
        n0 = 9030   #额定转速
        nc = 2  #压缩机台数




        _Pj_ = LP0[-1]  #压缩机进口压力=管段1最终点压力
        _Q_ = 4550 * 10 ** 4 / (60 * 60 * 24)   #进口流量
        _Pc_ = LP1[0]   #出口压力=管段2得起点压力
        _Tj_ = LT0[-1]  #压缩机进口温度=管段1最终点温度
        _n_ = jisuanzhuansu(_Pj_, _Pc_, _Tj_, _zf_, _Q_, a0, a1, a2, n0, nc,_MD0_)#_MD0_标况下密度
        n = min(_n_,nmax)   #取压缩机转速
        zs.append(n)    #将压缩机转速添加
        if _n_>nmax:    #如果算出来得实际转速>额定转速，也就是出口压力达不到设计压力，得重新计算出口压力
            _Pc_ = jsysjyl(_Pj_,_Tj_,_zf_,_Q_,n0,_n_,a0,a1,a2,nc)
            LP1[0] = _Pc_   #压缩机出口压力为下一个管段起点压力
        # 计算功率
        b0 = -2.38
        b1 = 18.96
        b2 = 47.72
        _power_ = jsysjgl(_Q_, n0, n, a0, a1, a2, b0, b1, b2, nc,_MD0_)
        power.append(_power_)
        #计算温度
        _Tysjj_ = LT0[-1]   #压缩机进口温度
        _Pysjc_ = LP1[0]    #压缩机出口压力
        _Pysjj_ = LP0[-1]   ##压缩机进口压力
        Tysjc = jsysjwd(_Tysjj_, _Pysjc_, _Pysjj_, _zf_)    #压缩机出口温度
        LT1.append(Tysjc)   #压缩机出口温度为下一个管段起点温度
    elif 16 < i < 33:
        _Q_ = 4550 * 10 ** 4 / (60 * 60 * 24)
        _Pj_ = LP1[-1]
        _Tj_ = LT1[-1]
        ZTCS = _ZTCS_(_Pj_, _Tj_, _zf_)
        _BC_ = 10000
        _NJ_ = NJ
        _Ke_ = 0.017 * 10 ** (-3)
        _Pc_ = jsyl(_Pj_, _Tj_, _zf_, _Q_, _BC_, _NJ_, _Ke_,_MD0_)
        LP1.append(_Pc_)
        _Tj_ = LT1[-1]
        _Thj_ = Thj
        _Pj_ = LP1[-1]
        _D_ = D
        _ZCRXS_ = ZCRXS
        _ylc_ = LP1[-2] - LP1[-1]
        Tc = jswd(_Pj_, _Tj_, _zf_, _Q_, _Thj_, _D_, _ZCRXS_, _BC_,
                  _ylc_,_MD0_)  # _Tj_进口温度, _Thj_环境温度, _D_管径, _M_质量流量, _Di_焦汤系数, _ZCRXS_总传热系数, _Cpp_高压定压比热, _BC_步长, _ylc_压力差用yali[-1]-yali[-2]表示
        LT1.append(Tc)
        continue
    elif i >= 33 and i <= 33:
        # 计算转速
        a0 = -243.41
        a1 = 684.18
        a2 = 8677.2
        n0 = 9030
        nc = 2
        _Pj_ = LP1[-1]
        _Pc_ = LP2[0]
        _Tj_ = LT1[-1]
        _Q_ = 4550 * 10 ** 4 / (60 * 60 * 24)
        _n_ = jisuanzhuansu(_Pj_, _Pc_, _Tj_, _zf_, _Q_, a0, a1, a2, n0, nc, _MD0_)
        n = min(_n_, nmax)
        zs.append(n)
        if _n_>nmax:
            _Pc_ = jsysjyl(_Pj_,_Tj_,_zf_,_Q_,n0,_n_,a0,a1,a2,nc)
            LP2[0] = _Pc_
        # 计算功率
        b0 = -2.38
        b1 = 18.96
        b2 = 47.72
        _power_ = jsysjgl(_Q_, n0, n, a0, a1, a2, b0, b1, b2, nc,_MD0_)
        power.append(_power_)
        # 计算温度
        _Tysjj_ = LT1[-1]
        _Pysjc_ = LP2[0]
        _Pysjj_ = LP1[-1]
        Tysjc = jsysjwd(_Tysjj_, _Pysjc_, _Pysjj_, _zf_)
        LT2.append(Tysjc)
    elif 33 < i < 50:
        _Q_ = 4550 * 10 ** 4 / (60 * 60 * 24)
        _Pj_ = LP2[-1]
        _Tj_ = LT2[-1]
        ZTCS = _ZTCS_(_Pj_, _Tj_, _zf_)
        _BC_ = 10000
        _NJ_ = NJ
        _Ke_ = 0.017 * 10 ** (-3)
        _Pc_ = jsyl(_Pj_, _Tj_, _zf_, _Q_, _BC_, _NJ_, _Ke_,_MD0_)
        LP2.append(_Pc_)
        _Tj_ = LT2[-1]
        _Thj_ = Thj
        _Pj_ = LP2[-1]
        _D_ = D
        _ZCRXS_ = ZCRXS
        _ylc_ = LP2[-2] - LP2[-1]
        Tc = jswd(_Pj_, _Tj_, _zf_, _Q_, _Thj_, _D_, _ZCRXS_, _BC_,
                  _ylc_,_MD0_)  # _Tj_进口温度, _Thj_环境温度, _D_管径, _M_质量流量, _Di_焦汤系数, _ZCRXS_总传热系数, _Cpp_高压定压比热, _BC_步长, _ylc_压力差用yali[-1]-yali[-2]表示
        LT2.append(Tc)
        continue
    elif i >= 50 and i <= 50:
        # 计算转速
        a0 = -243.41
        a1 = 684.18
        a2 = 8677.2
        n0 = 9030
        nc = 2
        _Pj_ = LP2[-1]
        _Pc_ = LP3[0]
        _Tj_ = LT2[-1]
        _Q_ = (4550 - FQ1) * 10 ** 4 / (60 * 60 * 24)
        _n_ = jisuanzhuansu(_Pj_, _Pc_, _Tj_, _zf_, _Q_, a0, a1, a2, n0, nc, _MD0_)
        n = min(_n_, nmax)
        zs.append(n)
        if _n_>nmax:
            _Pc_ = jsysjyl(_Pj_,_Tj_,_zf_,_Q_,n0,_n_,a0,a1,a2,nc)
            LP3[0] = _Pc_
        # 计算功率
        b0 = -2.38
        b1 = 18.96
        b2 = 47.72
        _power_ = jsysjgl(_Q_, n0, n, a0, a1, a2, b0, b1, b2, nc,_MD0_)
        power.append(_power_)
        # 计算温度
        _Tysjj_ = LT2[-1]
        _Pysjc_ = LP3[0]
        _Pysjj_ = LP2[-1]
        Tysjc = jsysjwd(_Tysjj_, _Pysjc_, _Pysjj_, _zf_)
        LT3.append(Tysjc)
    elif 50 < i < 67:
        _Q_ = (4550-FQ1) * 10 ** 4 / (60 * 60 * 24)
        _Pj_ = LP3[-1]
        _Tj_ = LT3[-1]
        ZTCS = _ZTCS_(_Pj_, _Tj_, _zf_)
        _BC_ = 10000
        _NJ_ = NJ
        _Ke_ = 0.017 * 10 ** (-3)
        _Pc_ = jsyl(_Pj_, _Tj_, _zf_, _Q_, _BC_, _NJ_, _Ke_,_MD0_)
        LP3.append(_Pc_)
        _Tj_ = LT3[-1]
        _Thj_ = Thj
        _Pj_ = LP3[-1]
        _D_ = D
        _ZCRXS_ = ZCRXS
        _ylc_ = LP3[-2] - LP3[-1]
        Tc = jswd(_Pj_, _Tj_, _zf_, _Q_, _Thj_, _D_, _ZCRXS_, _BC_,
                  _ylc_,_MD0_)  # _Tj_进口温度, _Thj_环境温度, _D_管径, _M_质量流量, _Di_焦汤系数, _ZCRXS_总传热系数, _Cpp_高压定压比热, _BC_步长, _ylc_压力差用yali[-1]-yali[-2]表示
        LT3.append(Tc)
    #最后一个压气站，注意出站压力不是设计压力
    elif i >= 67 and i <= 67:
        # 计算转速
        a0 = -243.41
        a1 = 684.18
        a2 = 8677.2
        n0 = 9030
        nc = 2
        _Pj_ = LP3[-1]
        _Pc_ = LP4[0]
        _Tj_ = LT3[-1]
        _Q_ = (4550 - FQ1 - FQ2) * 10 ** 4 / (60 * 60 * 24)
        _n_ = jisuanzhuansu(_Pj_, _Pc_, _Tj_, _zf_, _Q_, a0, a1, a2, n0, nc, _MD0_)
        n = min(_n_, nmax)
        zs.append(n)
        if _n_>nmax:
            _Pc_ = jsysjyl(_Pj_,_Tj_,_zf_,_Q_,n0,_n_,a0,a1,a2,nc)
            LP4[0] = _Pc_
        # 计算功率
        b0 = -2.38
        b1 = 18.96
        b2 = 47.72
        _power_ = jsysjgl(_Q_, n0, n, a0, a1, a2, b0, b1, b2, nc,_MD0_)
        power.append(_power_)
        # 计算温度
        _Tysjj_ = LT3[-1]
        _Pysjc_ = LP4[0]
        _Pysjj_ = LP3[-1]
        Tysjc = jsysjwd(_Tysjj_, _Pysjc_, _Pysjj_, _zf_)
        LT4.append(Tysjc)
    elif 67 < i < 78:
        _Q_ = (4550 - FQ1-FQ2) * 10 ** 4 / (60 * 60 * 24)
        _Pj_ = LP4[-1]
        _Tj_ = LT4[-1]
        ZTCS = _ZTCS_(_Pj_, _Tj_, _zf_)
        _BC_ = 10000
        _NJ_ = NJ
        _Ke_ = 0.017 * 10 ** (-3)
        _Pc_ = jsyl(_Pj_, _Tj_, _zf_, _Q_, _BC_, _NJ_, _Ke_,_MD0_)
        LP4.append(_Pc_)
        _Tj_ = LT4[-1]
        _Thj_ = Thj
        _Pj_ = LP4[-1]
        _D_ = D
        _ZCRXS_ = ZCRXS
        _ylc_ = LP4[-2] - LP4[-1]
        Tc = jswd(_Pj_, _Tj_, _zf_, _Q_, _Thj_, _D_, _ZCRXS_, _BC_,
                  _ylc_,_MD0_)  # _Tj_进口温度, _Thj_环境温度, _D_管径, _M_质量流量, _Di_焦汤系数, _ZCRXS_总传热系数, _Cpp_高压定压比热, _BC_步长, _ylc_压力差用yali[-1]-yali[-2]表示
        LT4.append(Tc)
        continue
    elif 78 < i < 86:
        _Q_ = (4550 - FQ1 - FQ2-FQ3) * 10 ** 4 / (60 * 60 * 24)
        LP5[0] = LP4[-1]
        _Pj_ = LP5[-1]
        LT5[0] = LT4[-1]
        _Tj_ = LT5[-1]
        ZTCS = _ZTCS_(_Pj_, _Tj_, _zf_)
        _BC_ = 10000
        _NJ_ = NJ
        _Ke_ = 0.017 * 10 ** (-3)
        _Pc_ = jsyl(_Pj_, _Tj_, _zf_, _Q_, _BC_, _NJ_, _Ke_,_MD0_)
        LP5.append(_Pc_)
        _Tj_ = LT5[-1]
        _Thj_ = Thj
        _Pj_ = LP5[-1]
        _D_ = D
        _ZCRXS_ = ZCRXS
        _ylc_ = LP5[-2] - LP5[-1]
        Tc = jswd(_Pj_, _Tj_, _zf_, _Q_, _Thj_, _D_, _ZCRXS_, _BC_,
                  _ylc_,_MD0_)  # _Tj_进口温度, _Thj_环境温度, _D_管径, _M_质量流量, _Di_焦汤系数, _ZCRXS_总传热系数, _Cpp_高压定压比热, _BC_步长, _ylc_压力差用yali[-1]-yali[-2]表示
        LT5.append(Tc)
    elif 86 < i < 94:
        _Q_ = (4550 - FQ1 - FQ2 - FQ3+ZQ1) * 10 ** 4 / (60 * 60 * 24)
        LP6[0] = LP5[-1]
        _Pj_ = LP6[-1]
        LT6[0] = LT5[-1]
        _Tj_ = LT6[-1]
        ZTCS = _ZTCS_(_Pj_, _Tj_, _zf_)
        _BC_ = 10000
        _NJ_ = NJ
        _Ke_ = 0.017 * 10 ** (-3)
        _Pc_ = jsyl(_Pj_, _Tj_, _zf_, _Q_, _BC_, _NJ_, _Ke_,_MD0_)
        LP6.append(_Pc_)
        _Tj_ = LT6[-1]
        _Thj_ = Thj
        _Pj_ = LP6[-1]
        _D_ = D
        _ZCRXS_ = ZCRXS
        _ylc_ = LP6[-2] - LP6[-1]
        Tc = jswd(_Pj_, _Tj_, _zf_, _Q_, _Thj_, _D_, _ZCRXS_, _BC_,
                  _ylc_,_MD0_)  # _Tj_进口温度, _Thj_环境温度, _D_管径, _M_质量流量, _Di_焦汤系数, _ZCRXS_总传热系数, _Cpp_高压定压比热, _BC_步长, _ylc_压力差用yali[-1]-yali[-2]表示
        LT6.append(Tc)
print('各压缩机转速',zs)
print('各压缩机功率',power)

print('第一管段压力',LP0)
print('第二管段压力', LP1)
print('第三管段压力', LP2)
print('第四管段压力',LP3)
print('第五管段压力',LP4)
print('第六管段压力',LP5)
print('第七管段压力',LP6)

print('第一管段温度',LT0)
print('第二管段温度', LT1)
print('第三管段温度', LT2)
print('第四管段温度',LT3)
print('第五管段温度',LT4)
print('第六管段温度',LT5)
print('第七管段温度',LT6)