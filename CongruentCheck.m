%%--CongruentCheck.m--%%
%{
Author: Peter Herbert 2017
%}
%--initialisation--%
r=(rand()*5)+5;%Radius of circumscribing circle
angle=zeros(1,3);
for i=1:1:3
    angle(i)=rand()*(2*pi);%Positions of vertices of triangle relative to circle
end
goal=CircSphereTri(r,angle);%Goal triangle at random place/orientation
target=CircSphereTri(r,angle);%Target triangle at random place/orientation
fig=figure();%Setup plotting
Plotter(goal,target, 'Step 1: Initial Arrangement', 1);%Plot triangles (goal, target)
%--goal translation to origin--%
Vone=zeros(3,3);
Uone=zeros(3,3);
for i=1:1:3
   Vone(1:3,i)=goal(1:3,1); %[v1,v1,v1], for column vector v1.
   Uone(1:3,i)=target(1:3,1); %[u1,u1,u1], for column vector u1.
end
Vdash=goal-Vone;%Translation of goal to origin
Udash=target-Uone;%Image of traget at origin
Plotter(Vdash,Udash, 'Step 2: Match First Vertex',2);%Plot triangles (Vdash, Udash)
%--Alignment(first rotation)--%
axis1=(Udash(1:3,2)+Vdash(1:3,2))/2;%Midpoint between second vertices
normaxis1=axis1/norm(axis1);%First unit axis
crossaxis1=[0,-normaxis1(3),normaxis1(2);...
           normaxis1(3),0,-normaxis1(1);...
           -normaxis1(2),normaxis1(1),0];%Cross-product matrix defined by axis
R1=eye(3)+2*(crossaxis1^2);%First rotation matrix
Trans1=R1*Vdash;%First rotation to match the second of the vertices
Plotter(Trans1,Udash, 'Step 3: Match Second Vertex',3);%Plot triangles (Trans1, Udash)
%--Alignment(second rotation)--%
normaxis2=Udash(1:3,2)/norm(Udash(1:3,2));%Second unit axis
crossaxis2=[0,-normaxis2(3),normaxis2(2);...
           normaxis2(3),0,-normaxis2(1);...
           -normaxis2(2),normaxis2(1),0];%Cross-product matrix defined by axis
v3v2=-(crossaxis2^2)*Trans1(1:3,3);%Perpendicular component of third vertex of goal
u3u2=-(crossaxis2^2)*Udash(1:3,3);%Perpendicular component of third vertex of target
xproduct=cross(v3v2,u3u2);
direction=dot((xproduct/norm(xproduct)),normaxis2);%Direction of rotation (+ is anticlockwise)
theta2=direction*acos(dot(u3u2,v3v2)/(norm(u3u2)*norm(v3v2)));%Directed angle of rotation 
R2=eye(3)+((crossaxis2)*(sin(theta2)))+(((crossaxis2)^2)*(1-cos(theta2)));%Second rotation matrix
Trans2=R2*Trans1;%Second rotation completing the alignment
Plotter(Trans2,Udash, 'Step 4: Match Third Vertex',4);%Plot triangles (Trans2, Udash)
%--Translation to target--%
Result=Trans2+Uone;
Plotter(Result,target, 'Step 5: Map onto Original Target Position',5);%Plot triangles (Result, target)
%--Check Result--%
Check=target-Result %If matrix of 0's, then successful.


