import math
import connectors
import timberShearJoints as joints

# define bolt

char = {} #dictionary of characteristics to be unpackekd to instance of "bolt class"
#units are not in SI as EN 1995-1-1 works with different units e.g. mm, N, kg/m3 etc...
char["d"] = 20 #diameter in mm
char["fu"] = 800 #ultimate yield strength 800 MPa
char["ro"] = 350 #characteristic density of timbe in kg/m3
char["alfa"] = 0 #angle between force and grains
char["t"] = 100 #ply thickness in mm

m20 = connectors.bolt(**char) #define instance of bolt class M20 8.8 in a 100 mm thick ply

print("For a bolt M{} of:".format(m20.d))
print("__ultimate yield strength fu = {} MPa".format(m20.fu))
print("__installed in timber ply t = {} mm thick".format(m20.t))
print("characteristic yield moment M_yRk = {} Nmm".format(m20.MyRk())) 
print("characteristic embedment strength f_hk = {} Nmm2".format(m20.fhk()))

#define timber - timber shear joint
t2t = joints.timber2(m20, m20) #define instance of timber2 joint class with two identical plies
print("characteristic resistance of timber - timber joint F_v,rk = {} N".format(t2t.Fvrk()))





 



