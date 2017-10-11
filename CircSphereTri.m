%{
Author: Peter Herbert 2017
%}
function [vertex]=CircSphereTri(r,angle)
%{
CIRCSPHERETRI generates a matrix comprising three column vectors of vertex
coordinates for a triangle. The function takes inputs of the radius of the 
circle circumscribing the triangle, and the angles (in a 1x3 matrix) 
defining the positions of the vertices relative to the circle. The output 
is a particular circumscribed triangle positioned with a random orientation
and position in 3D.
%}
    %--Centre of circle--%
    C=(rand(1,3)*5)+5;
    %--Orientation of circle in 3D space-%
    phi=randn()*(2*pi);
    theta=randn()*(2*pi);
    plane1=[cos(phi)*cos(theta);sin(phi)*cos(theta);-sin(theta)];
    plane2=[-sin(phi);cos(phi);0];
    %--Calculate position of each vertex using parametric equation--%
    vertex=zeros(3,3);
    for i=1:1:3
        vertex(1:3,i)=(r*cos(angle(i))*plane1)+(r*sin(angle(i))*plane2)+[C(1);C(2);C(3)];
    end    
end
