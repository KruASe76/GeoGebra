import numpy as np
from inspect import getmembers, isfunction

from lib_vars import *
from lib_elements import *

#--------------------------------------------------------------------------

class Command:
    def __init__(self, name, inputs, outputs = None):
        self.name = name
        self.inputs = toObjArray(inputs)        # могут храниться сами объекты, а также строки с именами или выражениями
        self.outputs = toObjArray(outputs)

    def __repr__(self):
        inputs_str = ' '.join([obj.name if hasattr(obj, "name") else str(obj) for obj in self.inputs])
        outputs_str = ' '.join([obj.name if hasattr(obj, "name") else str(obj) for obj in self.outputs])
        return "{}:\t{}\t>> {}".format(self.name, inputs_str, outputs_str)

    def checkParamsPrepaired(self, params):
        for obj in params:
            if type(obj) not in type_to_shortcut:
                #raise Exception("In command <{}> param ({} as {}) is not prepaired.".format(self.name, obj, type(obj)))
                return False
        return True

    def func(self):     # эта функция должна находить реализованную функцию в этом модуле и возвращать ссылку на нее
        #if not self.checkParamsPrepaired(self.inputs):
        #    raise Exception("In command <{}> inputs are not prepaired.".format(self.name))

        fname = strFullCommand(self.name, self.inputs)

        if fname in globals(): return globals()[fname]
        else: return None

#--------------------------------------------------------------------------        

def toObjArray(params):
    if params == None: return []
    elif not isinstance(params, list): return [params]
    else: return params

#--------------------------------------------------------------------------   

type_to_shortcut = {
    Point     : 'p',
    Polygon   : 'P',
    Circle    : 'c',
    Arc       : 'C',
    Line      : 'l',
    Ray       : 'r',
    Segment   : 's',
    Angle     : 'a',
    Vector    : 'v',

    int       : 'i',
    float     : 'i',
    Boolean   : 'b',
    Measure   : 'm',
    AngleSize : 'A'
}

def strFullCommand(name, params): # "Polygon", [Point, Point, int] -> "polygon_ppi"
    return "{}_{}".format(strCommand(name), strParams(params))

def strParams(params): # [Point, Point, int] -> "ppi"
    return ''.join(type_to_shortcut[type(x)] if type(x) in type_to_shortcut else '?' for x in params)

def strCommand(name): # "AreCollinear" -> "are_collinear"
    altered_name = [name[0].lower()]
    for x in name[1:]:
        if x.isupper(): altered_name += ['_', x.lower()]
        else: altered_name.append(x)
    return ''.join(altered_name)

#--------------------------------------------------------------------------

def angle_ppp(p1, p2, p3):
    return Angle(p2.a, p2.a-p1.a, p2.a-p3.a)

def angular_bisector_ll(l1, l2):
    x = intersect_ll(l1, l2)
    n1, n2 = l1.n, l2.n
    if np.dot(n1, n2) > 0: n = n1 + n2
    else: n = n1 - n2
    return [
        Line(vec, np.dot(vec, x.a))
        for vec in (n, vector_perp_rot(n))
    ]

def angular_bisector_ppp(p1, p2, p3):
    v1 = p2.a - p1.a
    v2 = p2.a - p3.a
    v1 /= np.linalg.norm(v1)
    v2 /= np.linalg.norm(v2)
    if np.dot(v1, v2) < 0: n = v1-v2
    else: n = vector_perp_rot(v1+v2)
    return Line(n, np.dot(p2.a, n))

def angular_bisector_ss(l1, l2):
    return angular_bisector_ll(l1, l2)

def are_collinear_ppp(p1, p2, p3):
    return Boolean(np.linalg.matrix_rank([p1.a-p2.a, p1.a-p3.a]) <= 1)

def are_concurrent_lll(l1, l2, l3):
    lines = l1,l2,l3
    
    differences = []
    for i in range(3):
        remaining = [l.n for l in lines[:i]+lines[i+1:]]
        prod = np.abs(np.cross(*remaining))
        differences.append((prod, i, lines[i]))

    l1, l2, l3 = tuple(zip(*sorted(differences)))[2]
    x = intersect_ll(l1, l2)
    return Boolean(np.isclose(np.dot(x.a, l3.n), l3.c))

