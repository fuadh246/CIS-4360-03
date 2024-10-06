'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Fuad Hassan

@Date          : Fall 2024

Basic Mortgage Calculation

'''

import sys
import math
from bisection_method import bisection

def calc_next_month_balance(prev_balance, level_payment, int_rate):
    # return next month balance 
    monthly_interest = int_rate/12
    next_month = prev_balance * (1+ monthly_interest) - level_payment
    #return ...
    return next_month

def last_month_balance(loan_amount, int_rate, mortgage_term, level_payment):
    # calculate the last month remaining balance
    # mortgage_term is the number of years for the mortgage
    # int_rate is the annual interest rate in fraction

    prev_bal = loan_amount
    prev_bal = loan_amount
    months = mortgage_term * 12 # year to months 
    
    for _ in range(months):
        prev_bal = calc_next_month_balance(prev_balance=prev_bal, level_payment=level_payment, int_rate= int_rate)
    return(prev_bal)


def calc_level_payment(loan_amount, int_rate, mortgage_term):
    # calculate the level payment by defining a function that return the last month balance
    # then use the bisection method to require the last month balance to be zero
    a = loan_amount * (1+int_rate * mortgage_term)/(12*mortgage_term)
    b = a/2


    def func(level_payment):
        return last_month_balance(loan_amount, int_rate, mortgage_term, level_payment)
    #
    # call bisection with the func
    level_payment,_ = bisection(func,a,b,1e-6)
    # return answer
    return level_payment
    
def test():
    loan_amount = 240000
    int_rate = 0.05
    term = 30
    level_payment = loan_amount * (1+int_rate * term)/(12*term) / 2
    print(level_payment)
    print(last_month_balance(loan_amount, int_rate, term, level_payment))
    
def run():
    #
    loan_amount = 240000
    int_rate = 0.05
    mortgage_term = 30

    print(calc_level_payment(loan_amount, int_rate, mortgage_term))

def test2():
    cases = [
        (240000, 0.05, 30),  # Test 1
        (300000, 0.04, 15),  # Test 2
        (180000, 0.035, 20)  # Test 3
    ]
    
    for loan_amount, int_rate, term in cases:
        level_payment = calc_level_payment(loan_amount, int_rate, term)
        remaining_balance = last_month_balance(loan_amount, int_rate, term, level_payment)
        print(f"Loan Amount: ${loan_amount}, Interest Rate: {int_rate*100}%, Term: {term} years")
        print(f"Monthly Payment: ${level_payment:.5f}")
        print(f"Remaining Balance at the end: ${remaining_balance:.5f}")
        print("-" * 50)

if __name__ == "__main__":
    # test()
    # run()
    test2()