import copy
import random
from typing import Set, Dict, List, TypeVar, Optional
from abc import ABC, abstractmethod

from util import monitor


Value = TypeVar('Value')


class Variable(ABC):
    @property
    @abstractmethod
    def startDomain(self) -> Set[Value]:
        """ Returns the set of initial values of this variable (not taking constraints into account). """
        pass


class CSP(ABC):
    def __init__(self, MRV=True, LCV=True):
        self.MRV = MRV
        self.LCV = LCV

    @property
    @abstractmethod
    def variables(self) -> Set[Variable]:
        """ Return the set of variables in this CSP.
            Abstract method to be implemented for specific instances of CSP problems.
        """
        pass

    def remainingVariables(self, assignment: Dict[Variable, Value]) -> Set[Variable]:
        """ Returns the variables not yet assigned. """
        return self.variables.difference(assignment.keys())

    @abstractmethod
    def neighbors(self, var: Variable) -> Set[Variable]:
        """ Return all variables related to var by some constraint.
            Abstract method to be implemented for specific instances of CSP problems.
        """
        pass

    def assignmentToStr(self, assignment: Dict[Variable, Value]) -> str:
        """ Formats the assignment of variables for this CSP into a string. """
        s = ""
        for var, val in assignment.items():
            s += f"{var} = {val}\n"
        return s

    def isComplete(self, assignment: Dict[Variable, Value]) -> bool:
        """ Return whether the assignment covers all variables.
            :param assignment: dict (Variable -> value)
        """
        # TODO: Implement CSP::isComplete (problem 1)
        return len(self.remainingVariables(assignment))==0


    @abstractmethod
    def isValidPairwise(self, var1: Variable, val1: Value, var2: Variable, val2: Value) -> bool:
        """ Return whether this pairwise assignment is valid with the constraints of the csp.
            Abstract method to be implemented for specific instances of CSP problems.
        """
        pass

    def isValid(self, assignment: Dict[Variable, Value]) -> bool:
        """ Return whether the assignment is valid (i.e. is not in conflict with any constraints).
            You only need to take binary constraints into account.
            Hint: use `CSP::neighbors` and `CSP::isValidPairwise` to check that all binary constraints are satisfied.
            Note that constraints are symmetrical, so you don't need to check them in both directions.
        """
        # TODO: Implement CSP::isValid (problem 1)
        for key in assignment:
            variablestocheck=self.neighbors(key)
            for check in variablestocheck:
                if(not check in self.remainingVariables(assignment)):
                    if self.isValidPairwise(key, assignment[key], check, assignment[check]) == False:
                        return False
        return True

    def functioncalllist(self):
        test=["appel","peer"]
        self.functioncalltest(test)
        print(test)
    def functioncalltest(self,list):
        list.append("citroen")
        print("test")

    def solveBruteForce(self, initialAssignment: Dict[Variable, Value] = dict()) -> Optional[Dict[Variable, Value]]:
        """ Called to solve this CSP with brute force technique.
            Initializes the domains and calls `CSP::_solveBruteForce`. """
        domains = domainsFromAssignment(initialAssignment, self.variables)
        return self._solveBruteForce(initialAssignment, domains)
    @monitor
    def _solveBruteForce(self, assignment: Dict[Variable, Value], domains: Dict[Variable, Set[Value]]) -> Optional[Dict[Variable, Value]]:
        """ Implement the actual backtracking algorithm to brute force this CSP.
            Use `CSP::isComplete`, `CSP::isValid`, `CSP::selectVariable` and `CSP::orderDomain`.
            :return: a complete and valid assignment if one exists, None otherwise.
        """
        # TODO: Implement CSP::_solveBruteForce (problem 1)
        if self.isComplete(assignment):
            return assignment
        var=self.selectVariable(assignment,domains)
        checklistvalid = copy.deepcopy(assignment)
        for value in self.orderDomain(assignment,domains,var):
            checklistvalid[var]=value
            if(self.isValid(checklistvalid)):
                assignment[var] = value
                result=self._solveBruteForce(assignment,domains)
                if result != False:
                    return result
                del assignment[var]
        return False


    def solveForwardChecking(self, initialAssignment: Dict[Variable, Value] = dict()) -> Optional[Dict[Variable, Value]]:
        """ Called to solve this CSP with forward checking.
            Initializes the domains and calls `CSP::_solveForwardChecking`. """
        domains = domainsFromAssignment(initialAssignment, self.variables)
        domains = self.forwardChecking(initialAssignment, domains)
        return self._solveForwardChecking(initialAssignment, domains)




    @monitor
    def _solveForwardChecking(self, assignment: Dict[Variable, Value], domains: Dict[Variable, Set[Value]]) -> Optional[Dict[Variable, Value]]:
        """ Implement the actual backtracking algorithm with forward checking.
            Use `CSP::forwardChecking` and you should no longer need to check if an assignment is valid.
            :return: a complete and valid assignment if one exists, None otherwise.
        """
        # TODO: Implement CSP::_solveForwardChecking (problem 2)
        if self.isComplete(assignment):
            return assignment
        var = self.selectVariable(assignment, domains)
        checklistvalid = copy.deepcopy(assignment)
        domvar=domains[var]
        domainInOrders=self.orderDomain(assignment,domains,var)
        for value in domainInOrders:
            checklistvalid[var] = value
            newdomains=self.forwardChecking(checklistvalid, domains, var)
            if (not self.checkkeyZero(newdomains)):
                newdomains[var] = {checklistvalid[var]}
                assignment[var] = value
                result = self._solveForwardChecking(assignment, newdomains)
                if result != False:
                    return result
                del assignment[var]
        return False
    def checkkeyZero(self,map):
        for key in map:
            if len(map[key])==0:
                return True
        return False
    def forwardChecking(self, assignment: Dict[Variable, Value], domains: Dict[Variable, Set[Value]], variable: Optional[Variable] = None) -> Dict[Variable, Set[Value]]:
        """ Implement the forward checking algorithm from the theory lectures.

        :param domains: current domains.
        :param assignment: current assignment.
        :param variable: If not None, the variable that was just assigned (only need to check changes).
        :return: the new domains after enforcing all constraints.
        """
        # TODO: Implement CSP::forwardChecking (problem 2)
        returndomains = copy.deepcopy(domains)

        if variable==None:
            for var in assignment:
                returndomains=self.forwardChecking(assignment,returndomains,var)
            return returndomains
        returndomains = copy.deepcopy(domains)
        if (variable == None):
            return returndomains
        for neigb in self.neighbors(variable):
            if neigb in assignment:
                continue
            checkassignment = copy.deepcopy(assignment)
            for val in domains[neigb]:
                checkassignment[neigb] = val
                if not self.isValidPairwise(variable,assignment[variable],neigb,val):
                    returndomains[neigb].remove(val)
        return returndomains

    def selectVariable(self, assignment: Dict[Variable, Value], domains: Dict[Variable, Set[Value]]) -> Variable:
        """ Implement a strategy to select the next variable to assign. """
        if not self.MRV:
            return random.choice(list(self.remainingVariables(assignment)))
        # TODO: Implement CSP::selectVariable (problem 2)
        minvalues=float('inf')
        variable=None
        for key in self.remainingVariables(assignment):
            if len(domains[key])<minvalues:
                minvalues=len(domains[key])
                variable=key
        return variable

    def orderDomain(self, assignment: Dict[Variable, Value], domains: Dict[Variable, Set[Value]], var: Variable) -> List[Value]:
        """ Implement a smart ordering of the domain values. """
        if not self.LCV:
            return list(domains[var])
        else:
            lcvlength=float('inf')
            tempassignment=copy.deepcopy(assignment)
            hashconstraining={}
            listvals=domains[var]
            for val in domains[var]:
                amountConstraints=0
                tempassignment[var]=val
                listafter=self.forwardChecking(tempassignment,domains,var)
                for key in listafter:
                    amountConstraints += len(domains[key]) - len(listafter[key])
                hashconstraining[val]=amountConstraints
            sortedDict = {}
            sortedKeys = sorted(hashconstraining, key=hashconstraining.get)  # [1, 3, 2]
            for x in sortedKeys:
                sortedDict[x] = hashconstraining[x]
            returnlist=[]
            for key in sortedDict:
                returnlist.append(key)
            return returnlist
        # TODO: Implement CSP::orderDomain (problem 2)

    def solveAC3(self, initialAssignment: Dict[Variable, Value] = dict()) -> Optional[Dict[Variable, Value]]:
        """ Called to solve this CSP with AC3.
            Initializes domains and calls `CSP::_solveAC3`. """
        domains = domainsFromAssignment(initialAssignment, self.variables)
        domains = self.ac3(initialAssignment, domains)
        return self._solveAC3(initialAssignment, domains)

    @monitor
    def _solveAC3(self, assignment: Dict[Variable, Value], domains: Dict[Variable, Set[Value]]) -> Optional[Dict[Variable, Value]]:
        """
            Implement the actual backtracking algorithm with AC3.
            Use `CSP::ac3`.
            :return: a complete and valid assignment if one exists, None otherwise.
        """
        # TODO: Implement CSP::_solveAC3 (problem 3)
        if self.isComplete(assignment):
            return assignment
        var = self.selectVariable(assignment, domains)
        checklistvalid = copy.deepcopy(assignment)
        domainsarcConsitent=self.ac3(assignment,domains,var)
        if (self.checkkeyZero(domainsarcConsitent)):
            return False
        domainInOrders=self.orderDomain(assignment,domainsarcConsitent,var)
        for value in domainInOrders:
            checklistvalid[var] = value
            if (self.isValid(checklistvalid)):
                assignment[var] = value
                domainsarcConsitent[var]={value}
                result = self._solveAC3(assignment, domainsarcConsitent)
                if result != False:
                    return result
                del assignment[var]
        return False
    def createAllArcs(self,assignment,dom):
        listofarcs=[]
        for head in self.variables:
            for tail in self.variables:
                if head!=tail:
                    listofarcs.append((head,tail))
        return listofarcs
    def createAllArcsVar(self,assignment,dom,var):
        listofarcs=[]
        for head in self.variables:
            for tail in self.variables:
                if head!=tail:
                    if(tail==var):
                        listofarcs.append((head, tail))
        return listofarcs
    def removeInconsistentValues(self,assignment,domains,arc):
        tailvalset=set(domains[arc[0]])
        headvalset=set(domains[arc[1]])
        removed=False
        for tailval in tailvalset:
            found=False
            for headval in headvalset:
                if(self.isValidPairwise(arc[0],tailval,arc[1],headval)):
                    found=True
                    break
            if(found==False):
                domains[arc[0]].remove(tailval)
                removed=True
        return removed

    def calculateallneighbours(self):
        neigboursreturn={}
        for key in self.variables:
            neigboursreturn[key]=self.neighbors(key)
        return neigboursreturn
    def ac3(self, assignment: Dict[Variable, Value], domains: Dict[Variable, Set[Value]], variable: Optional[Variable] = None) -> Dict[Variable, Set[Value]]:
        """ Implement the AC3 algorithm from the theory lectures.

        :param domains: current domains.
        :param assignment: current assignment.
        :param variable: If not None, the variable that was just assigned (only need to check changes).
        :return: the new domains ensuring arc consistency.
        """
        # TODO: Implement CSP::ac3 (problem 3)
        returndomains=copy.deepcopy(domains)
        queue=self.createAllArcs(assignment,domains)
        neigb=self.calculateallneighbours()  #to not calculate the neigbours for every arc just calculate them all so that a variable enver gets called double to find the neighbours
        while len(queue)!=0:
            arc=queue.pop()
            removed=False
            if(arc[1] in neigb[arc[0]]):
                removed = self.removeInconsistentValues(assignment, returndomains, arc)
            if removed==True:
                for var in neigb[arc[0]]:
                    queue.append((var,arc[0]))
        return returndomains


def domainsFromAssignment(assignment: Dict[Variable, Value], variables: Set[Variable]) -> Dict[Variable, Set[Value]]:
    """ Fills in the initial domains for each variable.
        Already assigned variables only contain the given value in their domain.
    """
    domains = {v: v.startDomain for v in variables}
    for var, val in assignment.items():
        domains[var] = {val}
    return domains
