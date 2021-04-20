import sys
import math
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

def get_direction():
    if x < landing_site[0][0] - 300:
        return "RIGHT"
    elif x > landing_site[1][0] + 300:
        return "LEFT"
    else:
        return "DOWN"

def middle_of_landing_site():
    l = landing_site[1][0] - landing_site[0][0]
    return int(landing_site[0][0] + l/2)


def land_dist():
    return abs( x - middle_of_landing_site()) ,y - landing_site[0][1]


def find_landing_site():
    for i in range(1,len(surface)):
        p1 = surface[i-1]
        p2 = surface[i]
        if p1[1] ==  p2[1]:
            return (p1,p2)

def go_over_landing_zone():
    if abs(hs) < 40:
        if dist_x > 2000:
            angle = 20
        elif dist_x > 1000:
            angle = 10
        else:
            angle = 5
        power = 4
    else:
        if dist_x > 2000:
            angle = -30
        elif dist_x > 1000:
            angle = -20
        else:
            angle = -10
        power=4
        print("slow down", file=sys.stderr, flush=True)
    
    if direction == "RIGHT":
        angle = -angle
        
    
    print("go over", file=sys.stderr, flush=True)
    return angle,power

def stabilisation():
    if vs ==0:
        d = 1
    else:
        d = vs
    angle = abs(int(math.degrees(math.atan(hs/d))))
    if hs < 0:
        angle = -angle
    print("stab", file=sys.stderr, flush=True)
    return angle,4

def landing():
    if abs(hs)>5:
        angle,power = stabilisation()
    else:
        angle = 0
        print("vs",vs, file=sys.stderr, flush=True)
        if abs(vs) > 35:
            power = 4
        elif abs(vs) > 15:
            power = 3
        else:
            power = 2
        

    print("landing", file=sys.stderr, flush=True)
    return angle,power


surface=[]
n = int(input())  # the number of points used to draw the surface of Mars.
for i in range(n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]
    surface.append((land_x,land_y))



#init
dist_y = 0
dist_x = 0
power = 0
angle = 0
direction = ""
landing_site = find_landing_site()
# game loop
while True:
    # hs: the horizontal speed (in m/s), can be negative.
    # vs: the vertical speed (in m/s), can be negative.
    # f: the quantity of remaining fuel in liters.
    # r: the rotation angle in degrees (-90 to 90).
    # p: the thrust power (0 to 4).
    x, y, hs, vs, f, r, p = [int(i) for i in input().split()]
    direction = get_direction()
    dist_x,dist_y = land_dist()



    if direction == "RIGHT" or direction == "LEFT":
        angle,power = go_over_landing_zone()
    else:
        angle,power = landing()


    
    print(landing_site, file=sys.stderr, flush=True)
    print(dist_x,dist_y, file=sys.stderr, flush=True)


    print(angle,power)
