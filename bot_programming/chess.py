import sys
import math
import re 
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

#function

def value_of_piece_on(case):
    p = pieces[case].lower()
    return int(value_of_pieces[p])

def value_of(move):
    case1 = move[0:2]
    case2 = move[2:4]
    value = 0
    if can_eat(move):
        value += value_of_piece_on(case2)
    if op_can_trade(move):
        value -= value_of_piece_on(case1)
    return value

def get_higher_value_check_move():
    max_value = -float("inf")
    next_move = check_moves_value[0]
    for move in check_moves_value:
        if moves_values[move] > max_value:
            max_value = moves_values[move]
            next_move = move
    return next_move

def get_higher_value_move():
    max_value = -float("inf")
    next_move = moves[0]
    for move in moves_values:
        if moves_values[move]>max_value:
            max_value = moves_values[move]
            next_move = move
    return next_move,max_value

def op_can_eat_my_queen():
    for case in op_can_eat_on:
        if case in my_pieces and my_pieces[case].lower() =="q":
            return True
    return False

def get_rook_in_danger():
    for case in op_can_eat_on:
        if case in my_pieces and my_pieces[case].lower() =="r":
            return case
    return False
def get_night_in_danger():
    for case in op_can_eat_on:
        if case in my_pieces and my_pieces[case].lower() =="n":
            return case
    return False
def get_bishop_in_danger():
    for case in op_can_eat_on:
        if case in my_pieces and my_pieces[case].lower() =="b":
            return case
    return False

def best_move_with(case):
    m = value_move
    value = -float("inf")
    for move in moves:
        if move[0:2] == case:
            if value_of(move) > value:
                value = value_of(move)
                m = move
    return m,value

def get_mate_moves():
    mate_moves = []
    for move in moves:
        case1 = str(move[0:2])
        case2 = move[2:4]
        p = my_pieces[case1].lower()
        if p!="k":
            del_op = False
            #temp
            del my_pieces[case1]
            my_pieces[case2] = p
            if case2 in op_pieces:
                del_op = op_pieces[case2]
                del op_pieces[case2] 
            op_moves_no_king = get_op_moves_no_king()
            #test
            if can_eat_king_on(case2,p):
                op_king_moves = get_op_king_moves()
                if len(op_king_moves) < 1 and case2 not in op_moves_no_king:
                    mate_moves.append(move)
            #restore
            my_pieces[case1] = p
            del my_pieces[case2]
            if del_op != False:
                op_pieces[case2]=del_op
        
    return mate_moves

def is_stalemate_move(move):
    b = False
    case1 = str(move[0:2])
    case2 = move[2:4]
    p = my_pieces[case1].lower()

    #temp
    print("del",case1, file=sys.stderr, flush=True)
    del my_pieces[case1]
    print("add",case2, file=sys.stderr, flush=True)
    my_pieces[case2] = p
    #test
    if not can_eat_king_on(case2,p):
        op_king_moves = get_op_king_moves()
        if len(op_king_moves) < 1:
            b = True
    #restore
    print("add",case1, file=sys.stderr, flush=True)
    my_pieces[case1] = p
    print("del",case2, file=sys.stderr, flush=True)
    del my_pieces[case2]

    return b

def get_king_pos():
    for case in my_pieces:
        if my_pieces[case].lower() == "k":
            return case
    return False

def get_op_king_moves():
    op_king_moves = []
    can_eat_on_case = get_moves()

    for case in op_can_eat_on:
        if 'k' in op_can_eat_on[case] and case not in op_pieces and case not in can_eat_on_case:
            op_king_moves.append(case)
    return op_king_moves

def get_no_value_moves():
    no_value_moves = []
    for move in moves_values:
        if moves_values[move] == 0:
            no_value_moves.append(move)
    return no_value_moves

def get_value_moves():
    value_moves = []
    for move in moves_values:
        if moves_values[move] > 0:
            value_moves.append(move)
    return value_moves

def get_check_moves_with_value():
    check_moves = []
    for move in value_moves:
        case = move[2:4]
        p = pieces[move[0:2]]
        eatable_case = on_case_piece_can_eat(case,p)

        for c in eatable_case:
            if c in op_pieces and op_pieces[c].lower() == "k":
                check_moves.append(move)
        
    return check_moves

