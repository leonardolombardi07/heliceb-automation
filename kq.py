def get_kq(
        J: float,
        PD: float,
        AeAo: float,
        nblades: int
) -> float:
    # TODO: we should include DeltaKQ0, but the difference is negligible for the purpose of this code
    b1 = 0.0037936800*1*1*1*1
    b2 = 0.0088652300*(J**2)*1*1*1
    b3 = -0.0322410000*J*PD*1*1
    b4 = 0.0034477800*(PD**2)*1*1*1
    b5 = -0.0408811000*PD*AeAo*1*1
    b6 = -0.1080090000*J*PD*AeAo*1
    b7 = -0.0885381000*(J**2)*PD*AeAo*1
    b8 = 0.1885610000*(PD**2)*AeAo*1*1
    b9 = -0.0037087100*J*nblades*1*1
    b10 = 0.0051369600*PD*nblades*1*1

    b11 = 0.0209449000*J*PD*nblades*1
    b12 = 0.0047431900*(J**2)*PD*nblades*1
    b13 = -0.0072340800*(J**2)*AeAo*nblades*1
    b14 = 0.0043838800*J*PD*AeAo*nblades
    b15 = -0.0269403000*(PD**2)*AeAo*nblades*1
    b16 = 0.0558082000*(J**3)*AeAo*1*1
    b17 = 0.0161886000*(PD**3)*AeAo*1*1
    b18 = 0.0031808600*J*(PD**3)*AeAo*1
    b19 = 0.0158960000*(AeAo**2)*1*1*1
    b20 = 0.0471729000*J*(AeAo**2)*1*1

    b21 = 0.0196283000*(J**3)*(AeAo**2)*1*1
    b22 = -0.0502782000*PD*(AeAo**2)*1*1
    b23 = -0.0300550000*(J**3)*PD*(AeAo**2)*1
    b24 = 0.0417122000*(J**2)*(PD**2)*(AeAo**2)*1
    b25 = -0.0397722000*(PD**3)*(AeAo**2)*1*1
    b26 = -0.0035002400*(PD**6)*(AeAo**2)*1*1
    b27 = -0.0106854000*(J**3)*nblades*1*1
    b28 = 0.0011090300*(J**3)*(PD**3)*nblades*1
    b29 = -0.0003139120*(PD**6)*nblades*1*1
    b30 = 0.0035985000*(J**3)*AeAo*nblades*1

    b31 = -0.0014212100*(PD**6)*AeAo*nblades*1
    b32 = -0.0038363700*J*(AeAo**2)*nblades*1
    b33 = 0.0126803000*(PD**2)*(AeAo**2)*nblades*1
    b34 = -0.0031827800*(J**2)*(PD**3)*(AeAo**2)*nblades
    b35 = 0.0033426800*(PD**6)*(AeAo**2)*nblades*1
    b36 = -0.0018349100*J*PD*(nblades**2)*1
    b37 = 0.0001124510*(J**3)*(PD**2)*(nblades**2)*1
    b38 = -0.0000297228*(J**3)*(PD**6)*(nblades**2)*1
    b39 = 0.0002695510*J*AeAo*(nblades**2)*1
    b40 = 0.0008326500*(J**2)*AeAo*(nblades**2)*1

    b41 = 0.0015533400*(PD**2)*AeAo*(nblades**2)*1
    b42 = 0.0003026830*(PD**6)*AeAo*(nblades**2)*1
    b43 = -0.0001843000*(AeAo**2)*(nblades**2)*1*1
    b44 = -0.0004253990*(PD**3)*(AeAo**2)*(nblades**2)*1
    b45 = 0.0000869243*(J**3)*(PD**3)*(AeAo**2)*(nblades**2)
    b46 = -0.0004659000*(PD**6)*(AeAo**2)*(nblades**2)*1
    b47 = 0.0000554194*J*(PD**6)*(AeAo**2)*(nblades**2)

    kq = b1+b2+b3+b4+b5+b6+b7+b8+b9+b10+b11+b12+b13+b14+b15+b16+b17+b18+b19+b20+b21+b22+b23+b24 + \
        b25+b26+b27+b28+b29+b30+b31+b32+b33+b34+b35+b36 + \
        b37+b38+b39+b40+b41+b42+b43+b44+b45+b46+b47
    return kq