def are_concurrent(o1, o2, o3):
    cand = []
    try:
        #if True:
        if isinstance(o1, Line) and isinstance(o2, Line):
            cand = intersect_ll(o1, o2)
        elif isinstance(o1, Line) and isinstance(o2, Circle):
            cand = intersect_lc(o1, o2)
        elif isinstance(o1, Circle) and isinstance(o2, Line):
            cand = intersect_cl(o1, o2)
        elif isinstance(o1, Circle) and isinstance(o2, Circle):
            cand = intersect_cc(o1, o2)
    except: pass

    if not isinstance(cand, (tuple,list)): cand = [cand]

    for p in cand:
        for obj in (o1,o2,o3):
            if not obj.contains(p.a): break
        else: return Boolean(True)

    return Boolean(False)

def are_concyclic_pppp(p1, p2, p3, p4):
    z1, z2, z3, z4 = (a_to_cpx(p.a) for p in (p1, p2, p3, p4))
    cross_ratio = (z1-z3)*(z2-z4)*(((z1-z4)*(z2-z3)).conjugate())
    return Boolean(np.isclose(cross_ratio.imag, 0))

def are_congruent_aa(a1, a2):
    #print(a1.angle, a2.angle)
    result = np.isclose((a1.angle-a2.angle+1)%(2*np.pi), 1)
    result = (result or np.isclose((a1.angle+a2.angle+1)%(2*np.pi), 1))
    return Boolean(result)

def are_complementary_aa(a1, a2):
    #print(a1.angle, a2.angle)
    result = np.isclose((a1.angle-a2.angle)%(2*np.pi), np.pi)
    result = (result or np.isclose((a1.angle+a2.angle)%(2*np.pi), np.pi))
    return Boolean(result)

def are_congruent_ss(s1, s2):
    l1, l2 = (
        np.linalg.norm(s.end_points[1] - s.end_points[0])
        for s in (s1, s2)
    )
    return Boolean(np.isclose(l1, l2))

def are_equal_mm(m1, m2):
    assert(m1.dim == m2.dim)
    return Boolean(np.isclose(m1.x, m2.x))

def are_equal_mi(m, i):
    assert(m.dim == 0)
    return Boolean(np.isclose(m.x, i))

def are_equal_pp(p1, p2):
    return Boolean(np.isclose(p1.a, p2.a).all())

def are_parallel_ll(l1, l2):
    if np.isclose(l1.n, l2.n).all(): return Boolean(True)
    if np.isclose(l1.n, -l2.n).all(): return Boolean(True)
    return Boolean(False)

def are_parallel_ls(l, s):
    return are_parallel_ll(l, s)

def are_parallel_rr(r1, r2):
    return are_parallel_ll(r1, r2)

def are_parallel_sl(s, l):
    return are_parallel_ll(s, l)

def are_parallel_ss(s1, s2):
    return are_parallel_ll(s1, s2)

def are_perpendicular_ll(l1, l2):
    if np.isclose(l1.n, l2.v).all(): return Boolean(True)
    if np.isclose(l1.n, -l2.v).all(): return Boolean(True)
    return Boolean(False)

def are_perpendicular_lr(l, r):
    return are_perpendicular_ll(l, r)

def are_perpendicular_rl(r, l):
    return are_perpendicular_ll(r, l)

def are_perpendicular_sl(s, l):
    return are_perpendicular_ll(s, l)

def are_perpendicular_ls(l, s):
    return are_perpendicular_ll(l, s)

def are_perpendicular_ss(s1, s2):
    return are_perpendicular_ll(s1, s2)

def area(*points):
    p0 = points[0].a
    vecs = [p.a - p0 for p in points[1:]]
    cross_sum = sum(
        np.cross(v1, v2)
        for v1, v2 in zip(vecs, vecs[1:])
    )
    return Measure(abs(cross_sum)/2, 2)

def area_P(polygon):
    points = [Point(p) for p in polygon.points]
    return area(*points)

def center_c(c):
    return Point(c.c)

def circle_pp(center, passing_point):
    return Circle(center.a, np.linalg.norm(center.a - passing_point.a))

def circle_ppp(p1, p2, p3):
    axis1 = line_bisector_pp(p1, p2)
    axis2 = line_bisector_pp(p1, p3)
    center = intersect_ll(axis1, axis2)
    return circle_pp(center, p1)

def circle_pm(p, m):
    assert(m.dim == 1)
    return Circle(p.a, m.x)

def circle_ps(p, s):
    return Circle(p.a, s.length)

def contained_by_pc(point, by_circle):
    return Boolean(by_circle.contains(point.a))

