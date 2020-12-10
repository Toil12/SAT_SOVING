from SAT1.FileOperation import FileOperation
from pysat.solvers import Solver
import numpy as np
TENT=1
EMPTY=2
TREE=3

class SAT1Solver():
    def __init__(self,map:dict):
        self.data = map
        self.size = map['size']
        self.row_constraint = map['row_number']
        self.column_constraint = map['column_number']
        self.envrionment = map['environment']
        self.PreProcessor()

    def Combinations(self,L, k):
        n = len(L)
        result = []
        for i in range(n - k + 1):
            if k > 1:
                newL = L[i + 1:]
                Comb, _ = self.Combinations(newL, k - 1)
                for item in Comb:
                    item.insert(0, L[i])
                    result.append(item)
            else:
                result.append([L[i]])
        return result, len(result)

    def GetNeighbours(self, x, y, directions=4):
        neighbours = []
        if directions == 4:
            if x - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x-1,y))
            if y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append((x,y+1))
            if x + 1 >= self.size[0]:
                neighbours.append(None)
            else:
                neighbours.append((x+1,y))
            if y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x,y-1))
            return neighbours
        else:
            if x - 1 < 0 or y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x-1,y-1))

            if x - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x-1,y))

            if x - 1 < 0 or y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append((x-1,y+1))

            if y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append((x,y+1))

            if x + 1 >= self.size[0] or y + 1 >= self.size[1]:
                neighbours.append(None)
            else:
                neighbours.append((x+1,y+1))

            if x + 1 >= self.size[0]:
                neighbours.append(None)
            else:
                neighbours.append((x+1,y))

            if x + 1 >= self.size[0] or y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x+1,y-1))

            if y - 1 < 0:
                neighbours.append(None)
            else:
                neighbours.append((x,y-1))
        return neighbours

    def PositioanToVar(self,positon:tuple):
        x=positon[0]
        y=positon[1]
        se=((x)*self.size[0])+y+1
        return se

    def ReturnIndex(self,item):
        for i in range(len(self.small_search_space)):
            if self.small_search_space[i]==item:
                return int(i)

    def PreProcessor(self):
        self.var=np.zeros((self.size[0],self.size[1]*3))
        self.small_search_space=[]
        trees=[]
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.envrionment[i,j]==-1:
                    self.var[i,3*(j+1)-1]=1
                    trees.append((i,j))
        for cell in trees:
            neighbours=self.GetNeighbours(cell[0],cell[1])
            for neighbour in neighbours:
                if neighbour!=None and neighbour not in self.small_search_space:
                    self.small_search_space.append(neighbour)
        self.small_search_space=sorted(self.small_search_space)

    def ClauseMaker(self):
        self.small_search_space_index=[int(i) for i in range(0, len(self.small_search_space))]
        print(self.small_search_space_index)
        self.clauses = []
        for row_index in range(len(self.row_constraint)):
            row_con=self.row_constraint[row_index]
            space=[]
            for j in range(len(self.small_search_space)):
                if self.small_search_space[j][0]==row_index:
                    space.append(self.small_search_space[j])
            # print(space)
            var_indexs=[self.PositioanToVar(i) for i in space]
            # print(row_con)
            if len(var_indexs)==row_con:
                for v in var_indexs:
                    self.clauses.append([v])
            elif row_con==0:
                continue
            else:
                var_indexs1=[-i for i in var_indexs]
                line_clause1,cluase_number1=self.Combinations(var_indexs1,row_con+1)
                for each in line_clause1:
                    self.clauses.append(each)

                line_clause0,cluase_number0=self.Combinations(var_indexs,self.size[0]-row_con+1)
                for each in line_clause0:
                    self.clauses.append(each)
        print(self.clauses)
        for col_index in range(len(self.column_constraint)):
            col_con=self.column_constraint[col_index]
            space=[]
            for j in range(len(self.small_search_space)):
                if self.small_search_space[j][1]==col_index:
                    space.append(self.small_search_space[j])
            # print(space)
            var_indexs=[self.PositioanToVar(i) for i in space]
            # print(col_con)
            if len(var_indexs)==col_con:
                for v in var_indexs:
                    self.clauses.append([v])
            elif col_con==0:
                continue
            else:
                var_indexs1=[-i for i in var_indexs]
                line_clause1,cluase_number1=self.Combinations(var_indexs1,col_con+1)
                for each in line_clause1:
                    self.clauses.append(each)
                line_clause0,cluase_number0=self.Combinations(var_indexs,self.size[0]-col_con+1)
                for each in line_clause0:
                    self.clauses.append(each)
        # print(self.clauses)
        print(len(self.clauses))

    def Solver(self,clauses=None):
        transform_clauses=[]
        if clauses==None:
            clauses=np.array(self.clauses)
        print(clauses.shape)
        for i in range(len(clauses)):
            line=[]
            for item in clauses[i]:
                line.append(item.item())
            transform_clauses.append(line)
        s=Solver(name='cadical')
        print(transform_clauses[0])

        for item in transform_clauses:
            s.add_clause(item)
        print(s.solve())
        print(s.get_model())



if __name__ == '__main__':
    file_name = 'tents-8x8-t1.txt'
    name = file_name.split('.')[0]
    map = FileOperation.ReadFile(file_name)
    sol=SAT1Solver(map)
    sol.PreProcessor()
    sol.ClauseMaker()
    sol.Solver()
    # print(sol.envrionment)
    # print(sol.small_search_space)
    # print(len(sol.small_search_space))
    # print(sol.PositioanToVar((3,3)))