def get_check_moves_no_value():
    check_moves = []
    for move in no_value_moves:
        case = move[2:4]
        p = pieces[move[0:2]]

        if can_eat_king_on(case,p):
            check_moves.append(move)
        
    return check_moves

def get_developpement_moves():
    dev_moves = []
    
    for move in no_value_moves:
        case1 = move[0:2]
        case2 = move[2:4]
        p = pieces[case1].lower()
        op_king = get_op_king_case()
        
        d = dist(case1,op_king) - dist(case2,op_king)
        
        if p !="p" and p !="k" and d > 0:
            dev_moves.append(move)
   
    return dev_moves

def get_pawn_moves_no_value():
    pawn_moves_no_value = []
    for move in no_value_moves:
        case = move[0:2]
        if pieces[case].lower() == "p":
            pawn_moves_no_value.append(move)
    return pawn_moves_no_value

def get_moves_values():
    moves_values = {}
    for move in moves:
        moves_values[move] = value_of(move)
    return moves_values

def can_eat(move):
    case = move[2:4]
    if case in op_pieces:
        return True
    else:
        return False

def op_can_trade(move):
    case = move[2:4]
    if op_can_eat(case):
        return True
    else:
        return False
    
def op_can_eat(case):
    if case in op_can_eat_on:
        return True
    else:
        return False

def valid_case(case):
    if len(case)!=2 :
        return False
    col = case[0]
    row = case[1]
    return (valid_column(col) and valid_row(row))

def valid_row(r):
    if int(r) > 0 and int(r) < 9:
        return True
    else:
        return False
def valid_column(c):
    if ord(c) > 96 and ord(c) < 105:
        return True
    else:
        return False

def previous_col(c):
    return chr(ord(c)-1)

def next_col(c):
    return chr(ord(c)+1)

def get_op_king_case():
    for case in op_pieces:
        if op_pieces[case].lower() == "k":
            return case
    return False

def dist(case1,case2):
    col_1 = case1[0]
    row_1 = int(case1[1])
    col_2 = case2[0]
    row_2 = int(case2[1])

    x_dist = abs(row_1 - row_2)
    y_dist = abs(ord(col_1) - ord(col_2))

    return x_dist + y_dist

def catch_the_king():
    up_dist_max = -float("inf")
    m = ""
    op_king_case = get_op_king_case()
    
    for move in no_value_moves:
        case1 = move[0:2]
        case2 = move[2:4]
        ud = dist(case1,op_king_case) - dist(case2,op_king_case)
        if ud > up_dist_max and not is_stalemate_move(move):
            up_dist_max = ud
            m = move
    
    return m,up_dist_max

def can_eat_king_on(case,p):
    eatable_case = on_case_piece_can_eat(case,p)
    for c in eatable_case:
        if c in op_pieces and op_pieces[c].lower() == "k":
            return True
    return False
        
