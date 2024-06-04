# -*- coding: utf-8 -*-
"""
Created on Sat May  7 22:36:52 2022

@author: julia
"""

import math
from tkinter import *
import tkinter.messagebox
# import pickle
# import sympy
import numpy as np
# from matplotlib import pyplot as plt
from Nmaxelem import *

f = open('allBests.txt', 'r+')
f.truncate(0)


def Jemp():

    return np.arange(0.1, 1.5, 0.1)


def pdx():

    return np.arange(0.5, 1.5, 0.05)


def aeaox():

    return np.arange(0.3, 1.1, 0.05)


class holtrop (Tk, object):

    def __init__(self):
        super(holtrop, self).__init__()

        self.title("Cálculo (Holtrop)")

        frameTopLevel = Frame(self, bg='white')
        frameTopLevel.grid(row=0, column=0)

        self.frameInfo = Frame(frameTopLevel, bg='White')
        self.frameInfo.grid(row=0, column=0)

        self.label = Label(self.frameInfo, text='Cálculo de Propulsores ',
                           font='Broadway 14', bg='White', fg='Blue')
        self.label.grid(row=0, column=3)

        self.label = Label(
            self.frameInfo, text="Diâmetro do propulsor [m]:", font='Likhan 10', bg='White', fg='dark turquoise')
        self.label.grid(row=1, column=0)
        self.entry = Entry(self.frameInfo, font='Arial 10')
        self.entry.grid(row=1, column=1)

        self.frameButtons = Frame(frameTopLevel)
        self.frameButtons.grid(row=6, column=3)

        self.label = Label(
            self.frameInfo, text="Velocidade Avanço [m/s]:", font='Likhan 10', bg='White', fg='dark turquoise')
        self.label.grid(row=2, column=0)
        self.entry2 = Entry(self.frameInfo, font='Arial 10')
        self.entry2.grid(row=2, column=1)

        self.label = Label(
            self.frameInfo, text="Peso específico do fluido [Kg/m3]:", font='Likhan 10', bg='White', fg='dark turquoise')
        self.label.grid(row=3, column=0)
        self.entry3 = Entry(self.frameInfo, font='Arial 10')
        self.entry3.grid(row=3, column=1)

        self.label = Label(
            self.frameInfo, text="Força propulsiva requerida [kN]:", font='Likhan 10', bg='White', fg='dark turquoise')
        self.label.grid(row=4, column=0)
        self.entry4 = Entry(self.frameInfo, font='Arial 10')
        self.entry4.grid(row=4, column=1)

        self.frm_entry = Frame(frameTopLevel)

        self.lbl_v = Label(self.frameInfo, text="Coeficiente Prismático",
                           font='Likhan 10', bg='White', fg='dark turquoise')
        self.lbl_v.grid(row=1, column=2)
        self.ent_Cp = Entry(self.frameInfo, width=10, font='Arial 10')
        self.ent_Cp.grid(row=1, column=3)

        self.lbl_v1 = Label(
            self.frameInfo, text="LCB a partir da ré [m]", font='Likhan 10', bg='White', fg='dark turquoise')
        self.lbl_v1.grid(row=2, column=2)
        self.ent_LCB = Entry(self.frameInfo, width=10, font='Arial 10')
        self.ent_LCB.grid(row=2, column=3)

        '''self.lbl_v2 = Label(self.frameInfo, text="ηrr - Eficiência Rotativa Relativa",font='Likhan 14',bg='White',fg='dark turquoise')
        self.lbl_v2.grid(row=3, column=2)
        self.ent_ηrr = Entry(self.frameInfo, width=10,font='Arial 12')
        self.ent_ηrr.grid(row=3, column=3)'''

        self.lbl_v3 = Label(
            self.frameInfo, text="LPP [m]", font='Likhan 10', bg='White', fg='dark turquoise')
        self.lbl_v3.grid(row=3, column=2)
        self.ent_w = Entry(self.frameInfo, width=10, font='Arial 10')
        self.ent_w.grid(row=3, column=3)

        self.lbl_v31 = Label(
            self.frameInfo, text="LWL [m]", font='Likhan 10', bg='White', fg='dark turquoise')
        self.lbl_v31.grid(row=4, column=2)
        self.ent_lwl = Entry(self.frameInfo, width=10, font='Arial 10')
        self.ent_lwl.grid(row=4, column=3)

        self.lbl_v32 = Label(
            self.frameInfo, text="Calado [m]", font='Likhan 10', bg='White', fg='dark turquoise')
        self.lbl_v32.grid(row=5, column=2)
        self.ent_cal = Entry(self.frameInfo, width=10, font='Arial 10')
        self.ent_cal.grid(row=5, column=3)

        self.lbl_v4 = Label(self.frameInfo, text="ηt                                                                             ",
                            font='Likhan 10', bg='White', fg='dark turquoise')
        self.lbl_v4.grid(row=1, column=4)
        self.lbl_v41 = Label(self.frameInfo, text=" (P/ Acoplamento Direto Digite 1, P/Caixa Redutora Digite 2)",
                             font='Likhan 8', bg='White', fg='dark turquoise')
        self.lbl_v41.grid(row=1, column=4)
        self.ent_ηt = Entry(self.frameInfo, width=10, font='Arial 10')
        self.ent_ηt.grid(row=1, column=5)

        self.lbl_v5 = Label(self.frameInfo, text="Margem de Mar %",
                            font='Likhan 10', bg='White', fg='dark turquoise')
        self.lbl_v5.grid(row=2, column=4)
        self.ent_mmar = Entry(self.frameInfo, width=10, font='Arial 10')
        self.ent_mmar.grid(row=2, column=5)

        self.lbl_v6 = Label(self.frameInfo, text="Margem de Rotação %",
                            font='Likhan 10', bg='White', fg='dark turquoise')
        self.lbl_v6.grid(row=3, column=4)
        self.ent_mrot = Entry(self.frameInfo, width=10, font='Arial 10')
        self.ent_mrot.grid(row=3, column=5)

        self.lbl_v7 = Label(self.frameInfo, text="Margem Operacional %",
                            font='Likhan 10', bg='White', fg='dark turquoise')
        self.lbl_v7.grid(row=4, column=4)
        self.ent_moper = Entry(self.frameInfo, width=10, font='Arial 10')
        self.ent_moper.grid(row=4, column=5)

        self.buttonCalculate = Button(
            self.frameButtons, text='Calcular', font='Broadway 10', bg='white', fg='dark turquoise')
        self.buttonCalculate.grid(row=6, column=3)
        self.buttonCalculate.bind('<Button-1>', self.Calculate)

    def Calculate(self, event):
        # from .data import prop_diameter, Vs, rho, required_prop_force, prismatic_coefficient, LCB, LWL, LPP, T, nt, sea_margin, rotation_margin, operation_margin

        d = float(self.entry.get())
        va = float(self.entry2.get())
        ro = float(self.entry3.get())
        tpropcalc = float(self.entry4.get())
        Cp = float(self.ent_Cp.get())
        lcbi = float(self.ent_LCB.get())
        nt = float(self.ent_ηt.get())
        LWL = float(self.ent_lwl.get())
        LPP = float(self.ent_w.get())
        lcb = ((lcbi+LWL-LPP)-LWL/2)/LWL*100

        if nt == 1:
            ntv = 0.97
        else:
            ntv = 0.93

        J = Jemp()
        PD = pdx()
        AeAo = aeaox()
        z = 3
        t1 = 1*tpropcalc
        t2 = 1.11*tpropcalc
        THP = 2*tpropcalc*va
        lists = []
        grupo = []

        file = open('allBests.txt', 'a')
        file.write('Npás J  P/D Ae/Ao nRev.p/seg. Empuxo Propulsor       KT                  KQ                Rendimento            DHP                BHP                BHP1         RPM1           BHP2       RPM2         BHP3         RPM3 ')
        file.write('\n')

        while z < 7:
            for i in J:
                for x in PD:
                    for y in AeAo:

                        a1 = (0.00880496000)*1*1*1*1
                        a2 = -0.20455400000*i*1*1*1
                        a3 = 0.16635100000*x*1*1*1
                        a4 = 0.15811400000*(x**2)*1*1*1
                        a5 = -0.14758100000*(i**2)*(y)*1*1
                        a6 = -0.48149700000*(i)*x*y*1
                        a7 = 0.41543700000*(x**2)*y*1*1
                        a8 = (0.01440430000)*z*1*1*1
                        a9 = -0.05300540000*(i**2)*z*1*1
                        a10 = 0.01434810000*x*z*1*1
                        a11 = 0.06068260000*i*x*z*1
                        a12 = -0.01258940000*y*z*1*1
                        a13 = 0.01096890000*i*z*y*1
                        a14 = -0.13369800000*(x**3)*1*1*1
                        a15 = 0.00638407000*(x**6)*1*1*1
                        a16 = -0.00132718000*(i**2)*(x**6)*1*1
                        a17 = 0.16849600000*(i**3)*y*1*1
                        a18 = -0.05072140000*(y**2)*1*1*1
                        a19 = 0.08545590000*(i**2)*(y**2)*1*1
                        a20 = -0.05044750000*(i**3)*(y**2)*1*1
                        a21 = 0.01046500000*(i)*(x**6)*(y**2)*1
                        a22 = -0.0064827200*(i**2)*(x**6)*(y**2)*1
                        a23 = -0.00841728000*(x**3)*z*1*1
                        a24 = 0.01684240000*(i)*(x**3)*z*1
                        a25 = -0.00102296000*(i**3)*(x**3)*z*1
                        a26 = -0.03177910000*(x**3)*y*z*1
                        a27 = 0.01860400000*(i)*(y**2)*z*1
                        a28 = -0.00410798000*(x**2)*(y**2)*z*1
                        a29 = -0.00060684800*(z**2)*1*1*1
                        a30 = -0.00498190000*(i)*(z**2)*1*1
                        a31 = 0.00259830000*(i**2)*(z**2)*1*1
                        a32 = -0.00056052800*(i**3)*(z**2)*1*1
                        a33 = -0.00163652000*(i)*(x**2)*(z**2)*1
                        a34 = -0.00032878700*(i)*(x**6)*(z**2)*1
                        a35 = 0.00011650200*(i**2)*(x**6)*(z**2)*1
                        a36 = 0.00069090400*(y)*(z**2)*1*1
                        a37 = 0.00421749000*(x**3)*y*(z**2)*1
                        a38 = 0.00005652229*(i**3)*(x**6)*y*(z**2)
                        a39 = -0.00146564000*(x**3)*(y**2)*(z**2)*1

                        kt = a1+a2+a3+a4+a5+a6+a7+a8+a9+a10+a11+a12+a13+a14+a15+a16+a17+a18+a19+a20 + \
                            a21+a22+a23+a24+a25+a26+a27+a28+a29+a30+a31+a32+a33+a34+a35+a36+a37+a38+a39

                        n = va/(i*d)
                        tprop = (kt*ro*(n**2)*(d**4))/1000

                        b1 = 0.0037936800*1*1*1*1
                        b2 = 0.0088652300*(i**2)*1*1*1
                        b3 = -0.0322410000*i*x*1*1
                        b4 = 0.0034477800*(x**2)*1*1*1
                        b5 = -0.0408811000*x*y*1*1
                        b6 = -0.1080090000*i*x*y*1
                        b7 = -0.0885381000*(i**2)*x*y*1
                        b8 = 0.1885610000*(x**2)*y*1*1
                        b9 = -0.0037087100*i*z*1*1
                        b10 = 0.0051369600*x*z*1*1

                        b11 = 0.0209449000*i*x*z*1
                        b12 = 0.0047431900*(i**2)*x*z*1
                        b13 = -0.0072340800*(i**2)*y*z*1
                        b14 = 0.0043838800*i*x*y*z
                        b15 = -0.0269403000*(x**2)*y*z*1
                        b16 = 0.0558082000*(i**3)*y*1*1
                        b17 = 0.0161886000*(x**3)*y*1*1
                        b18 = 0.0031808600*i*(x**3)*y*1
                        b19 = 0.0158960000*(y**2)*1*1*1
                        b20 = 0.0471729000*i*(y**2)*1*1

                        b21 = 0.0196283000*(i**3)*(y**2)*1*1
                        b22 = -0.0502782000*x*(y**2)*1*1
                        b23 = -0.0300550000*(i**3)*x*(y**2)*1
                        b24 = 0.0417122000*(i**2)*(x**2)*(y**2)*1
                        b25 = -0.0397722000*(x**3)*(y**2)*1*1
                        b26 = -0.0035002400*(x**6)*(y**2)*1*1
                        b27 = -0.0106854000*(i**3)*z*1*1
                        b28 = 0.0011090300*(i**3)*(x**3)*z*1
                        b29 = -0.0003139120*(x**6)*z*1*1
                        b30 = 0.0035985000*(i**3)*y*z*1

                        b31 = -0.0014212100*(x**6)*y*z*1
                        b32 = -0.0038363700*i*(y**2)*z*1
                        b33 = 0.0126803000*(x**2)*(y**2)*z*1
                        b34 = -0.0031827800*(i**2)*(x**3)*(y**2)*z
                        b35 = 0.0033426800*(x**6)*(y**2)*z*1
                        b36 = -0.0018349100*i*x*(z**2)*1
                        b37 = 0.0001124510*(i**3)*(x**2)*(z**2)*1
                        b38 = -0.0000297228*(i**3)*(x**6)*(z**2)*1
                        b39 = 0.0002695510*i*y*(z**2)*1
                        b40 = 0.0008326500*(i**2)*y*(z**2)*1

                        b41 = 0.0015533400*(x**2)*y*(z**2)*1
                        b42 = 0.0003026830*(x**6)*y*(z**2)*1
                        b43 = -0.0001843000*(y**2)*(z**2)*1*1
                        b44 = -0.0004253990*(x**3)*(y**2)*(z**2)*1
                        b45 = 0.0000869243*(i**3)*(x**3)*(y**2)*(z**2)
                        b46 = -0.0004659000*(x**6)*(y**2)*(z**2)*1
                        b47 = 0.0000554194*i*(x**6)*(y**2)*(z**2)

                        kq = b1+b2+b3+b4+b5+b6+b7+b8+b9+b10+b11+b12+b13+b14+b15+b16+b17+b18+b19+b20+b21+b22+b23+b24 + \
                            b25+b26+b27+b28+b29+b30+b31+b32+b33+b34+b35+b36 + \
                            b37+b38+b39+b40+b41+b42+b43+b44+b45+b46+b47

                        print(float(self.ent_cal.get()))

                        if tprop >= t1 and tprop <= t2:

                            Ao = math.pi*((d**2)/4)

                            Ae = Ao*y
                            Ap = Ae*(1.067-(0.229*x))
                            vr = ((va**2)+(0.7*math.pi*d*n)**2)**0.5
                            qt = (0.5*ro*(vr**2))
                            popv = 101325 - 2278 + \
                                (ro*9.805*(float(self.ent_cal.get())-((d/2)+0.15)))
                            sigma = float((popv)/qt)
                            tau = float((tprop/Ap)/(qt/1000))
                            # y = 0,1082*ln(x)+0,2675 p 5% de cavitacao
                            tauregression = 0.1082*math.log(sigma)+0.2675
                            sigmaregression = math.exp((tau-0.2675)/0.1082)
                            if sigma >= sigmaregression and sigma <= 1.5 and sigma >= 0.16:
                                if tau <= tauregression and tau <= 0.32 and tau >= 0.08:  # valores 1.5 e 0.16 para 5%
                                    rendimento = (i*kt)/(2*math.pi*kq)
                                    rotacao = n*60
                                    nRR = 0.9737 + 0.111 * \
                                        (Cp - 0.0225*lcb) - 0.06325*x
                                    DHP = THP/(nRR*rendimento)
                                    BHP = DHP/ntv
                                    BHP1 = BHP * \
                                        (1+((float(self.ent_mmar.get()))/100))
                                    RPM1 = ((BHP1/BHP)**(1/3))*rotacao
                                    RPM2 = RPM1 * \
                                        (1+(float(self.ent_mrot.get())/100))
                                    BHP2 = ((RPM2/RPM1)**3)*BHP1
                                    BHP3 = BHP2 * \
                                        (1+(float(self.ent_moper.get())/100))
                                    RPM3 = ((BHP3/BHP2)**(1/3))*RPM2

                                    if rendimento > 0.55:
                                        lists.append(rendimento)
                                        # lists.append(RPM3)
                                        # lists.append(BHP3)
                                        grupo.append(rendimento)
                                        grupo.append(RPM3)
                                        grupo.append(BHP3)

                                        a = str(round(i, 2))
                                        b = str(round(x, 2))
                                        c = str(round(y, 2))
                                        f = str(round(n, 2))
                                        ab = str(round(RPM1, 2))
                                        ac = str(round(RPM2, 2))
                                        ad = str(round(RPM3, 2))

                                        file = open('allBests.txt', 'a')
                                        file.write(str(z))
                                        file.write('--')
                                        file.write(a)
                                        file.write('--')
                                        file.write(b)
                                        file.write('--')
                                        file.write(c)
                                        file.write('--')
                                        file.write(f)
                                        file.write('--')
                                        file.write(str(tprop))
                                        file.write('--')
                                        file.write(str(kt))
                                        file.write('--')
                                        file.write(str(kq))
                                        file.write('--')
                                        file.write(str(rendimento))
                                        file.write('--')
                                        file.write(str(DHP))
                                        file.write('--')
                                        file.write(str(BHP))
                                        file.write('--')
                                        file.write(str(BHP1))
                                        file.write('--')
                                        file.write(ab)
                                        file.write('--')
                                        file.write(str(BHP2))
                                        file.write('--')
                                        file.write(str(ac))
                                        file.write('--')
                                        file.write(str(BHP3))
                                        file.write('--')
                                        file.write(str(ad))
                                        file.write('\n')

            z = z + 1

        # print (lista)
        # print (((len(lista))-1)/8)

        maiores = Nmaxele(lists, 45)

        final = []

        for ii in maiores:
            for ij in grupo:
                if ii == ij:
                    index1 = grupo.index(ij)

                    final.append(grupo[index1])
                    final.append(grupo[index1+1])
                    final.append(grupo[index1+2])

        # Set up the window
        window = tkinter.Tk()
        window.title("6 Melhores Propulsores")
        window.resizable(width=False, height=False)

        # Create the Fahrenheit entry frame with an Entry
        # widget and label in it

        frm_entry = tkinter.Frame(master=window)
        frm_entry.grid(row=3, column=3)
        frm_entry.config(bg='LightCyan')

        # frm_entry = tkinter.Frame(master=window)

        lbl_v = tkinter.Label(
            master=frm_entry, text='Rendimento = ' + str(final[0]), bg='LightCyan')

        lbl_v1 = tkinter.Label(
            master=frm_entry, text='RPM3 = ' + str(final[1]), bg='LightCyan')

        lbl_v2 = tkinter.Label(
            master=frm_entry, text='BHP3 = ' + str(final[2]) + 'kW', bg='LightCyan')

        lbl_v3 = tkinter.Label(
            master=frm_entry, text='Rendimento = ' + str(final[3]), bg='LightCyan')

        lbl_v4 = tkinter.Label(
            master=frm_entry, text='RPM3 = ' + str(final[4]), bg='LightCyan')

        lbl_v5 = tkinter.Label(
            master=frm_entry, text='BHP3 = ' + str(final[5]) + 'kW', bg='LightCyan')

        lbl_v6 = tkinter.Label(
            master=frm_entry, text='Rendimento = ' + str(final[6]), bg='LightCyan')

        lbl_v7 = tkinter.Label(
            master=frm_entry, text='RPM3 = ' + str(final[7]), bg='LightCyan')

        lbl_v8 = tkinter.Label(
            master=frm_entry, text='BHP3 = ' + str(final[8]) + 'kW', bg='LightCyan')

        lbl_v9 = tkinter.Label(
            master=frm_entry, text='Rendimento = ' + str(final[9]), bg='LightCyan')

        lbl_v10 = tkinter.Label(
            master=frm_entry, text='RPM3 = ' + str(final[10]), bg='LightCyan')

        lbl_v11 = tkinter.Label(
            master=frm_entry, text='BHP3 = ' + str(final[11]) + 'kW', bg='LightCyan')

        lbl_v12 = tkinter.Label(
            master=frm_entry, text='Rendimento = ' + str(final[12]), bg='LightCyan')

        lbl_v13 = tkinter.Label(
            master=frm_entry, text='RPM3 = ' + str(final[13]), bg='LightCyan')

        lbl_v14 = tkinter.Label(
            master=frm_entry, text='BHP3 = ' + str(final[14]) + 'kW', bg='LightCyan')

        lbl_v15 = tkinter.Label(
            master=frm_entry, text='Rendimento = ' + str(final[15]), bg='LightCyan')

        lbl_v16 = tkinter.Label(
            master=frm_entry, text='RPM3 = ' + str(final[16]), bg='LightCyan')

        lbl_v17 = tkinter.Label(
            master=frm_entry, text='BHP3 = ' + str(final[17]) + 'kW', bg='LightCyan')

        lbl_v.grid(row=0, column=1, sticky="w")
        lbl_v1.grid(row=0, column=2, sticky="w")
        lbl_v2.grid(row=0, column=3, sticky="w")

        lbl_v3.grid(row=1, column=1, sticky="w")
        lbl_v4.grid(row=1, column=2, sticky="w")
        lbl_v5.grid(row=1, column=3, sticky="w")

        lbl_v6.grid(row=2, column=1, sticky="w")
        lbl_v7.grid(row=2, column=2, sticky="w")
        lbl_v8.grid(row=2, column=3, sticky="w")

        lbl_v9.grid(row=3, column=1, sticky="w")
        lbl_v10.grid(row=3, column=2, sticky="w")
        lbl_v11.grid(row=3, column=3, sticky="w")

        lbl_v12.grid(row=4, column=1, sticky="w")
        lbl_v13.grid(row=4, column=2, sticky="w")
        lbl_v14.grid(row=4, column=3, sticky="w")

        lbl_v15.grid(row=5, column=1, sticky="w")
        lbl_v16.grid(row=5, column=2, sticky="w")
        lbl_v17.grid(row=5, column=3, sticky="w")

        frm_entry.grid(row=0, column=0, padx=10)

        # Run the application
        window.mainloop()

        # file.close()


hol = holtrop()
hol.mainloop()