def contained_by_pl(point, by_line):
    return Boolean(by_line.contains(point.a))

def distance_pp(p1, p2):
    return Measure(np.linalg.norm(p1.a-p2.a), 1)

def equality_aa(a1, a2):
    return are_congruent_aa(a1, a2)

def equality_mm(m1, m2):
    assert(m1.dim == m2.dim)
    return Boolean(np.isclose(m1.x, m2.x))

def equality_ms(m, s):
    assert(m.dim == 1)
    return Boolean(np.isclose(m.x, s.length))

def equality_mi(m, i):
    assert(m.dim == 0 or i == 0)
    return Boolean(np.isclose(m.x, i))

def equality_pp(p1, p2):
    return are_equal_pp(p1, p2)

def equality_Pm(polygon, m):
    assert(m.dim == 2)
    return Boolean(np.isclose(area_P(polygon).x, m.x))

def equality_PP(poly1, poly2):
    return Boolean(np.isclose(area_P(poly1).x, area_P(poly2).x))

def equality_sm(s, m):
    return equality_ms(m,s)

def equality_ss(s1, s2):
    return Boolean(np.isclose(s1.length, s2.length))

def equality_si(s, i): # !!!
    pass # TODO

def intersect_ll(line1, line2):
    matrix = np.stack((line1.n, line2.n))
    b = np.array((line1.c, line2.c))
    assert(not np.isclose(np.linalg.det(matrix), 0))
    return Point(np.linalg.solve(matrix, b))

def intersect_lc(line, circle):

    # shift circle to center
    y = line.c - np.dot(line.n, circle.c)
    x_squared = circle.r_squared - y ** 2
    if np.isclose(x_squared, 0): return Point(y * line.n + circle.c)
    assert(x_squared > 0)

    x = np.sqrt(x_squared)
    return [
        Point(x * line.v + y * line.n + circle.c),
        Point(-x * line.v + y * line.n + circle.c),
    ]

def intersect_cc(circle1, circle2):
    center_diff = circle2.c - circle1.c
    center_dist_squared = np.dot(center_diff, center_diff)
    center_dist = np.sqrt(center_dist_squared)
    relative_center = (circle1.r_squared - circle2.r_squared) / center_dist_squared
    center = (circle1.c + circle2.c) / 2 + relative_center*center_diff / 2

    rad_sum  = circle1.r + circle2.r
    rad_diff = circle1.r - circle2.r
    det = (rad_sum ** 2 - center_dist_squared) * (center_dist_squared - rad_diff ** 2)
    if np.isclose(det, 0): return [Point(center)]
    assert(det > 0)
    center_deviation = np.sqrt(det)
    center_deviation = np.array(((center_deviation,),(-center_deviation,)))

    return [
        Point(center + center_dev)
        for center_dev in center_deviation * 0.5 * vector_perp_rot(center_diff) / center_dist_squared
    ]

def intersect_cl(c,l):
    return intersect_lc(l,c)

def intersect_Cl(arc, line):
    results = intersect_lc(line,arc)
    if not isinstance(results, (tuple, list)): results = (results,)
    return [x for x in results if arc.contains(x.a)]

def intersect_cs(circle, segment):
    results = intersect_lc(segment, circle)
    if not isinstance(results, (tuple, list)): results = (results,)
    return [x for x in results if segment.contains(x.a)]

def intersect_lr(line, ray):
    result = intersect_ll(line, ray)
    assert(ray.contains(result.a))
    return result

def intersect_ls(line, segment):
    result = intersect_ll(line, segment)
    assert(segment.contains(result.a))
    return result

def intersect_rl(ray, line):
    result = intersect_ll(ray, line)
    assert(ray.contains(result.a))
    return result

def intersect_rr(r1, r2):
    result = intersect_ll(r1, r2)
    assert(r1.contains(result.a))
    assert(r2.contains(result.a))
    return result

def intersect_rs(ray, segment):
    result = intersect_ll(ray, segment)
    assert(ray.contains(result.a))
    assert(segment.contains(result.a))
    return result

def intersect_sl(segment, line):
    return intersect_ls(line, segment)

def intersect_sr(segment, ray):
    return intersect_rs(ray, segment)

def intersect_ss(s1, s2):
    result = intersect_ll(s1, s2)
    assert(s1.contains(result.a))
    assert(s2.contains(result.a))
    return result