def on_case_piece_can_eat(case,p):
    piece_eat_on = []
    col = case[0]
    row = int(case[1])
    p = p.lower()

    if p == "p":
        if color == "b" and row+1<9 :
            if valid_column(previous_col(col)) :
                piece_eat_on.append(previous_col(col)+str(row+1))
            if valid_column(next_col(col))  :
                piece_eat_on.append(next_col(col)+str(row+1))
        elif color == "w" and row-1>0:
            if valid_column(previous_col(col)) :    
                piece_eat_on.append(previous_col(col)+str(row-1)) 
            if valid_column(next_col(col))  :         
                piece_eat_on.append(next_col(col)+str(row-1))
    elif p == "n":
        if valid_case(previous_col(col)+str(row+2)):
            piece_eat_on.append(previous_col(col)+str(row+2))
        if valid_case(next_col(col)+str(row+2)):
            piece_eat_on.append(next_col(col)+str(row+2))
        if valid_case(previous_col(col)+str(row-2)):
            piece_eat_on.append(previous_col(col)+str(row-2))
        if valid_case(next_col(col)+str(row-2)):
            piece_eat_on.append(next_col(col)+str(row-2))
        if valid_case(previous_col(previous_col(col))+str(row+1)):
            piece_eat_on.append(previous_col(previous_col(col))+str(row+1))
        if valid_case(previous_col(previous_col(col))+str(row-1)):
            piece_eat_on.append(previous_col(previous_col(col))+str(row-1))
        if valid_case(next_col(next_col(col))+str(row+1)):
            piece_eat_on.append(next_col(next_col(col))+str(row+1))
        if valid_case(next_col(next_col(col))+str(row-1)):
            piece_eat_on.append(next_col(next_col(col))+str(row-1))
    elif p == "b":
        #left-up
        for i in range(1,8):
            if valid_case(chr(ord(col)-i)+str(row+i)):
                piece_eat_on.append(chr(ord(col)-i)+str(row+i))
            else:
                break
            if chr(ord(col)-i)+str(row+i) in pieces:
                break
        #right-up
        for i in range(1,8):
            if valid_case(chr(ord(col)+i)+str(row+i)):
                piece_eat_on.append(chr(ord(col)+i)+str(row+i))
            else:
                break
            if chr(ord(col)+i)+str(row+i) in pieces:
                break
        #left_down
        for i in range(1,8):
            if valid_case(chr(ord(col)-i)+str(row-i)):
                piece_eat_on.append(chr(ord(col)-i)+str(row-i))
            else:
                break
            if chr(ord(col)-i)+str(row-i) in pieces:
                break
        #right_down
        for i in range(1,8):
            if valid_case(chr(ord(col)+i)+str(row-i)):
                piece_eat_on.append(chr(ord(col)+i)+str(row-i))
            else:
                break
            if chr(ord(col)+i)+str(row-i) in pieces:
                break
    elif p == "r":
        #right
        for i in range(1,8):
            if valid_case(chr(ord(col)+i)+str(row)):
                piece_eat_on.append(chr(ord(col)+i)+str(row))
            else:
                break
            if chr(ord(col)+i)+str(row) in pieces:
                break
        #left
        for i in range(1,8):
            if valid_case(chr(ord(col)-i)+str(row)):
                piece_eat_on.append(chr(ord(col)-i)+str(row))
            else:
                break
            if chr(ord(col)-i)+str(row) in pieces:
                break
        #up
        for i in range(1,8):
            if valid_case(col+str(row+i)):
                piece_eat_on.append(col+str(row+i))
            else:
                break
            if col+str(row+i) in pieces:
                break
        #down
        for i in range(1,8):
            if valid_case(col+str(row-i)):
                piece_eat_on.append(col+str(row-i))
            else:
                break
            if col+str(row-i) in pieces:
                break
    elif p == "q":
        #right
        for i in range(1,8):
            if valid_case(chr(ord(col)+i)+str(row)):
                piece_eat_on.append(chr(ord(col)+i)+str(row))
            else:
                break
            if chr(ord(col)+i)+str(row) in pieces:
                break
        #left
        for i in range(1,8):
            if valid_case(chr(ord(col)-i)+str(row)):
                piece_eat_on.append(chr(ord(col)-i)+str(row))
            else:
                break
            if chr(ord(col)-i)+str(row) in pieces:
                break
        #up
        for i in range(1,8):
            if valid_case(col+str(row+i)):
                piece_eat_on.append(col+str(row+i))
            else:
                break
            if col+str(row+i) in pieces:
                break
        #down
        for i in range(1,8):
            if valid_case(col+str(row-i)):
                piece_eat_on.append(col+str(row-i))
            else:
                break
            if col+str(row-i) in pieces:
                break
        #left-up
        for i in range(1,8):
            if valid_case(chr(ord(col)-i)+str(row+i)):
                piece_eat_on.append(chr(ord(col)-i)+str(row+i))
            else:
                break
            if chr(ord(col)-i)+str(row+i) in pieces:
                break
        #right-up
        for i in range(1,8):
            if valid_case(chr(ord(col)+i)+str(row+i)):
                piece_eat_on.append(chr(ord(col)+i)+str(row+i))
            else:
                break
            if chr(ord(col)+i)+str(row+i) in pieces:
                break
        #left_down
        for i in range(1,8):
            if valid_case(chr(ord(col)-i)+str(row-i)):
                piece_eat_on.append(chr(ord(col)-i)+str(row-i))
            else:
                break
            if chr(ord(col)-i)+str(row-i) in pieces:
                break
        #right_down
        for i in range(1,8):
            if valid_case(chr(ord(col)+i)+str(row-i)):
                piece_eat_on.append(chr(ord(col)+i)+str(row-i))
            else:
                break
            if chr(ord(col)+i)+str(row-i) in pieces:
                break

    elif p == "k":
        if valid_case(col+str(row-1)):
            piece_eat_on.append(col+str(row-1))
        if valid_case(col+str(row+1)):
            piece_eat_on.append(col+str(row+1))
        if valid_case(previous_col(col)+str(row)):
            piece_eat_on.append(previous_col(col)+str(row))
        if valid_case(previous_col(col)+str(row-1)):
            piece_eat_on.append(previous_col(col)+str(row-1))
        if valid_case(previous_col(col)+str(row+1)):
            piece_eat_on.append(previous_col(col)+str(row+1))
        if valid_case(next_col(col)+str(row)):
            piece_eat_on.append(next_col(col)+str(row))
        if valid_case(next_col(col)+str(row-1)):
            piece_eat_on.append(next_col(col)+str(row-1))
        if valid_case(next_col(col)+str(row+1)):
            piece_eat_on.append(next_col(col)+str(row+1))

    return piece_eat_on

