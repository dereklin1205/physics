from vpython import *

scene = canvas(background=vec(0.8, 0.8, 0.8), width=1200, height=300, center=vec(3, 0, 10), fov=0.004)
curve(pos=[vec(-7, 0, 0), vec(13, 0, 0)], color=color.white, radius=0.01)

def len(H,W,position):
    lens_surface1= shapes.ellipse(width=W, height=sqrt(H**2-(H-W)**2), angle1=pi/2, angle2=pi)
    circle1 = paths.arc(pos=position, radius=0.0000001, angle2=2*pi, up=vec(1, 0, 0))
    lens_surface2 = shapes.ellipse(width=W, height=sqrt(H**2-(H-W)**2), angle1=-pi/2, angle2=pi)
    circle2 = paths.arc(pos=position, radius=0.0000001, angle2=2 * pi, up=vec(1, 0, 0))
    extrusion(path=circle1, shape=lens_surface1, color=color.yellow, opacity=0.6)
    extrusion(path=circle2, shape=lens_surface2, color=color.yellow, opacity=0.6)

len1_pos=vec(0,0,0)
len2_pos=vec(6,0,0)
len(6,0.15,len1_pos)
len(6,0.15,len2_pos)
 

def refraction_vector(n1, n2, v_in, normal_v):
    # find the unit vector of velocity of the outgoing ray
    sin2 = (n1 / n2) * sin(diff_angle(normal_v, v_in))
    cos2 = sqrt(1 - sin2 ** 2)
    sign = norm(cross(normal_v, v_in)).z
    v_out = vec(-sign * sin2 * normal_v.y + cos2 * normal_v.x, sign * sin2 * normal_v.x + cos2 * normal_v.y, 0)
    return norm(v_out)

def solve_linear_equations(a1, b1, c1, a2, b2, c2):
    # Calculate the determinant
    determinant = a1 * b2 - a2 * b1

    # Check if the system has a unique solution
    if determinant == 0:
        return "The system of equations has no unique solution."

    # Calculate the solutions
    x = (c1 * b2 - c2 * b1) / determinant
    y = (a1 * c2 - a2 * c1) / determinant

    return x, y

print(refraction_vector(1, 1.5, norm(vec(-1, 1, 0)), norm(vec(0, 1, 0))))

thickness = 0.3

R1 = 4.0
g1center = vec(-R1 + thickness / 2, 0, 0)+len1_pos
g2center = vec(R1 - thickness / 2, 0, 0)+len1_pos

R2= 4.0
l1center = vec(-R2 + thickness / 2, 0, 0)+ len2_pos
l2center = vec(R2 - thickness / 2, 0, 0)+ len2_pos

nair = 1
nglass = [1.513,1.515,1.532]
ray_color=[color.red, color.green, color.blue]


for i in range(0,3):
    a=[]
    c=[]
    dt = 0.002
    for y_pos in range(-2,3):
        ray = sphere(pos=vec(-6, y_pos*0.5, 0), color=ray_color[i], radius=0.01, make_trail=True)
        ray.v = vector(1,0,0)

        state = 0
        while True:
            rate(5000)
            ray.pos = ray.pos + ray.v * dt

            # your code here
            if mag(ray.pos - g2center) < 4 and ray.pos.x < 0 and state == 0:
                # print('hit 1')
                state += 1
                ray.v = refraction_vector(1, nglass[i], ray.v, -norm(ray.pos - g2center))

            if mag(ray.pos - g1center) > 4 and ray.pos.x > 0 and state == 1:
                # print('hit 2')
                state += 1
                ray.v = refraction_vector(nglass[i], 1, ray.v, norm(ray.pos - g1center))
            
            if mag(ray.pos - l2center) < 4 and ray.pos.x > 0 and state == 2:
                state += 1
                ray.v = refraction_vector(1, nglass[i], ray.v, -norm(ray.pos - l2center))
            
            if mag(ray.pos - l1center) > 4 and ray.pos.x > 0 and state == 3:
                # print('hit 2')
                state += 1
                ray.v = -refraction_vector(nglass[i], 1, ray.v, norm(ray.pos - l1center))
                a.append(ray.v.y/ray.v.x)
                c.append(-ray.pos.y+ray.v.y/ray.v.x*ray.pos.x)

            if ray.pos.x < -20 and state==4:
                break
    print(a,c)
    sol=solve_linear_equations(a[0],-1,c[0],a[1],-1,c[1])
    print(sol)
    r=sol[1]
    img_pos=vec(sol[0],0, 0)
    img=cylinder(pos=img_pos,radius=r,axis=vec(0.1,0,0),opacity=0.3,color=ray_color[i])
