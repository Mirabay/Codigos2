""" 

Created on Tue Feb 20 09:30:27 2024 

 

@author: arturoe 

""" 

import numpy as np 

 

 

def rotx(angle, units="rad"): 

    #Function to get a rotation matrix around the x-axis 

    # angle: the rotation angle (it can be either in degrees or radians depending on the selected "units" 

    # units: A string indicating if the angle is given in radians "rad" or degrees "deg" 

    if units == "deg": 

        angle = np.deg2rad(angle) 

    Rx=np.array([[1.0,0.0,0.0],[0.0,np.cos(angle),-np.sin(angle)],[0.0,np.sin(angle),np.cos(angle)]]) 

    return Rx 

 

def trotx(angle, units="rad"): 

    if units == "deg": 

        angle = np.deg2rad(angle) 

    R=rotx(angle) 

    TR=np.append(R, np.array([[0.0],[0.0],[0.0]]),1) 

    TR=np.append(TR, np.array([[0.0,0.0,0.0,1.0]]),0) 

    return TR 

 

 

#Function to get a rotation matrix about the y axis 

def roty(angle, units="rad"): 

    if units == "deg": 

        angle = np.deg2rad(angle) 

    #Angle must be in radians 

    R=np.array([[np.cos(angle),0.0,np.sin(angle)],[0.0,1.0,0.0],[-np.sin(angle),0.0,np.cos(angle)]]) 

    return R 

 

 

def troty(angle, units="rad"): 

    if units == "deg": 

        angle = np.deg2rad(angle) 

    R=roty(angle) 

    TR=np.append(R, np.array([[0.0],[0.0],[0.0]]),1) 

    TR=np.append(TR, np.array([[0.0,0.0,0.0,1.0]]),0) 

    return TR 

 

#Function to get a rotation matrix about the z-axis 

def rotz(angle, units="rad"): 

    if units == "deg": 

        angle = np.deg2rad(angle) 

    #Angle must be in radians 

    R=np.array([[np.cos(angle),-np.sin(angle),0.0],[np.sin(angle),np.cos(angle),0.0],[0.0,0.0,1.0]]) 

    return R 

 

 

def trotz(angle, units="rad"): 

    if units == "deg": 

        angle = np.deg2rad(angle) 

    R=rotz(angle) 

    TR=np.append(R, np.array([[0.0],[0.0],[0.0]]),1) 

    TR=np.append(TR, np.array([[0.0,0.0,0.0,1.0]]),0) 

    return TR 

 

def transl(x,y,z): 

    T=np.array([[1.0,0.0,0.0,x],[0.0,1.0,0.0,y],[0.0,0.0,1.0,z],[0.0,0.0,0.0,1.0]]) 

    return T 

 

def rot2rpy(R=np.identity(3), units="rad"): 

     

    r11=R[0][0] 

    r12=R[0][1] 

    r13=R[0][2] 

    r21=R[1][0] 

    r22=R[1][1] 

    r23=R[1][2] 

    r31=R[2][0] 

     

    #yaw angle 

    yaw = np.arctan2(r21,r11)  

     

    #roll 

    roll= np.arctan2(-r23*np.cos(yaw)+r13*np.sin(yaw), r22*np.cos(yaw)-r12*np.sin(yaw))  

    #pitch 

    pitch = np.arctan2(-r31, r11*np.cos(yaw)+r21*np.sin(yaw)) 

     

    if units == "deg": 

        yaw = np.rad2deg(yaw) 

        pitch = np.rad2deg(pitch) 

        roll = np.rad2deg(roll) 

     

    return roll, pitch, yaw 

 

def rot2rpyfull(R=np.identity(3), units="rad"): 

     

    r11=R[0][0] 

    r12=R[0][1] 

    r13=R[0][2] 

    r21=R[1][0] 

    r22=R[1][1] 

    r23=R[1][2] 

    r31=R[2][0] 

     

    #yaw angle 

    yaw1 = np.arctan2(r21,r11)  

    yaw2 = np.arctan2(-r21,-r11)  

    #roll 

    roll1= np.arctan2(-r23*np.cos(yaw1)+r13*np.sin(yaw1), r22*np.cos(yaw1)-r12*np.sin(yaw1))  

    roll2= np.arctan2(-r23*np.cos(yaw2)+r13*np.sin(yaw2), r22*np.cos(yaw2)-r12*np.sin(yaw2))  

    #pitch 

    pitch1 = np.arctan2(-r31, r11*np.cos(yaw1)+r21*np.sin(yaw1)) 

    pitch2 = np.arctan2(-r31, r11*np.cos(yaw2)+r21*np.sin(yaw2)) 

    if units == "deg": 

        yaw1 = np.rad2deg(yaw1) 

        pitch1 = np.rad2deg(pitch1) 

        roll1 = np.rad2deg(roll1) 

        yaw2 = np.rad2deg(yaw2) 

        pitch2 = np.rad2deg(pitch2) 

        roll2 = np.rad2deg(roll2) 

     

    return np.array([[roll1,pitch1,yaw1],[roll2,pitch2,yaw2]]) 

 

