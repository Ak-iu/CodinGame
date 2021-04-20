import sys
import math
import re

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
#Write an action using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)
def find_valid_action(action):
    for i in valid_action:
        if re.findall(action,i):
            return i
    return False

def invert(s):
    return s[2]+" "+s[0]
inline=0


def can_win():
    rm = False
    for i in range(0,3):

        inline = re.findall(str(i)+"[0-9]",my_moves)
        m = find_valid_action(str(i)+" [0-9]")
        if len(inline)>1 and m :
            rm = m

        inline = re.findall("[0-9]"+str(i),my_moves)
        m = find_valid_action("[0-9] "+str(i))
        if len(inline)>1 and  m :
            rm = m

        if "00" in my_moves and "11" in my_moves and find_valid_action("2 2"):
            rm = find_valid_action("2 2")
        elif "11" in my_moves and "22" in my_moves and find_valid_action("0 0"):
            rm = find_valid_action("0 0")
        elif "22" in my_moves and "00" in my_moves and find_valid_action("1 1"):
            rm = find_valid_action("1 1")
        elif "20" in my_moves and "11" in my_moves and find_valid_action("0 2"):
            rm = find_valid_action("0 2")
        elif "11" in my_moves and "02" in my_moves and find_valid_action("2 0"):
            rm = find_valid_action("2 0")
        elif "02" in my_moves and "20" in my_moves and find_valid_action("1 1"):
            rm = find_valid_action("1 1")

    return rm


    return rm
def op_can_win():
    rm = False
    for i in range(0,3):

        inline = re.findall(str(i)+"[0-9]",op_moves)
        m = find_valid_action(str(i)+" [0-9]")
        if len(inline)>1 and m :
            rm = m

        inline = re.findall("[0-9]"+str(i),op_moves)   
        m = find_valid_action("[0-9] "+str(i))
        if len(inline)>1 and  m :
            rm = m

        if "00" in op_moves and "11" in op_moves and find_valid_action("2 2"):
            rm = m
        elif "11" in op_moves and "22" in op_moves and find_valid_action("0 0"):
            rm = m
        elif "22" in op_moves and "00" in op_moves and find_valid_action("1 1"):
            rm = m
        elif "20" in op_moves and "11" in op_moves and find_valid_action("0 2"):
            rm = m
        elif "11" in op_moves and "02" in op_moves and find_valid_action("2 0"):
            rm = m
        elif "02" in op_moves and "20" in op_moves and find_valid_action("1 1"):
            rm = m

    return rm


x=0
y=0

op_moves=""
my_moves=""
valid_action=[]

# game loop
while True:
    valid_action=[]
    opponent_row, opponent_col = [int(i) for i in input().split()]
    valid_action_count = int(input())
    for i in range(valid_action_count):
        row, col = [int(j) for j in input().split()]
        valid_action.append(str(col)+' '+str(row))
    op_moves+= str(opponent_col)+str(opponent_row)+' '


    print(my_moves, file=sys.stderr, flush=True)

    print(can_win() , file=sys.stderr, flush=True)
    print(op_can_win(), file=sys.stderr, flush=True)


    my_move = can_win()
    op_move = op_can_win()
    
    if my_move != False:
        my_moves += my_move.replace(' ','')+' '
        print(invert(my_move))
    elif op_move != False:
        my_moves += op_move.replace(' ','')+' '
        print(invert(op_move))
    else:
        my_moves += valid_action[0].replace(' ','')+' '
        print(invert(valid_action[0]))
