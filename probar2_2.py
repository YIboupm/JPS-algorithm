

import sys

import json
import math
# mapa 0 camino,1 mulo
map_test = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]

# direccion
g_dir = [[1, 0], [0, 1], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
class Node:
    def __init__(self, parent, pos, g, h):
        self.parent = parent
        self.pos = pos
        self.g = g
        self.h = h
        self.f = g + h
    def get_direction(self):
        return self.parent and [self.pos[0] != self.parent.pos[0] and (self.pos[0] - self.parent.pos[0]) / abs(self.pos[0] - self.parent.pos[0]) or 0, self.pos[1] != self.parent.pos[1] and (self.pos[1] - self.parent.pos[1]) / abs(self.pos[1] - self.parent.pos[1]) or 0] or [0, 0]


class JPS:

    # Si desea modificar el mapa, introduzca el tamaño del mapa
    def __init__(self, width, height):
        self.s_pos = None
        self.e_pos = Node

        self.width = width
        self.height = height
        self.open = []
        self.close = []
        self.path = []

    def prune_neighbours(self, c):
        nbs = []
        
        if c.parent:
            
            dir = c.get_direction()
            if self.is_pass(c.pos[0] + dir[0], c.pos[1] + dir[1]):
                nbs.append([c.pos[0] + dir[0], c.pos[1] + dir[1]])
            print ("dir = ", dir)
              
            if dir[0] != 0 and dir[1] != 0:
                 
                if self.is_pass(c.pos[0], c.pos[1] + dir[1]):
                    nbs.append([c.pos[0], c.pos[1] + dir[1]])
                
                if self.is_pass(c.pos[0]+dir[0], c.pos[1]):
                    nbs.append([c.pos[0]+dir[0], c.pos[1]])
                 
                if not self.is_pass(c.pos[0] - dir[0], c.pos[1]) and self.is_pass(c.pos[0], c.pos[1] + dir[1]):
                     
                    nbs.append([c.pos[0] - dir[0], c.pos[1] + dir[1]])
                  
                if not self.is_pass(c.pos[0], c.pos[1]-dir[1]) and self.is_pass(c.pos[0]+dir[0], c.pos[1]):
                    
                    nbs.append([c.pos[0]+dir[0], c.pos[1]-dir[1]])
            else:   
                 
                if dir[0] == 0:
                      
                    if not self.is_pass(c.pos[0]+1, c.pos[1]):
                         
                        nbs.append([c.pos[0]+1, c.pos[1]+dir[1]])
                     
                    if not self.is_pass(c.pos[0]-1, c.pos[1]):
                        
                        nbs.append([c.pos[0]-1, c.pos[1]+dir[1]])

                else: 
                    if not self.is_pass(c.pos[0], c.pos[1]+1):
                         
                         nbs.append([c.pos[0]+dir[0], c.pos[1]+1])
                     
                    if not self.is_pass(c.pos[0], c.pos[1]-1):
                        
                         nbs.append([c.pos[0]+dir[0], c.pos[1]-1])

        else:
            for d in g_dir:
                if self.is_pass(c.pos[0] + d[0], c.pos[1] + d[1]):
                    nbs.append([c.pos[0] + d[0], c.pos[1] + d[1]])
        print ("prune_neighbours c= %s, nbs = %s" % ([c.pos[0], c.pos[1]], nbs))
        return nbs
    # ↑ ↓ ← → ↖ ↙ ↗ ↘
    def jump_node(self, now, pre):
        dir = [a != b and (a - b)/abs(a-b) or 0 for a, b in zip(now, pre)]
        print ("now = %s, pre = %s, dir = %s" %(now, pre, dir)    )    

        if now == self.e_pos:
            return now

        if self.is_pass(now[0], now[1]) is False:
            return None
        if dir[0] != 0 and dir[1] != 0:
            
            if (self.is_pass(now[0] - dir[0], now[1] + dir[1]) and not self.is_pass(now[0]-dir[0], now[1])) or (self.is_pass(now[0] + dir[0], now[1] - dir[1]) and not self.is_pass(now[0], now[1]-dir[1])):
                return now
        else:
           
            if dir[0] != 0:
                
                '''
                * 1 0       0 0 0
                0 → 0       0 0 0
                * 1 0       0 0 0
                
                '''
                print ('direccion horizons:', self.is_pass(now[0] + dir[0], now[1] + 1), self.is_pass(now[0], now[1]+1), self.is_pass(now[0] + dir[0], now[1] - 1), self.is_pass(now[0], now[1]-1))
                if (self.is_pass(now[0] + dir[0], now[1] + 1) and not self.is_pass(now[0], now[1]+1)) or (self.is_pass(now[0] + dir[0], now[1] - 1) and not self.is_pass(now[0], now[1]-1)):
                    return now
            else: 
                '''
                0 0 0
                1 ↓ 1
                0 0 0
                                
                '''
                print ('vertical direction:', self.is_pass(now[0] + 1, now[1] + dir[1]), self.is_pass(now[0] + 1, now[1]), self.is_pass(now[0]-1 , now[1] + dir[1]), self.is_pass(now[0] - 1, now[1]))
                if (self.is_pass(now[0] + 1, now[1] + dir[1]) and not self.is_pass(now[0]+1, now[1])) or (self.is_pass(now[0] - 1, now[1] + dir[1]) and not self.is_pass(now[0]-1, now[1])):
                    return now

        if dir[0] != 0 and dir[1] != 0:
            t1 = self.jump_node([now[0]+dir[0], now[1]], now)
            t2 = self.jump_node([now[0], now[1] + dir[1]], now)
            if t1 or t2:
                return now
        if self.is_pass(now[0] + dir[0], now[1]) or self.is_pass(now[0], now[1] + dir[1]):
            t = self.jump_node([now[0] + dir[0], now[1] + dir[1]], now)
            if t:
                return t

        return None

    def extend_round(self, c):
        nbs = self.prune_neighbours(c)
        print ("************[%d, %d] --- %s, parent = [%d, %d]" % (c.pos[0], c.pos[1], nbs, c.pos[0], c.pos[1]))
        for n in nbs:
            jp = self.jump_node(n,[c.pos[0], c.pos[1]])
            print ("expandSuccessors:parent = %s, nb = %s, jp = %s" % ([c.pos[0], c.pos[1]], n, jp))
            if jp:
                if self.node_in_close(jp):
                    continue
                g = self.get_g(jp, c.pos)
                h = self.get_h(jp, self.e_pos)
                node = Node(c, jp, c.g + g, h)
                i = self.node_in_open(node)
                if i != -1:
                
                    if self.open[i].g > node.g:
                        self.open[i].parent = c
                        self.open[i].g = node.g
                        self.open[i].f = node.g + self.open[i].h
                    continue
                self.open.append(node)

    def is_pass(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height and (map_test[int(x)][int(y)] != 1 or [x, y] == self.e_pos)

    
    def find_path(self, s_pos, e_pos):
        self.s_pos, self.e_pos = s_pos, e_pos
       
        p = Node(None, self.s_pos, 0, abs(self.s_pos[0]-self.e_pos[0]) + abs(self.s_pos[1]-self.e_pos[1]))
        self.open.append(p)
        while True:
           
            if not self.open:
                return "not find"
            
            idx, p = self.get_min_f_node()
            print("find path with extend_round(%d, %d), open_list = %s" % (p.pos[0], p.pos[1], [[n.pos[0], n.pos[1]] for n in self.open]))
           
            if self.is_target(p):
                self.make_path(p)
                return
            self.extend_round(p)
            
            self.close.append(p)
            del self.open[idx]

    def make_path(self, p):
    
        while p:

            if p.parent:
                dir = p.get_direction()
                n = p.pos
                while n != p.parent.pos:
                    self.path.append(n)
                    n = [n[0] - dir[0], n[1] - dir[1]]
            else:
                self.path.append(p.pos)
            p = p.parent
        self.path.reverse()
    def is_target(self, n):
        return n.pos == self.e_pos

    def get_min_f_node(self):
        best = None
        bv = -1
        bi = -1
        for idx, node in enumerate(self.open):
            
            if bv == -1 or node.f < bv:  
                best = node
                bv = node.f
                bi = idx
        return bi, best
    
    def get_g(self, pos1, pos2):
        if pos1[0] == pos2[0]:
            return abs(pos1[1] - pos2[1])
        elif pos1[1] == pos2[1]:
            return abs(pos1[0] - pos2[0])
        else:
            return abs(pos1[0] - pos2[0]) * 1.4
    
    def get_h(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def node_in_close(self, node):
        for i in self.close:
            if node == i.pos:
                return True
        return False

    def node_in_open(self, node):
        for i, n in enumerate(self.open):
            if node == n.pos:
                return i
        return -1

    def get_searched(self):
        l = []
        for i in self.open:
            l.append((i.pos[0], i.pos[1]))
        for i in self.close:
            l.append((i.pos[0], i.pos[1]))
        return l

    def print_path(self):
        for n in self.path:
            map_test[int(n[0])][int(n[1])] = 6

        print ('------------------------------')
        for ns in map_test:
            print (''.join(str(ns)))

def find_path(s_pos, e_pos):
    jps = JPS(9, 25)
    err = jps.find_path(s_pos, e_pos)
    searched = jps.get_searched()
    path = jps.path
    print ("path length is %d" % (len(path)))
    print ("searched %s" % (searched))
    print ("err = ", err)
    
    if len(path) > 0:
        print("find_path, start_pos:%s" % s_pos, "end_pos:%s" % e_pos, "path = ",
                json.dumps(path), "len(path) = ", len(path), "len(searched) = ", len(searched))
    else:
        print("find_path not find path, start_pos:%s" % s_pos, "end_pos:%s" % e_pos,
                "len(searched) = ", len(searched))
    jps.print_path()
    return path, err


def check_pos_valid(x, y):
    jps = JPS(None, x, y, x, y)
    return jps.is_valid_coord(x, y)


if __name__ == "__main__":
    
    find_path([0,0], [0,24])

