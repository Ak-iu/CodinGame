import sys
import math


def dist(l,l2):
    x1 = l[0]
    y1 = l[1]
    x2 = l2[0]
    y2 = l2[1]
    vx = abs(x1-x2)
    vy = abs(y1-y2)
    return int(math.sqrt(pow(vx,2)+pow(vy,2)))

def pop_smallest(d):
    item =  min(d.items(), key=lambda x: x[1])
    del d[item[0]]
    return item[0]

def humans_in_danger():
    humans_focus = []
    nearest_zombie = {}
    for h_key in humans:
        h=humans[h_key]
        min_dist = float("inf")
        for z_key in zombies:
            z = zombies[z_key]
            if dist(z,h) < min_dist:
                min_dist = dist(z,h)
        
        nearest_zombie[h_key] = min_dist


    print(nearest_zombie,humans_focus, file=sys.stderr, flush=True)
    while len(nearest_zombie) != 0:
        humans_focus.append(pop_smallest(nearest_zombie))

    print("Are focus : ",humans_focus, file=sys.stderr, flush=True)
    return humans_focus
    



def can_save(h):
    for key in zombies:
        z = zombies[key]
        if dist(ash,h)*0.4 - 950 >= dist(z,h):
            return False
    return True

def show_savable_humans():
    for key in humans:
        h=humans[key]
        print(key," : ",h," : ",can_save(h), file=sys.stderr, flush=True)

def r_deads():
    for key in humans:
        h=humans[key]
        for z_key in zombies:
            z=zombies[z_key]
            if dist(z,h) == 0:
                deads[key] = h
    
    for key in deads:
        if key in humans:
            del humans[key]

def kill_zombies():
    for z_key in zombies:
        z = zombies[z_key]
        if dist(ash,z) < 2000:
            dead_zombies[z_key]=z

def r_dead_zombies():
    for z_key in dead_zombies:
        if z_key in zombies:
            del zombies[z_key]

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

humans_focus=[]
humans={}
deads={}
dead_zombies={}
zombies={}
while True:
    x, y = [int(i) for i in input().split()]
    ash = [x,y]
    human_count = int(input())
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        humans[str(human_id)] = [human_x,human_y]
    zombie_count = int(input())
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
        zombies[zombie_id]  = [zombie_x, zombie_y, zombie_xnext, zombie_ynext]
    



    
    r_deads()
    kill_zombies()
    r_dead_zombies()
    show_savable_humans()
    humans_focus = humans_in_danger()


    keys = list(humans.keys())
    z_keys = list(zombies.keys())
    
    
   
    for key in humans_focus:
        h = humans[key]
        if can_save(h) and key in humans:
            print("I protect : ",key, file=sys.stderr, flush=True)
            x = h[0]
            y = h[1]
            break

   
    print(x,y)
