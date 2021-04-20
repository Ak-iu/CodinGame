import sys
import math

# To debug: print("Debug messages...", file=sys.stderr, flush=True)

alpha ="ABCDEFGHIJKLMNOPQRSTUVWXYZ "

def action_on_rune(c,pos):
    c_rune = runes[pos]
    i1 = alpha.index(c_rune)
    i2 = alpha.index(c)

    if i1>i2:
        if i1-i2 < i2 - i1 + 27:
            action = "-"*(i1-i2)+"."
        else:
            action = "+"*(i2 - i1 + 27)+"."
    else:
        if i2-i1 < i1 - i2 + 27:
            action = "+"*(i2-i1)+"."
        else:
            action = "-"*(i1 - i2 + 27)+"."
    return action

def show_potential_action():
    for i in potential_action:
        print(i,potential_action[i], file=sys.stderr, flush=True)

def get_smallest_action():
    indice = 0
    action_size = float("inf")
    action = None
    for k in potential_action:
        a = potential_action[k]
        if len(a) < action_size:
            action_size = len(a)
            indice = k
            action = a
    return indice,action

def get_potential_action(c):
    ind = 0
    for i in range(0,15):
        a = ">"*i + action_on_rune(c, (rune+ind) % 30 )
        potential_action[ (rune+ind) % 30 ] = a
        ind+=1
    for i in range(29,14,-1):
        a = "<"*(i-14) + action_on_rune(c, (rune+ind) % 30)
        potential_action[  (rune+ind) % 30  ] = a
        ind+=1
    return potential_action

#init
runes={}
for i in range(0,30):
    runes[i]=" "
rune = 0
action = ""
magic_phrase = input()
print(magic_phrase,action, file=sys.stderr, flush=True)

potential_action={}
for i in magic_phrase:
    potential_action = get_potential_action(i)
    #show_potential_action()
    ind,a =  get_smallest_action()
    print("action : ",ind,a, file=sys.stderr, flush=True)
    runes[ind]=i
    rune=ind
    action += a

print(action)
