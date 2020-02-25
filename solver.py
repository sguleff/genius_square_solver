class Piece(object):
    '''
    Piece Types:
    
        1 - * * * *
            *
            
        2 - * * *
              *
        
        3 - * *
              * *
              
        4 - * * * *
        
        5 - * * *
       
              
        6 - * *
              *
              
        7 - * *
            * *
 
        8 - * * 
            
        9 - *  
    '''
    
    location = ()
    rotations = [0,1,2,3]
    types = {1:[[1,1,1,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]],
             2:[[1,0,0,0],[1,1,0,0],[1,0,0,0],[0,0,0,0]],
             3:[[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,0,0,0]],
             4:[[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]],
             5:[[1,0,0,0],[1,0,0,0],[1,0,0,0],[0,0,0,0]],
             6:[[1,0,0,0],[1,1,0,0],[0,0,0,0],[0,0,0,0]],
             7:[[1,1,0,0],[1,1,0,0],[0,0,0,0],[0,0,0,0]],
             8:[[1,0,0,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]],
             9:[[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]}
    
    memoized_type_rotation = {}
             
    def __init__(self, t):
        self.type = t
        self.memoized_type_rotation = {}
        self.location = (-1,-1,-1)
        self.piece = np.matrix(self.types[t])
        
    def get_piece(self, t):
        self.piece
        
    def set_location(self, x, y, r):
        '''
        set the current location of a piece based on x,y and rotation coordinates
        '''
        self.location = (x, y, r)
        
    def get_location(self, x, y):
        return self.location
    
    def rotate_piece(self, switch = 0):
        
        #memoize and reduce redundent work
        if switch in self.memoized_type_rotation:
            self.memoized_type_rotation[switch]
        
        if switch == 0:
            self.memoized_type_rotation[0] = self.__shift_piece(self.piece)
            return self.memoized_type_rotation[0]
        if switch == 1:
            self.memoized_type_rotation[1] = self.__shift_piece(self.piece.T)
            return self.memoized_type_rotation[1]
        if switch == 2:
            self.memoized_type_rotation[2] = self.__shift_piece(np.flip(self.piece, 1))
            return self.memoized_type_rotation[2]
        if switch == 3:
            self.memoized_type_rotation[3] = self.__shift_piece(np.flip(self.piece.T, 0))
            return self.memoized_type_rotation[3]
        return None
    
    def __shift_piece(self, p):
        oriented_piece = p
        while int(np.sum(oriented_piece.T, 1)[0][0]) == 0:
            oriented_piece = np.roll(oriented_piece, -1, 1)
        while int(np.sum(oriented_piece, 1)[0][0]) == 0:
            oriented_piece = np.roll(oriented_piece, -1, 0)
        return oriented_piece
    
    def __repr__(self):
        return "".join([str(x) + "\n" for x in self.types[self.type]])

    def __str__(self):
        return self.__repr__() 

import numpy as np

_CLIPBUFFER = 3

class Board(object):
    '''
    self.Board:
       
        Board + piece clipping boundries with X
        
         1 . 2 . 3 . 4 . 5 . 6 
       + - + - + - + - + - + - + - + - + - + - + 
     A | 0 . 1 . 2 . 3 . 4 . . . n | X . X . X |
       + - + - + - + - + - + - + - + - + - + - +
     B | 0 . 1 . 2 . 3 . 4 . . . n | X . X . X .
       + - + - + - + - + - + - + - + - + - + - + 
     C | 0 . 1 . 2 . 3 . 4 . . . n | X . X . X . 
       + - + - + - + - + - + - + - + - + - + - + 
     D | 0 . 1 . 2 . 3 . 4 . . . n | X . X . X .
       + - + - + - + - + - + - + - + - + - + - + 
     E | 0 . . . . . . . . . . . n | X . X . X . 
       + - + - + - + - + - + - + - + - + - + - + 
     F | 0 . n . n . n . n . n . n | X . X . X . 
       =========================== + + - + - + -
       | X . X . X . X . X . X . X . X . X . X . 
       + - + - + - + - + - + - + - + - + - + - + 
       | X . X . X . X . X . X . X . X . X . X . 
       + - + - + - + - + - + - + - + - + - + - + 
       | X . X . X . X . X . X . X . X . X . X . 
       + - + - + - + - + - + - + - + - + - + - +     
    '''
    
    def wasted_rotations(self, pn, r):
        if pn in (7,9) and (r == 2 or r == 3 or r == 4):
            return True
        if pn in (5,4,8) and (r == 2):
            return True
        if not pn in (1,3) and (r > 4):
            return True
        else:
            return False
    
    def all_space_discovery(self, pn):
        comb = []
        piece = self.pieces[pn]
        for y in range(self.size):
            for x in range(self.size):
                for r, i in enumerate(piece.rotations):
                    if not self.wasted_rotations(pn,r): #skip geometric rotation redundencies
                        if self.__check_piece_interference((x, y, r), piece):
                            comb.append((x,y,r))
        return comb
    
    def space_discovery(self, pn):
        piece = self.pieces[pn]
        for y in range(self.size):
            for x in range(self.size):
                for r, i in enumerate(piece.rotations):
                    if not self.wasted_rotations(pn,r): #skip geometric rotation redundencies
                        if self.__check_piece_interference((x, y, r), piece):
                            return x, y, r
        return None
    
    def add_peg(self, x , y):
        if self.Board[x][y] == 0:
            self.Board[x][y] = 'P' 
            return True
        else:
            return False
        
    def add_peg_name(self, y, x):
        if self.Board[x-1][ord(y) - 65] == 0:
            self.Board[x-1][ord(y) - 65] = 'P' 
            return True
        else:
            return False
          
    def remove_peg(self, x , y):
        if self.Board[x][y] == 9:
            self.Board[x][y] = 'P'
            return True
        else:
            return False
          
    def __check_piece_interference(self, l, piece):
        x,y,r = l
        oriented_piece = piece.rotate_piece(r)
        free = True
        for _y in range(4):
            for _x in range(4):
                if oriented_piece.item((_x,_y)) == 1:
                    if not self.Board[_x + x][_y + y] == 0:
                        free = False     
        return free
    
    def __verify_piece_location(self,piece, x, y):
        x,y,r = piece.location
        oriented_piece = piece.rotate_piece(r)
        for _y in range(4):
                for _x in range(4):
                    if oriented_piece.item((_x,_y)) == 1:
                        if not self.Board[_x + x][_y + y] == piece.type:
                            return False
        return True

    def add_piece(self, pn, l):
        piece = self.pieces[pn]
        (x,y,r) = l
        oriented_piece = piece.rotate_piece(r)
        for _y in range(4):
                for _x in range(4):
                    if oriented_piece.item((_x,_y)) == 1:
                        if not self.Board[_x + x][_y + y] == 0:
                            Exception("Add Piece Interference")
                        self.Board[_x + x][_y + y] = piece.type
        self.pieces[pn].location = l
                        
    def remove_piece(self,pn):
        piece = self.pieces[pn]
        (x,y,r) = piece.location
        oriented_piece = piece.rotate_piece(r)
        for _y in range(4):
            for _x in range(4):
                if oriented_piece.item((_x,_y)) == 1:
                    if not self.Board[_x + x][_y + y] == piece.type:
                        Exception("Remove Piece Interference")
                    self.Board[_x + x][_y + y] = 0 
        self.pieces[pn].location = (-1,-1,-1)
        
        
    def __init__(self, size, _CLIPBUFFER):
        s = size + _CLIPBUFFER
        self.size = size
        self.pieces = {x:Piece(x) for x in range(1,10)}
        self.Board = [[0 if x < size and y < size else 1 for x in range(s)] for y in range(s)]
        
    def __repr__(self):
        output = "    " + "".join([f"{i + 1} . " for i in range(self.size)])
        for y in range(self.size):
            output += f"\n  +" + " - +"*self.size + f"\n{chr(y+65)} "
            for x in range(self.size):
                output += f"+ {self.Board[x][y]} "
        return output

    def __str__(self):
        return self.__repr__()


from collections import defaultdict
import time 

class Decision_Tree(object):
    #(piece,x,y)
    Permutation_Stack = {}
    Current_Attempt = []
    work_stats = defaultdict(int)
    solutions = []
    
    
    def __init__(self, tracking_on = True):
        self.Permutation_Stack = {1:[],
                                  2:[],
                                  3:[],
                                  4:[],
                                  5:[],
                                  6:[],
                                  7:[],
                                  8:[],
                                  9:[]
                                 }
        self.Current_Attempt = []
        self.tracking_on = tracking_on
        self.work_stats = defaultdict(int)
        self.work_stats.clear()
        self.solutions = []
        self.start = time.time()
        
        #do work
        self.work(1)
   
    def add_decision_layer(self, pn, piece_permutations):
        self.Permutation_Stack[pn] = piece_permutations
        
    def remove_decision_layer(self, pn):
        del self.Permutation_Stack[pn]
        
    def get_attempt(self, pn):
        x = self.Permutation_Stack[pn].pop()
        self.Current_Attempt.append(x)
        return x
    
    def toss_attempt(self):
        return self.Current_Attempt.pop()
    
    def work(self, pntr):
        layer = self.check_combos(pntr)

        if layer is not None:
            self.add_decision_layer(pntr,layer)

            while len(self.Permutation_Stack[pntr]) > 0:   
                if self.tracking_on:
                    self.__stats_tracking(pntr)
                    
                l = self.get_attempt(pntr)
                B.add_piece(pntr, l)

                # We made it to the leaf and placed a piece
                if pntr == 9:
                    #print first solution fast and keep going:
                    if self.work_stats[pntr] == 1:
                        print("FOUND FIRST SOLUTION:  ")
                        total_results = sum(self.work_stats.values())
                        update_time = time.time() - self.start
                        print(f"Total Results: {total_results}, Total Time: {update_time}")
                        print(B)
                        
                    self.solutions.append(str(self.Current_Attempt))
                else:
                    self.work(pntr + 1)

                B.remove_piece(pntr)
                self.toss_attempt()

            self.remove_decision_layer(pntr)
            
    def __stats_tracking(self, pntr):

        #keep track of runs
        self.work_stats[pntr] += 1
        total_results = sum(self.work_stats.values())
        if total_results % 10000 == 0:
            update_time = time.time() - self.start
            rate = total_results / update_time
            print(f"Total Results: {total_results}, Total Time: {update_time}, rate: {rate} ")
            print(f"Run Statistics: {self.work_stats}")
            len_sol = len(self.solutions)
            print(f"Solutions Found: {len_sol}")
    
    def check_combos(self, pntr):
        current_perm = {z:B.all_space_discovery(z) for z in range(1,10) if B.pieces[z].location == (-1,-1,-1)}
        if len(current_perm[next(iter(current_perm))]) == 0:
            return None
        else:
            return current_perm[pntr]

# run here
B = Board(6, _CLIPBUFFER)
B.add_peg_name("B", 2)
B.add_peg_name("B", 5)
B.add_peg_name("C", 3)
B.add_peg_name("D", 3)
B.add_peg_name("D", 4)
B.add_peg_name("E", 2)
B.add_peg_name("E", 5)

print(B)

T = Decision_Tree(True)