def rot2eulzxzfull(R=np.identity(3), units="rad"): 

    r11=R[0][0] 

    r12=R[0][1] 

    r13=R[0][2] 

    r21=R[1][0] 

    r22=R[1][1] 

    r23=R[1][2] 

    #r31=R[2][0] 

    #r32=R[2][1] 

    r33=R[2][2] 

     

    #First Rotation (about Z) 

    phi1 = np.arctan2(r13,-r23)  

    phi2 = np.arctan2(-r13,r23)  

    # Second Rotation (about X) 

    theta1= np.arctan2(-r23*np.cos(phi1)+r13*np.sin(phi1), r33)  

    theta2= np.arctan2(-r23*np.cos(phi2)+r13*np.sin(phi2), r33)  

    # 3rd Rotation (about Z) 

    psi1 = np.arctan2(-r12*np.cos(phi1)-r22*np.sin(phi1), r11*np.cos(phi1)+r21*np.sin(phi1)) 

    psi2 = np.arctan2(-r12*np.cos(phi2)-r22*np.sin(phi2), r11*np.cos(phi2)+r21*np.sin(phi2)) 

    if units == "deg": 

        phi1 = np.rad2deg(phi1) 

        psi1 = np.rad2deg(psi1) 

        theta1 = np.rad2deg(theta1) 

        phi2 = np.rad2deg(phi2) 

        psi2 = np.rad2deg(psi2) 

        theta2 = np.rad2deg(theta2) 

     

    return np.array([[phi1,theta1,psi1],[phi2,theta2,psi2]]) 

 

 

def rot2eulzxz(R=np.identity(3), units="rad"): 

    r11=R[0][0] 

    r12=R[0][1] 

    r13=R[0][2] 

    r21=R[1][0] 

    r22=R[1][1] 

    r23=R[1][2] 

    #r31=R[2][0] 

    #r32=R[2][1] 

    r33=R[2][2] 

     

    #First Rotation (about Z) 

    phi1 = np.arctan2(r13,-r23)  

     

    # Second Rotation (about X) 

    theta1= np.arctan2(-r23*np.cos(phi1)+r13*np.sin(phi1), r33)  

     

    # 3rd Rotation (about Z) 

    psi1 = np.arctan2(-r12*np.cos(phi1)-r22*np.sin(phi1), r11*np.cos(phi1)+r21*np.sin(phi1)) 

    

    if units == "deg": 

        phi1 = np.rad2deg(phi1) 

        psi1 = np.rad2deg(psi1) 

        theta1 = np.rad2deg(theta1) 

     

    return np.array([[phi1,theta1,psi1]]) 

 

 

def rpy2rot(roll, pitch, yaw, units="rad"): 

    if units == "deg": 

        yaw = np.deg2rad(yaw) 

        pitch = np.deg2rad(pitch) 

        roll = np.deg2rad(roll) 

    R=rotz(yaw)@roty(pitch)@rotx(roll)  

    return R  

 

def eulzxz2rot(phi, theta, psi, units="rad"): 

    if units == "deg": 

        phi = np.deg2rad(phi) 

        theta = np.deg2rad(theta) 

        psi = np.deg2rad(psi) 

    #Rotation about ZXZ 

    R=rotz(phi)@rotx(theta)@rotz(psi)  

    return R  

 

def HTM(R,tx,ty,tz): 

    # R must be a 3x3 numpy array 

    # tx, ty, and tz are scalar values representing the translation  

    t=np.array([[tx],[ty],[tz]]) 

    T=np.concatenate((R, t), 1) #Concatenate along columns 

    T=np.concatenate((T, np.array([[0,0,0,1]])),0) 

    return T 

def forward_kin_RR(q1, q2):
    # Constantes del robot
    c1 = 1
    c2 = 1
    c3 = 1
    c4 = 1
    
    T01= trotz(q1,"deg")@transl(0, 0, c1)@transl(c2, 0, 0)@trotx(90,"deg")
    T12= trotz(q2,"deg")@transl(0, 0, c3)@transl(c4, 0, 0)@trotx(0,"deg")

    
    T02= T01@T12
    # Retornamos la matris T02
    return T02
    
    
 

if __name__=="__main__": 

    #Set decimal digits 

    np.set_printoptions(precision=4) 
    #Suppress exponential formating 

    np.set_printoptions(suppress=True)
    
    T02=forward_kin_RR(0,90)
    print(T02)