def line_bisector_pp(p1, p2):
    p = (p1.a + p2.a) / 2
    n = p2.a - p1.a
    assert((n != 0).any())
    return Line(n, np.dot(n, p))

def line_bisector_s(segment):
    p1, p2 = segment.end_points
    p = (p1 + p2) / 2
    n = p2 - p1
    return Line(n, np.dot(n, p))

def line_pl(point, line):
    return Line(line.n, np.dot(line.n, point.a))

def line_pp(p1, p2):
    assert((p1.a != p2.a).any())
    n = vector_perp_rot(p1.a - p2.a)
    return Line(n, np.dot(p1.a, n))

def line_pr(point, ray):
    return line_pl(point, ray)

def line_ps(point, segment):
    return line_pl(point, segment)

def midpoint_pp(p1, p2):
    return Point((p1.a+p2.a)/2)

def midpoint_s(segment):
    p1, p2 = segment.end_points
    return Point((p1 + p2) / 2)

def minus_a(angle):
    return AngleSize(-angle.angle)

def minus_A(anglesize):
    return AngleSize(-anglesize.x)

def minus_m(m):
    return Measure(-m.x, m.dim)

def minus_mm(m1, m2):
    assert(m1.dim == m2.dim)
    return Measure(m1.x - m2.x, m1.dim)

def minus_ms(m, s):
    assert(m.dim == 1)
    return Measure(m.x - s.length, 1)

def minus_sm(s, m):
    assert(m.dim == 1)
    return Measure(s.length - m.x, 1)

def minus_ss(s1, s2):
    return Measure(s1.length - s2.length, 1)

def mirror_cc(circle, by_circle):
    center_v = circle.c - by_circle.c
    denom = square_norm(center_v) - circle.r_squared
    if np.isclose(denom, 0):
        return Line(center_v, circle.r_squared / 2 + np.dot(center_v, by_circle.c))
    else:
        return Circle(
            center = (by_circle.r_squared/denom) * center_v + by_circle.c,
            r = by_circle.r_squared * circle.r / abs(denom)
        )

def mirror_cl(circle, by_line):
    return Circle(
        center = circle.c + by_line.n*2*(by_line.c - np.dot(circle.c, by_line.n)),
        r = circle.r,
    )

def mirror_cp(circle, by_point):
    return Circle(
        center = 2 * by_point.a - circle.c,
        r = circle.r
    )

def mirror_ll(line, by_line):
    n = line.n - by_line.n * 2 * np.dot(line.n, by_line.n)
    return Line(n, line.c + 2 * by_line.c * np.dot(n, by_line.n) )

def mirror_lp(line, by_point):
    return Line(line.n, 2 * np.dot(by_point.a, line.n) - line.c)

def mirror_pc(point, by_circle):
    v = point.a - by_circle.c
    assert(not np.isclose(v, 0).all())
    return Point(by_circle.c + v * (by_circle.r_squared / square_norm(v)) )

def mirror_pl(point, by_line):
    return Point(point.a + by_line.n * 2 * (by_line.c - np.dot(point.a, by_line.n)))

def mirror_pp(point, by_point):
    return Point(2 * by_point.a - point.a)

def mirror_ps(point, segment):
    return mirror_pl(point, segment)

def orthogonal_line_pl(point, line):
    return Line(line.v, np.dot(line.v, point.a))

def orthogonal_line_pr(point, ray):
    return orthogonal_line_pl(point, ray)

def orthogonal_line_ps(point, segment):
    return orthogonal_line_pl(point, segment)

def point_():
    return Point(np.random.normal(size = 2))

def point_ii(x, y):
    return Point([x,y])

def point_c(circle):
    return Point(circle.c + circle.r * random_direction())

def point_l(line):
    return Point(line.c * line.n + line.v * np.random.normal() )

def point_s(segment):
    return Point(interpolate(segment.end_points[0], segment.end_points[1], np.random.random()))

def polar_pc(point, circle):
    n = point.a - circle.c
    assert(not np.isclose(n, 0).all())
    return Line(n, np.dot(n, circle.c) + circle.r_squared)

def polygon_ppi(p1, p2, n):
    p1c, p2c = (a_to_cpx(p.a) for p in (p1, p2))
    alpha = 2 * np.pi/n
    center = p2c + (p1c-p2c)/(1-np.exp(-alpha * 1j))
    v = p2c - center
    points = [Point(cpx_to_a(center + v * np.exp(i * alpha * 1j))) for i in range(1, n - 1)]
    raw_points = [p.a for p in [p1, p2] + points]
    segments = [
        Segment(p1, p2)
        for p1, p2 in zip(raw_points, raw_points[1:] + raw_points[:1])
    ]
    return [Polygon(raw_points)] + segments + points

