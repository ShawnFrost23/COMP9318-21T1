## import modules here 

################# Question 0 #################

def add(a, b): # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x): # do not change the heading of the function
    if x < 2:
        return x
    else:
        lower = nsqrt(x // 4) * 2
        higher = lower + 1
        
        if (higher * higher) > x:
            return lower
        else:
            return higher


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them

def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    # let y = x_0
    y = x_0
    
    for i in range(MAX_ITER):
        x = y
        y = x - f(x) / fprime(x)
        
        if abs(x - y) < EPSILON:
            break
    
    return y


################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)
        
def treeHelper(parent, tokens, startPointer, endPointer):
    if (startPointer <= endPointer) and (parent != None):
        i = 0
        while startPointer + i <= endPointer:
            branch = None
            while (startPointer + i <= endPointer) and (tokens[startPointer + i] != '[') and (tokens[startPointer + i] != ']'):
                branch = Tree(tokens[startPointer + i])
                parent.add_child(branch)
                i += 1
            
            if startPointer + i <= endPointer:
                if tokens[startPointer + i] == '[':
                    i += 1
                    i += treeHelper(branch, tokens, startPointer + i, endPointer)
                elif tokens[startPointer + i] == ']':
                    i += 1
                    return i
        return i
    return 0
                

def make_tree(tokens): # do not change the heading of the function
    if len(tokens) == 0:
        return None
    else: 
        returnTree = Tree(tokens[0])
        if len(tokens) > 1 and tokens[1] == '[':
            treeHelper(returnTree, tokens, 1, len(tokens) - 1)
        return returnTree

        

def max_depth(root): # do not change the heading of the function
    if root == None:
        return 0
    
    depth = 1
    maxBranchDepth = 0;
    if len(root.children) > 0:
        for branch in root.children:
            branchDepth = max_depth(branch)
            if branchDepth > maxBranchDepth:
                maxBranchDepth = branchDepth

    return depth + maxBranchDepth
