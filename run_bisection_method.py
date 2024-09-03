'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Fuad Hassan

@Date          : 09/03/2024

Using Bi-section method to solve algerbic equation

'''

import math
import sys
# from bisection_method import bisection

def bisection(f, x_L, x_R, eps=1.0e-6):
    f_L = f(x_L)
    f_R = f(x_R)

    if f_L * f_R > 0:
        print('Error! Function does not have opposite signs at interval endpoints!')
        sys.exit(1)

    x_M = (x_L + x_R) / 2.0
    f_M = f(x_M)
    iteration_counter = 1

    while abs(f_M) > eps:
        if f_L * f_M > 0:  # i.e., same sign
            x_L = x_M
            f_L = f_M
        else:
            x_R = x_M
        
        x_M = (x_L + x_R) / 2.0
        f_M = f(x_M)
        iteration_counter += 1

    return x_M, iteration_counter

def func1(x):
    '''
    function to solve equation the 2 x^3 - 5 x^2 + 1 = 0
    '''
    result = 2 * x**3 - 5 * x**2 + 1
    return(result)

def func2(x):
    '''
    function to solve the question sin(x) + x = 1
    '''
    result = math.sin(x) + x
    return(result)



def run():

    ''' TODO: 
    call bisection method to solve the equation x^3 - 2 x^2 + 1 = 0
    '''
    a = 0
    b = 1000
    solution, no_iterations = bisection(func1, a, b)
    
    print('Number of function calls: {:d}'.format(1 + 2 * no_iterations))
    print('A solution is: {:f}'.format(solution))
    '''
    end TODO
    '''


if __name__ == "__main__":
    run()
