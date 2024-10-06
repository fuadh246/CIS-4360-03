'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Fuad Hassan

@Date          : Fall 2024

A Simple Mortgage Calculator
'''

import sys
import math
from bisection_method import bisection

class MortgageCalculator(object):

    def __init__(self, loan_amount, int_rate, term):
        self.loan_amount = loan_amount
        self.int_rate = int_rate
        self.term = term

    def _calc_next_month_balance(self, prev_balance, level_payment, int_rate):
        next_month = prev_balance * (1+ (int_rate/12)) - level_payment
        return next_month
    
    def _last_month_balance(self, level_payment):

        prev_bal = self.loan_amount
        months = self.term * 12
        
        for _ in range(months):
            prev_bal = self._calc_next_month_balance(prev_bal,level_payment,self.int_rate)
            
        return prev_bal
        
    def calc_level_payment(self):
        # Calculate level payment using numerical methods
        def func(level_payment):
            return self._last_month_balance(level_payment)
        
        a = self.loan_amount * (1+self.int_rate * self.term)/(12*self.term)
        b = a/2
        
        level_payment, _ = bisection(func, a, b, 1e-6)
        return level_payment

    def compute_level_payment_analytically(self):
        # use the analytical formula to compute the level payment
        monthly_interest = self.int_rate / 12  # Monthly interest rate
        months = self.term * 12  # Total number of months
        
        level_payment = (self.loan_amount * monthly_interest)/(1 - (1 + monthly_interest) ** -months)
        return level_payment
        

    
def _test():
    #
    loan_amount = 240000
    int_rate = 0.05
    mortgage_term = 30

    mtgCalc = MortgageCalculator(loan_amount, int_rate, mortgage_term)
    print(mtgCalc.calc_level_payment())
    
def _test2():
    cases = [
        (240000, 0.05, 30),  # Test 1
        (300000, 0.04, 15),  # Test 2
        (180000, 0.035, 20)  # Test 3
    ]
    
    for loan_amount, int_rate, term in cases:
        mtgCalc = MortgageCalculator(loan_amount, int_rate, term)
        level_payment_numerical = mtgCalc.calc_level_payment()
        level_payment_analytical = mtgCalc.compute_level_payment_analytically()
        
        print(f"Loan Amount: ${loan_amount}, Interest Rate: {int_rate * 100}%, Term: {term} years")
        print(f"Numerical Level Payment: ${level_payment_numerical:.5f}")
        print(f"Analytical Level Payment: ${level_payment_analytical:.5f}")
        print("-" * 50)


if __name__ == "__main__":
    _test2()
