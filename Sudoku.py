from typing import Set, Dict

from CSP import CSP, Variable, Value


class Sudoku(CSP):
    def __init__(self, MRV=True, LCV=True):
        super().__init__(MRV=MRV, LCV=LCV)
        # TODO: Implement Sudoku::__init__ (problem 4)
        variables=set()
        for row in range(9):
            for col in range(9):
                variables.add(Cell(row,col))
        self._variables=variables

    @property
    def variables(self) -> Set['Cell']:
        """ Return the set of variables in this CSP. """
        # TODO: Implement Sudoku::variables (problem 4)
        return self._variables

    def getCell(self, x: int, y: int) -> 'Cell':
        """ Get the  variable corresponding to the cell on (x, y) """
        # TODO: Implement Sudoku::getCell (problem 4)
        for cell in self._variables:
            if cell.x==x and cell.y==y:
                return cell

    def neighbors(self, var: 'Cell') -> Set['Cell']:
        """ Return all variables related to var by some constraint. """
        # TODO: Implement Sudoku::neighbors (problem 4)
        x=var.x
        y=var.y
        #horizontaal en verticaal
        cells=set()
        for val in range(9):
            if(self.getCell(var.x,val)==var):
                continue
            cells.add(self.getCell(var.x,val))
        for val in range(9):
            if (self.getCell(val, var.y) == var):
                continue
            cells.add(self.getCell(val,var.y))
        #per vak
        blocky=int(y/3)
        blockx=int(x/3)
        for row in range(3):
            for col in range(3):
                rowx=row+(3*blockx)
                rowy=col+(3*blocky)
                if(self.getCell(rowx,rowy)==var):
                    continue
                cells.add(self.getCell(row+(3*blockx),col+(3*blocky)))
        return cells

    def isValidPairwise(self, var1: 'Cell', val1: Value, var2: 'Cell', val2: Value) -> bool:
        """ Return whether this pairwise assignment is valid with the constraints of the csp. """
        # TODO: Implement Sudoku::isValidPairwise (problem 4)
        if val1==val2:
            return False
        return True


    def assignmentToStr(self, assignment: Dict['Cell', Value]) -> str:
        """ Formats the assignment of variables for this CSP into a string. """
        s = ""
        for y in range(9):
            if y != 0 and y % 3 == 0:
                s += "---+---+---\n"
            for x in range(9):
                if x != 0 and x % 3 == 0:
                    s += '|'

                cell = self.getCell(x, y)
                s += str(assignment.get(cell, ' '))
            s += "\n"
        return s

    def parseAssignment(self, path: str) -> Dict['Cell', Value]:
        """ Gives an initial assignment for a Sudoku board from file. """
        initialAssignment = dict()
        with open(path, "r") as file:
            for y, line in enumerate(file.readlines()):
                if line.isspace():
                    continue
                assert y < 9, "Too many rows in sudoku"

                for x, char in enumerate(line):
                    if char.isspace():
                        continue

                    assert x < 9, "Too many columns in sudoku"

                    var = self.getCell(x, y)
                    val = int(char)

                    if val == 0:
                        continue

                    assert val > 0 and val < 10, f"Impossible value in grid"
                    initialAssignment[var] = val
        return initialAssignment


class Cell(Variable):
    def __init__(self,x,y):
        super().__init__()
        # TODO: Implement Cell::__init__ (problem 4)
        self.x=x
        self.y=y
        # You can add parameters as well.

    @property
    def startDomain(self) -> Set[Value]:
        """ Returns the set of initial values of this variable (not taking constraints into account). """
        # TODO: Implement Cell::startDomain (problem 4)
        return {1,2,3,4,5,6,7,8,9}
    def __repr__(self):
        return f"{self.x},{self.y}"
    def __hash__(self):
        return hash((self.x, self.y))
    def __eq__(self, other):
        return isinstance(other, Cell) and self.x == other.x and self.y == other.y


