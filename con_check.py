'''
con_check.py
Author: Peter Herbert 2017
'''
from pymel.core import *
from numpy import *

def extend4x4(mat3x3,vect=array([0,0,0])):
    "function takes a 3x3 matrix and extends it into a 4x4 matrix with homogeneous coordinates"
    if shape(mat3x3)!=(3,3):
        print "Matrix is not a 3x3 matrix, as required"
        return

    mat4x4 = hstack((vstack((mat3x3,[0,0,0])),
                     vstack(([[vect[0]],[vect[1]],[vect[2]],[1]]))
                   ));

    return transpose(mat4x4);

'''initialize example'''
'''randomise example parameters (calculation can not have direct access to these values)'''
sphereRadius = random.randint(3,high=6); #Radius of Sphere (should be same for both spheres)
goalAxis = (random.random(3)).tolist(); #Orientation of goal sphere
goalMove = ((random.random(3))*20).tolist(); #Translate goal sphere to position in scenario
targetAxis = (random.random(3)).tolist(); #Orientation of target sphere
targetMove = ((random.random(3))*20).tolist(); #Translate target sphere to position in scenario

'''Generate Spheres in position'''
#Sphere 1 --- Goal Sphere
polySphere( r=sphereRadius, sx=20, sy=20, ax=goalAxis, ch=2, cuv=2, n='goal');
goalVertexCount = polyEvaluate(v=True);
move(goalMove[0],goalMove[1],goalMove[2], 'goal');
#Sphere 2 --- Target Sphere
polySphere( r=sphereRadius, sx=20, sy=20, ax=targetAxis, ch=2, cuv=2, n='target');
targetVertexCount = polyEvaluate(v=True);
move(targetMove[0],targetMove[1],targetMove[2], 'target');

if goalVertexCount != targetVertexCount:
    print 'Vertex Counts are not equal'; #Error check (just to confirm)

'''End of example'''

'''User input'''
goalInput = promptDialog(
  title='Choose goal Object',
  message='Goal Object:',
  button=['OK','Cancel'], 
  defaultButton='OK',
  cancelButton='Cancel',
  dismissString='Cancel');
if goalInput =='OK':
  goalObject = promptDialog(query=True, text=True);

targetInput = promptDialog(
  title='Choose target Object',
  message='Target Object:',
  button=['OK','Cancel'], 
  defaultButton='OK',
  cancelButton='Cancel',
  dismissString='Cancel');
if targetInput == 'OK':
  targetObject = promptDialog(query=True, text=True);

'''Beginning of Mapping'''
'''Choose three random vertices from sphere'''
indices=random.randint(goalVertexCount, size=3);
goalVertices = zeros(3).tolist();
targetVertices = zeros(3).tolist();
for x in range(0,3):
    goalVertices[x] = pointPosition('%s.vtx[%s]' %(goalObject, indices[x]), w=True);
    targetVertices[x] = pointPosition('%s.vtx[%s]' %(targetObject, indices[x]), w=True);
  
'''Goal translation to origin'''
Vstart = transpose(array(goalVertices));
Ustart = transpose(array(targetVertices));
Vone = zeros((3,3));
Uone = zeros((3,3));
for x in range(0,3):
  Vone[0:3,x] = Vstart[0:3,0]; #Zero indexed
  Uone[0:3,x] = Ustart[0:3,0];

Vdash = Vstart-Vone; #Translation of goal to origin
Udash = Ustart-Uone; #Translation of target to origin
transV4 = extend4x4(identity(3),(Vstart[0:3,0])*(-1)); #Goal tranlation matrix 4x4
transU4 = extend4x4(identity(3),Ustart[0:3,0]); #Target tranlation matrix 4x4
'''Alignment (first rotation)'''
axis1 = (Udash[0:3,1]+Vdash[0:3,1])/2; #Midpoint between second vertices
normaxis1 = axis1/(linalg.norm(axis1)); #First unit axis
crossaxis1 = array([[0,(normaxis1[2]*(-1)),normaxis1[1]],
              [normaxis1[2],0,(normaxis1[0]*(-1))],
              [(normaxis1[1]*(-1)),normaxis1[0],0]]); #Cross-product matrix defined by axis
R1 = identity(3)+(2*(linalg.matrix_power(crossaxis1,2))); #Frist rotation matrix
R14x4 = extend4x4(R1); #Frist Rotation matrix 4x4
Trans1 = dot(R1,Vdash);
'''Alignment (second rotation)'''
normaxis2 = (Udash[0:3,1])/(linalg.norm(Udash[0:3,1])); #second unit axis
crossaxis2 = array([[0,(normaxis2[2]*(-1)),normaxis2[1]],
              [normaxis2[2],0,(normaxis2[0]*(-1))],
              [(normaxis2[1]*(-1)),normaxis2[0],0]]); #Cross-product matrix defined by axis
perpV3 = (-1)*(dot((linalg.matrix_power(crossaxis2,2)),Trans1[0:3,2])); #Perpendicular component v3
perpU3 = (-1)*(dot((linalg.matrix_power(crossaxis2,2)),Udash[0:3,2])); #Perpendicular component u3
xproduct = cross(perpV3,perpU3);
direction = dot((xproduct/(linalg.norm(xproduct))),normaxis2); #Direction of rotation (+ is anticlockwise)
theta2 = (direction)*arccos(dot(perpU3,perpV3)/((linalg.norm(perpU3))*(linalg.norm(perpV3)))); 
R2 = identity(3) + ((crossaxis2)*(sin(theta2)))+((linalg.matrix_power(crossaxis2,2))*(1-cos(theta2)));
R24x4 = extend4x4(R2); #Second Rotation matrix 4x4
Motion = reshape((dot(dot(transV4,R14x4),dot(R24x4,transU4))).tolist(),16); #4x4 transformation matrix
'''Move goal sphere to target position'''
'''Individual Steps'''
'''
xform('goal', m=reshape(transV4.tolist(),16), r=True, piv=[0,0,0]);#Apply first translation
xform('goal', m=reshape(R14x4.tolist(),16), r=True, piv=[0,0,0])#Apply first rotation
xform('goal', m=reshape(R24x4.tolist(),16), r=True, piv=[0,0,0])#Apply Second rotation
xform('goal', m=reshape(transU4.tolist(),16), r=True, piv=[0,0,0])#Apply Second translation
'''
xform('goal',m=Motion, r=True, piv=[0,0,0])#Perform total transformation
'''Check step'''
goalCheck = zeros(3).tolist();
targetCheck = zeros(3).tolist();
for x in range(0,3):
    goalCheck[x] = pointPosition('goal.vtx[%s]' %(indices[x]), w=True);
    targetCheck[x] = pointPosition('target.vtx[%s]' %(indices[x]), w=True);

Check = transpose(array(goalCheck))-transpose(array(targetCheck));
print Check#Check difference in positions of goal vertices and target vertices is negligable