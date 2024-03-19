from scipy.optimize import linprog
import sys

TOTAL = 100

def AtoD(A):
    if A > 0:
        return 1 + A/100
    else:
        return 1 + 100/abs(A)

def FourParlaysAmerican(a1,a2,a3,a4,a5,a6,a7,a8,total):
    return FourParlays(AtoD(a1), AtoD(a2), AtoD(a3), AtoD(a4), AtoD(a5), AtoD(a6), AtoD(a7), AtoD(a8), total)

def FourParlays(o1,o2,o3,o4,o5,o6,o7,o8, total):
    # Set up values relating to both minimum and maximum values of y
    coefficients_inequalities = [[-o1*o5, 0, 0, 0], [0, -o4*o8, 0, 0], [0, 0, -o1*o6, 0], [0, 0, 0, -o4*o7]]  # require -1*x + -1*y <= -180
    constants_inequalities = [-total, -total, -total, -total]
    coefficients_equalities = [[1, 1, 1, 1], [o1*o5, -o4*o8, 0, 0], [o1*o5, 0, -o1*o6, 0], [o1*o5, 0, 0, -o4*o7], [0, o4*o8, -o1*o6, 0], [0, o4*o8, 0, -o4*o7], [0, 0, o1*o6, -o4*o7]]  # require 3*x + 12*y = 1000
    constants_equalities = [total, 0,0,0,0,0,0]
    # Objective function
    coefficients_min_y = [1, 1, 1, 1]  
    # Optimize
    res = linprog(coefficients_min_y,
                  A_ub=coefficients_inequalities,
                  b_ub=constants_inequalities,
                  A_eq=coefficients_equalities,
                  b_eq=constants_equalities)
    # Compute ROI
    ROI = [o1*o5*res.x[0], o4*o8*res.x[1], o1*o6*res.x[2], o4*o7*res.x[3]]
    print(ROI)
    return res.x



def is3WayArbAmerican(a1, a2, a3):
    o1 = AtoD(a1)
    o2 = AtoD(a2)
    o3 = AtoD(a3)
    return o1*o2*o3 > o1*o2 + o1*o3 + o2*o3

def findOddsWithArb(a1,a2,a3,b1,b2,b3):
    a = [a1,a2,a3]
    b = [b1,b2,b3]
    odd_sets_with_arbs = []
    # With one a
    for i in range(0, 3):
        for j in range(0, 3):
        # exclude b[j]
            if is3WayArbAmerican(a[i], b[j-1], b[(j+1)%3]):
                odd_sets_with_arbs.append([a[i], b[j-1], b[(j+1)%3]])
    # With one b
    for i in range(0, 3):
        for j in range(0, 3):
        # exclude b[j]
            if is3WayArbAmerican(b[i], a[j-1], a[(j+1)%3]):
                odd_sets_with_arbs.append([b[i], a[j-1], a[(j+1)%3]])



# Decimal odds assumed
def computeWagers(odds1, odds2, total):
    # Set up values relating to both minimum and maximum values of y
    coefficients_inequalities = [[-odds1, 0], [0, -odds2]]  # require -1*x + -1*y <= -180
    constants_inequalities = [-total, -total]
    coefficients_equalities = [[1, 1], [-odds1, odds2]]  # require 3*x + 12*y = 1000
    constants_equalities = [total, 0]
    # Objective function
    coefficients_min_y = [1, 1]  
    # Optimize
    res = linprog(coefficients_min_y,
                  A_ub=coefficients_inequalities,
                  b_ub=constants_inequalities,
                  A_eq=coefficients_equalities,
                  b_eq=constants_equalities)
    return res.x

# Decimal odds assumed
def computeWagers(odds1, odds2, total):
    # Set up values relating to both minimum and maximum values of y
    coefficients_inequalities = [[-odds1, 0], [0, -odds2]]  # require -1*x + -1*y <= -180
    constants_inequalities = [-total, -total]
    coefficients_equalities = [[1, 1], [-odds1, odds2]]  # require 3*x + 12*y = 1000
    constants_equalities = [total, 0]
    # Objective function
    coefficients_min_y = [1, 1]  
    # Optimize
    res = linprog(coefficients_min_y,
                  A_ub=coefficients_inequalities,
                  b_ub=constants_inequalities,
                  A_eq=coefficients_equalities,
                  b_eq=constants_equalities)
    return res.x

if __name__ == "__main__":
    while True:
        [a1, a2] = list(map(int, input().split()))
        o1 = AtoD(a1)
        o2 = AtoD(a2)
        [x, y] = computeWagers(o1, o2, int(sys.argv[1]))
        print(x,y)
        print("Payoff1: {}, Payoff2: {}".format(x*o1, y*o2))
    """
    ret = FourParlaysAmerican(110,-125,-105,100,120,-135,100,-105,TOTAL)
    # Compute ROI
    print(ret)
    """