def polygon(*points):
    raw_points = [p.a for p in points]
    segments = [
        Segment(p1, p2)
        for p1, p2 in zip(raw_points, raw_points[1:] + raw_points[:1])
    ]
    return [Polygon(raw_points)] + segments

def power_mi(m, i):
    assert(i == 2)
    return Measure(m.x ** i, m.dim*i)

def power_si(s, i):
    return Measure(s.length ** i, i)

def product_mm(m1, m2):
    return Measure(m1.x * m2.x, m1.dim + m2.dim)

def product_ms(m, s):
    return Measure(m.x * s.length, m.dim + 1)

def product_mf(m, f):
    return Measure(m.x * f, m.dim)

def product_sm(s, m):
    return product_ms(m,s)

def product_ss(s1, s2):
    return Measure(s1.length * s2.length, 2)

def product_fm(f, m):
    return product_mf(m, f)

def product_ff(f1, f2):
    return Measure(f1 * f2, 0)

def product_iA(i, angle_size):
    return AngleSize(angle_size.x * i)

def product_im(i, m):
    return Measure(i * m.x, m.dim)

def product_is(i, s):
    return Measure(i * s.length, 1)

def product_if(i, f):
    return Measure(i * f, 0)

def prove_b(x):
    print(x.b)
    return x

def radius_c(circle):
    return Measure(circle.r, 1)

def ratio_mm(m1, m2):
    assert(not np.isclose(m1.x, 0))
    return Measure(m1.x / m2.x, m1.dim - m2.dim)

def ratio_ms(m, s):
    return Measure(m.x / s.length, m.dim - 1)

def ratio_mi(m, i):
    assert(i != 0)
    return Measure(m.x / i, m.dim)

def ratio_sm(s, m):
    assert(not np.isclose(m.x, 0))
    return Measure(s.length / m.x, 1 - m.dim)

def ratio_ss(s1, s2):
    return Measure(s1.length / s2.length, 0)

def ratio_si(s, i):
    assert(i != 0)
    return Measure(s.length / i, 1)

def ratio_ii(i1, i2):
    assert(i2 != 0)
    return Measure(i1 / i2, 0)

def ray_pp(p1, p2):
    return Ray(p1.a, p2.a - p1.a)

def rotate_pap(point, angle, by_point):
    return Point(by_point.a + rotate_vec(point.a - by_point.a, angle.angle))

def rotate_pAp(point, angle_size, by_point):
    return Point(by_point.a + rotate_vec(point.a - by_point.a, angle_size.x))

def segment_pp(p1, p2):
    return Segment(p1.a, p2.a)

def semicircle(p1, p2):
    vec = a_to_cpx(p1.a - p2.a)
    return Arc(
        (p1.a + p2.a) / 2,
        abs(vec) / 2,
        [np.angle(v) for v in (-vec, vec)]
    )

def sum_mm(m1, m2):
    assert(m1.dim == m2.dim)
    return Measure(m1.x + m2.x, m1.dim)

def sum_ms(m, s):
    assert(m.dim == 1)
    return Measure(m.x + s.length, 1)

def sum_mi(m, i):
    assert(m.dim == 0)
    return Measure(m.x + i, 0)

def sum_ss(s1, s2):
    return Measure(s1.length + s2.length, 1)

def tangent_pc(point, circle):
    polar = polar_pc(point, circle)
    intersections = intersect_lc(polar, circle)
    if type(intersections) in (tuple, list) and len(intersections) == 2:
        return [line_pp(point, x) for x in intersections]
    else: return polar

def touches_cc(c1, c2):
    lens = c1.r, c2.r, np.linalg.norm(c1.c-c2.c)
    return Boolean(np.isclose(sum(lens), 2 * max(lens)))

def touches_lc(line, circle):
    return Boolean(
        np.isclose(circle.r, np.abs(np.dot(line.n, circle.c) - line.c) )
    )

def touches_cl(circle, line):
    return touches_lc(line, circle)

def translate_pv(point, vector):
    return Point(point.a + vector.v)

def vector_pp(p1, p2):
    return Vector((p1.a, p2.a))