def get_queen_moves():
    ms=[]
    for move in moves:
        if my_pieces[move[0:2]].lower() == "q":
            ms.append(move)
    return ms

def get_best_move_with_queen():
    qm = get_queen_moves()
    value = -float("inf")
    m = False
    for move in qm:
        if value_of(move) > value:
            value = value_of(move)
            m = move
    if value == 0:
        for move in dev_moves:
            if my_pieces[move[0:2]].lower() == "q":
                m = move
    return m

def get_moves():
    actual_moves = {}
    for case in my_pieces:
        col = case[0]
        row = int(case[1])
        p = my_pieces[case].lower()
        for case in on_case_piece_can_eat(case,p):
            if case in actual_moves:
                actual_moves[case]+=p
            else:
                actual_moves[case]=p
    return actual_moves

def get_op_moves_no_king():
    op_moves = {}
    for case in op_pieces:
        col = case[0]
        row = int(case[1])
        p = op_pieces[case].lower()
        if p != "k":
            for case in on_case_piece_can_eat(case,p):
                if case in op_moves:
                    op_moves[case]+=p
                else:
                    op_moves[case]=p
    return op_moves
def get_op_moves():
    op_moves = {}
    for case in op_pieces:
        col = case[0]
        row = int(case[1])
        p = op_pieces[case].lower()
        for case in on_case_piece_can_eat(case,p):
            if case in op_moves:
                op_moves[case]+=p
            else:
                op_moves[case]=p
    return op_moves


def get_pieces_pos():
    pieces = {}
    my_pieces = {}
    op_pieces = {}
    row_number = 8
    col_id= 0
    col_alpha = columns[col_id]

    for row in board.split("/"):
        for c in row:
            if c.isdigit() :
                col_id += int(c)-1
            else:
                pos = col_alpha+str(row_number)
                pieces[pos] =  c
                if color == "w":
                    if c.isupper():
                        my_pieces[pos] = c
                    else:
                        op_pieces[pos] = c
                else:
                    if c.isupper():
                        op_pieces[pos] = c
                    else:
                        my_pieces[pos] = c
            col_id+=1
            col_alpha = columns[col_id % 8]
        row_number-=1
    
    return pieces,my_pieces,op_pieces
def find(p):
    for case in my_pieces:
        if my_pieces[case].lower() == p:
            return case
    return False

def get_starting_moves():
    mvs = []
    q_case = find("q")

    if color == 'w' and q_case:
        q_pawn_case1 = q_case[0] + str(int(q_case[1])+1)
        q_pawn_case2 = q_case[0] + str(int(q_case[1])+3)
        q_pawn_move = q_pawn_case1 + q_pawn_case2
        if "e2e4" in moves and my_pieces["e2"].lower() == "p":
            mvs.append("e2e4")
        if "d2d3" in moves and my_pieces["d2"].lower() == "p":
            mvs.append("d2d3")
        if q_pawn_move in moves:
            mvs.append(q_pawn_move)
    elif q_case:
        q_pawn_case1 = q_case[0] + str(int(q_case[1])-1)
        q_pawn_case2 = q_case[0] + str(int(q_case[1])-3)
        q_pawn_move = q_pawn_case1 + q_pawn_case2
        if "e7e5" in moves and my_pieces["e7"].lower() == "p":
            mvs.append("e7e5")
        if "d7d6" in moves and my_pieces["d7"].lower() == "p":
            mvs.append("d7d6")
        if q_pawn_move in moves:
            mvs.append(q_pawn_move)        
    return mvs
