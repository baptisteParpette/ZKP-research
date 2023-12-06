import sys;
from py_ecc.bn128 import G1, G2, multiply, add, curve_order, eq, neg, pairing
import galois

GF = galois.GF(curve_order)

u = galois.Poly([14774563938491510775016323878048660684770145970280823181996287825938670734546, 3648040478639879203707734290876212514758060733402672390616367364429301415868, 10032111316259667810196269299909584415584667016857349074195010252180578894213, 7296080957279758407415468581752425029516121466805344781232734728858602830837, 8025689053007734248157015439927667532467733613485879259356008201744463116328, 21888242871839275222246405745257275088548364400416034343698204186575808495064], field=GF)
v = galois.Poly([20429026680383323540763312028906790082645140107054965387451657240804087929235, 14592161914559516814830937163504850059032242933610689562465469457717205663881, 7296080957279758407415468581752425029516121466805344781232734728858602830952, 7296080957279758407415468581752425029516121466805344781232734728858602834704, 16051378106015468496314030879855335064935467226971758518712016403488926226275, 1809], field=GF)
w = galois.Poly([11126523459851631571308589587172448170012085236878150791379920461509369318592, 3648040478639879203707734290876212514758060733402672390616367364429301416191, 13680151794899547013904003590785796930342727750260021464811377616609880307969, 7296080957279758407415468581752425029516121466805344781232734728858602837524, 8025689053007734248157015439927667532467733613485879259356008201744463107336, 3647], field=GF)
t = galois.Poly([1, 21888242871839275222246405745257275088548364400416034343698204186575808495596, 175, 21888242871839275222246405745257275088548364400416034343698204186575808494882, 1624, 21888242871839275222246405745257275088548364400416034343698204186575808493853, 720], field=GF)
h = galois.Poly([0, 18568526036276985146872367540559921700118529133019602468237309884945144207081, 8414813370729321363219173764287796867375260091715497647688420720616921933174, 2760350628837508597472185613429667469500265954941355442233051305751504736345, 1240333762737558929260629658897912255017740649356908612809564903905962484152, 19213013187503363806194067265281385911059119862587407923912868119327654122536], field=GF)

# check initial
h_quo = (u * v - w) // t
h_rem = (u * v - w) % t

print(h_quo)
print(h_rem)
if (h_rem != 0):
    print("Les équations sont cassées")
    sys.exit()
print("Les équations sont bonnes")

# La partie du vérifieur. Il prépare, X sur G1 et X sur G2 et T sur G2
tau = GF(123)

XG1_6 = multiply(G1, int(tau**6))
XG1_5 = multiply(G1, int(tau**5))
XG1_4 = multiply(G1, int(tau**4))
XG1_3 = multiply(G1, int(tau**3))
XG1_2 = multiply(G1, int(tau**2))
XG1_1 = multiply(G1, int(tau))
XG1_0 = G1

XG2_5 = multiply(G2, int(tau**5))
XG2_4 = multiply(G2, int(tau**4))
XG2_3 = multiply(G2, int(tau**3))
XG2_2 = multiply(G2, int(tau**2))
XG2_1 = multiply(G2, int(tau))
XG2_0 = G2

TG1_0=multiply(G1, int(t(tau)))
TG1_1=multiply(TG1_0, (int(tau)))
TG1_2=multiply(TG1_0, (int(tau**2)))
TG1_3=multiply(TG1_0, (int(tau**3)))
TG1_4=multiply(TG1_0, (int(tau**4)))

# La partie du prouveur
u5 = multiply(XG1_5, 14774563938491510775016323878048660684770145970280823181996287825938670734546)
u4 = multiply(XG1_4, 3648040478639879203707734290876212514758060733402672390616367364429301415868)
u3 = multiply(XG1_3, 10032111316259667810196269299909584415584667016857349074195010252180578894213)
u2 = multiply(XG1_2, 7296080957279758407415468581752425029516121466805344781232734728858602830837)
u1 = multiply(XG1_1, 8025689053007734248157015439927667532467733613485879259356008201744463116328)
u0 = multiply(XG1_0, 21888242871839275222246405745257275088548364400416034343698204186575808495064)
encodeCoeffUwG1=(add(add(add(add(add(u0, u1), u2),u3),u4),u5))

v5 = multiply(XG2_5, 20429026680383323540763312028906790082645140107054965387451657240804087929235)
v4 = multiply(XG2_4, 14592161914559516814830937163504850059032242933610689562465469457717205663881)
v3 = multiply(XG2_3, 7296080957279758407415468581752425029516121466805344781232734728858602830952)
v2 = multiply(XG2_2, 7296080957279758407415468581752425029516121466805344781232734728858602834704)
v1 = multiply(XG2_1, 16051378106015468496314030879855335064935467226971758518712016403488926226275)
v0 = multiply(XG2_0, 1809)
encodeCoeffVwG2=(add(add(add(add(add(v0, v1), v2),v3),v4),v5))

w5 = multiply(XG1_5, 11126523459851631571308589587172448170012085236878150791379920461509369318592)
w4 = multiply(XG1_4, 3648040478639879203707734290876212514758060733402672390616367364429301416191)
w3 = multiply(XG1_3, 13680151794899547013904003590785796930342727750260021464811377616609880307969)
w2 = multiply(XG1_2, 7296080957279758407415468581752425029516121466805344781232734728858602837524)
w1 = multiply(XG1_1, 8025689053007734248157015439927667532467733613485879259356008201744463107336)
w0 = multiply(XG1_0, 3647)
encodeCoeffWwG1=(add(add(add(add(add(w0, w1), w2),w3),w4),w5))


# Le vérifieurs reçoit 
print("Le vérifieur reçoit du prouveur")
print("Uw=",encodeCoeffUwG1)
print("Vw=",encodeCoeffVwG2)
print("Ww=",encodeCoeffWwG1)
print("Les coefficients du polynôme h=", [0, 18568526036276985146872367540559921700118529133019602468237309884945144207081, 8414813370729321363219173764287796867375260091715497647688420720616921933174, 2760350628837508597472185613429667469500265954941355442233051305751504736345, 1240333762737558929260629658897912255017740649356908612809564903905962484152, 19213013187503363806194067265281385911059119862587407923912868119327654122536])

print("Il recoit également du préparateur, les coefficients de T[tau] pour tous les degrés de h")
print("Il combine les coefficients de h du prouveur, avec les coeffient de T[tau] du préparateur")
ht4  = multiply(TG1_4, 18568526036276985146872367540559921700118529133019602468237309884945144207081)
ht3  = multiply(TG1_3, 8414813370729321363219173764287796867375260091715497647688420720616921933174)
ht2  = multiply(TG1_2, 2760350628837508597472185613429667469500265954941355442233051305751504736345)
ht1  = multiply(TG1_1, 1240333762737558929260629658897912255017740649356908612809564903905962484152)
ht0  = multiply(TG1_0, 19213013187503363806194067265281385911059119862587407923912868119327654122536)
encodeCoeffHTG1=(add(add(add(add(ht0, ht1), ht2),ht3),ht4))

print("Le vérifieur peut alors réaliser le test suivant")
print(" Pairing(U(proof surG1), V(proof surG2) == Pairing((W(proof sur G1) + Ecode(coefh sur TG1)), G2) ")

LPairing = pairing(encodeCoeffVwG2, encodeCoeffUwG1)
RPairing = pairing(G2, add(encodeCoeffWwG1, encodeCoeffHTG1))

#print(LPairing)
#print(RPairing)

print("VALIDATION", LPairing == RPairing)

