%{
Author: Peter Herbert 2017
%}
function Plotter(tri1, tri2, plot_title, step)
%{
PLOTTER takes in  the 3x3 matrix of vertex coordinates for a 'goal' 
triangle (TRI1) and a 'target' triangle (TRI2) and plots them in a figure. 
The other inputs include: STEP which denotes the step in the transformation 
process, allowing the triangles to be plotted inthe correct subplot of the 
figure; PLOT_TITLE, which is astring denoting the main title of the 
subplot.
%}
    %--Plot triangles--%
    %coordinates
    X1=tri1(1,1:3);Y1=tri1(2,1:3);Z1=tri1(3,1:3);
    X2=tri2(1,1:3);Y2=tri2(2,1:3);Z2=tri2(3,1:3);
    %positioning subplot
    subplot(2,10,[(4*step)-3,(4*step)-2]);
    %drawing lines
    hold on; grid on; 
    fill3(X1,Y1,Z1,[0;0;0]);%dark blue triangle is goal
    fill3(X2,Y2,Z2,[1;1;1]);%yellow triangle is target
    %drawing vertices
    plot3(tri1(1,1),tri1(2,1),tri1(3,1), 'r*'); 
    plot3(tri1(1,2),tri1(2,2),tri1(3,2), 'b*'); 
    plot3(tri1(1,3),tri1(2,3),tri1(3,3), 'g*');
    plot3(tri2(1,1),tri2(2,1),tri2(3,1), 'r*'); 
    plot3(tri2(1,2),tri2(2,2),tri2(3,2), 'b*'); 
    plot3(tri2(1,3),tri2(2,3),tri2(3,3), 'g*');
    %--Labels--%
    title(plot_title);
    xlabel('X axis');
    ylabel('Y axis');
    zlabel('Z axis');
    hold off;
end

