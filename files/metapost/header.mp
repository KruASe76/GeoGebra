numeric dot_diam;
dot_diam := 3;

color dot_color;
dot_color := background;

vardef Point(expr a) text t =
fill fullcircle scaled dot_diam shifted a withcolor dot_color;
draw fullcircle scaled dot_diam shifted a
enddef;

vardef Segment(expr a,b) =  draw (a--b) enddef;

vardef Circle(expr a,r) =  draw fullcircle scaled 2r shifted a enddef; 

vardef Polyline(text t) =
save _p;
path _p;
_p = origin for a = t: --a endfor;
draw subpath (1,length _p) of _p
enddef;

vardef Polygon(text t) =
save _p;
path _p;
_p = for a = t: a--endfor cycle;
draw _p
enddef;

numeric right_angle_size;
right_angle_size :=5;

vardef RightAngleMark(expr a,b,c)=
draw (unitvector(a-b)--unitvector(a-b)+unitvector(c-b)--unitvector(c-b)) scaled right_angle_size shifted b 
enddef;

numeric line_mark_size; line_mark_size=5;

def LineMark(expr a,b,n)=
draw image(
for i=1 upto n: draw (.5up--.5down) scaled line_mark_size shifted (2i,0); endfor;
currentpicture:=currentpicture shifted -center currentpicture;
) rotated angle(a-b) shifted 1/2[a,b]
enddef;

numeric angle_mark_radius;
angle_mark_radius := 12;

def AngleMark (expr a,b,c, n)   =
draw image(for m = 0 upto n-1:
draw fullcircle scaled (2 angle_mark_radius-3m) shifted b ;
endfor
clip currentpicture to (a--b--c--cycle);)
enddef;