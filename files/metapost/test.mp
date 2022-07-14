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

beginfig(1)

u := 2cm;

% отрисовка элементов --------------------

Point((0.0u, 0.0u));
Point((1.0u, 1.0u));
Point((0.0u, 3.0u));
Point((-1.0u, 0.0u));
Point((0.0u, -2.0u));
Point((5.0u, 0.0u));
Point((-3.0u, 0.0u));
Point((3.0u, 0.0u));
Point((2.846153846153846u, 0.3846153846153847u));
Point((2.760095373268236u, 0.5997615668294116u));
Point((1.6698729810778064u, -4.232050807568877u));
Point((-0.5u, -1.0u));
Point((0.37274174053203635u, -0.33048208926034234u));
Point((2.5u, 3.0u));
Point((2.0u, -3.0u));
Point((-3.0u, -4.0u));
Point((2.5717967697244895u, -5.133974596215561u));
Point((3.8038475772933658u, -4.803847577293369u));
Point((4.13397459621556u, -3.571796769724492u));
Point((3.2320508075688776u, -2.669872981077808u));
Segment((0.0u, 3.0u), (-1.0u, 0.0u));
Segment((1.0u, 1.0u), (0.0u, -2.0u));
Segment((0.0u, -2.0u), (-1.0u, 0.0u));
Segment((-1.0u, 0.0u), (1.0u, 1.0u));
Circle((-3.0u, 0.0u), 2.0u);
Segment((0.0u, 3.0u), (2.5u, 3.0u));
Circle((1.6698729810778064u, -4.232050807568877u), 1.0u);
Circle((0.6065587146347143u, -3.286882570730571u), 1.4226665895948496u);
Segment((2.0u, -3.0u), (1.6698729810778064u, -4.232050807568877u));
Segment((1.6698729810778064u, -4.232050807568877u), (2.5717967697244895u, -5.133974596215561u));
Segment((2.5717967697244895u, -5.133974596215561u), (3.8038475772933658u, -4.803847577293369u));
Segment((3.8038475772933658u, -4.803847577293369u), (4.13397459621556u, -3.571796769724492u));
Segment((4.13397459621556u, -3.571796769724492u), (3.2320508075688776u, -2.669872981077808u));
Segment((3.2320508075688776u, -2.669872981077808u), (2.0u, -3.0u));

endfig;
end