#init
columns="abcdefgh"
constants_count = int(input())
for i in range(constants_count):
    name, value = input().split()
print("fen","moves")
moves = []
op_can_eat_on = []
moves_values = {}
pieces = {}
my_pieces = {}
op_pieces = {}
value_of_pieces = {'p':1,'n':3,'b':3,'r':5,'q':9,'k':999}


# game loop
while True:
    inputs = input().split()
    board = inputs[0]
    color = inputs[1]
    castling = inputs[2]
    en_passant = inputs[3]
    half_move_clock = int(inputs[4])
    full_move = int(inputs[5])
    movesCount = int(input())
    
    moves = []
    for i in range(movesCount):
        moves.append(input())
    pieces,my_pieces,op_pieces = get_pieces_pos()
    op_can_eat_on = get_op_moves()
    moves_values = get_moves_values()
    
    value_move,value = get_higher_value_move()
    
    value_moves = get_value_moves()
    no_value_moves = get_no_value_moves()
    
    
    pawn_moves_no_value = get_pawn_moves_no_value()
    check_moves_0 = get_check_moves_no_value()
    check_moves_value = get_check_moves_with_value()
    dev_moves = get_developpement_moves()
    mate_moves = get_mate_moves()
    move_with_queen = get_best_move_with_queen()
    rook_in_danger = get_rook_in_danger()
    night_in_danger = get_night_in_danger()
    bishop_in_danger = get_bishop_in_danger()
    starting_moves = get_starting_moves()


    print("mate:",mate_moves, file=sys.stderr, flush=True)
    print("king op moves :",get_op_king_moves(), file=sys.stderr, flush=True)
    print("value move :",value_move,moves_values[value_move], file=sys.stderr, flush=True)
    print("check moves :",check_moves_0, file=sys.stderr, flush=True)
    print("value and check moves :",check_moves_value, file=sys.stderr, flush=True)
    print("pawn pushs :",pawn_moves_no_value, file=sys.stderr, flush=True)
    print("queen in dangeer :",op_can_eat_my_queen(),"rook in danger", rook_in_danger , file=sys.stderr, flush=True)


    if len(mate_moves) > 0:
        print("\n CHECKMATE !!!", file=sys.stderr, flush=True)
        next_move = mate_moves[0]
    elif op_can_eat_my_queen() and move_with_queen != False:
        print("\nbest move with queen.", file=sys.stderr, flush=True)
        next_move = move_with_queen
    elif rook_in_danger != False and value < 5 and best_move_with(rook_in_danger)[1] > -1 :
        print("\nbest move with rook.", file=sys.stderr, flush=True)
        next_move = best_move_with(rook_in_danger)[0]
    elif night_in_danger != False and value < 3 and best_move_with(night_in_danger)[1] > -1 :
        print("\nbest move with night.", file=sys.stderr, flush=True)
        next_move = best_move_with(night_in_danger)[0]
    elif bishop_in_danger != False and value < 3 and best_move_with(bishop_in_danger)[1] > -1 :
        print("\nbest move with night.", file=sys.stderr, flush=True)
        next_move = best_move_with(bishop_in_danger)[0]
    
    elif len(starting_moves)>0:
        next_move = starting_moves[0]
    
    
    elif castling in moves:
        print("\ncastling .", file=sys.stderr, flush=True)
        next_move = castling
    elif len(check_moves_value) > 0:
        print("\ncheck and value !", file=sys.stderr, flush=True)
        next_move = get_higher_value_check_move()
    elif value > 0:
        print("\nvalue !", file=sys.stderr, flush=True)
        next_move = value_move
    elif len(op_pieces) < 4:
        print("\ncatch the king !",get_op_king_case(),"with",catch_the_king(), file=sys.stderr, flush=True)
        next_move = catch_the_king()[0]
    
    elif len(dev_moves):
        print("\ndeveloppement.", file=sys.stderr, flush=True)
        next_move = dev_moves[0]

    elif len(pawn_moves_no_value) > 0 :
        print("\npush pawn", file=sys.stderr, flush=True)
        next_move = pawn_moves_no_value[0]

    elif len(check_moves_0):
        print("\ncheck !", file=sys.stderr, flush=True)
        next_move = check_moves_0[0]

    else:
        print("\nnothing better to play ...", file=sys.stderr, flush=True)
        next_move = value_move


    print(next_move)
