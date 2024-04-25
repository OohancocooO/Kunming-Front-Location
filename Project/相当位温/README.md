## 计算方法
相当位温：
$\theta_{e}=\theta\exp\left(\frac{Lr}{C_{p}T_{d}}\right)=T\left(\frac{p}{p_{0}}\right)^{-\frac{R}{C_{p}}}\exp\left(\frac{Lr}{C_{p}T_{d}}\right)$

简化：$\theta_{e}=T\left(\frac{p}{p_{0}}\right)^{-\frac{R}{C_{p}}}\exp\left(\frac{Lr}{C_{p}T_{d}}\right)$

R= $R_{d}$ = 287.05
$C_{p}$=$C_{pd}$=1004
$T_{d}$=露点温度
Lr
T：温度(K) 
TD：露点温度(K) 
P：気圧(hPa) 
e：水蒸気圧(hPa) 
x：混合比(kg/kg)

$\theta_{e}=T\left(\frac{1000}{P-e}\right)^{\frac{R_{d}}{C_{pd}}}\left(\frac{T}{T_{LCL}}\right)^{0.28x}\exp\left(\left(\frac{3036.0}{T_{LCL}}-1.78\right)x(1+0.448x)\right)$

TCL计算
$T_{LCL}=\frac{1}{\frac{1}{T_{D}-56}+\frac{\ln(T/T_{D})}{800}}+56$

饱和水汽压
$e_{s}=6.112\exp\left(\frac{17.67(T-273.15)}{T-29.65}\right)$

水汽压
$e=\frac{e_{s}exp[\frac{a(T_{d}-273.15)}{T_{d}-b}]}{exp[\frac{a(T-273.15)}{T-b}]}$

混合比
$x=0.622\frac{e}{P-e}$







## Meaning
通常来说，锋线是气团与气团的分界线，在许多情况下，可以作为温度梯度来识别。然而，在梅雨锋线的情况下，温度梯度并不明显，而是更多地作为等温位梯度来清晰识别。向上方移动时温位降低的状态被称为绝对不稳定，会引起对流试图消除不稳定。因此，在大规模空间尺度上，这种温度层结通常不会出现。然而，上升过程中温位降低的状态却时常可以见到。等温位是指如果空气中包含的所有水蒸气都凝结时的假想温度，所以，即便下层的等温位比上层的要高，如果没有水蒸气的凝结发生，也并不一定意味着静力学上不稳定。
