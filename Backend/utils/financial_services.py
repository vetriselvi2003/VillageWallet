import random
from datetime import datetime
from utils.database import get_db, User, Loan, Savings, Transaction, CreditData
from sqlalchemy.orm import Session

class FinancialServices:
    def __init__(self):
        self.max_loan_amount = 5000
        self.min_loan_amount = 500
        self.base_interest_rate = 0.03
        self.savings_interest_rate = 0.08
    
    def calculate_credit_score(self, user_id):
        db = next(get_db())
        try:
            credit_data = db.query(CreditData).filter(CreditData.user_id == user_id).first()
            if not credit_data:
                credit_data = CreditData(
                    user_id=user_id,
                    upi_transaction_count=random.randint(10, 50),
                    avg_monthly_spending=random.uniform(2000, 8000),
                    utility_payment_history=random.uniform(0.7, 0.95)
                )
                db.add(credit_data)
                db.commit()
            score = 0
            if credit_data.upi_transaction_count > 30:
                score += 300
            elif credit_data.upi_transaction_count > 15:
                score += 200
            else:
                score += 100
            if 3000 <= credit_data.avg_monthly_spending <= 6000:
                score += 200
            elif credit_data.avg_monthly_spending > 6000:
                score += 150
            else:
                score += 100
            score += int(credit_data.utility_payment_history * 300)
            score += random.randint(100, 200)
            credit_score = max(300, min(850, score))
            credit_data.calculated_score = credit_score
            credit_data.last_updated = datetime.utcnow()
            db.commit()
            return credit_score
        finally:
            db.close()
    
    def check_loan_eligibility(self, user_id, requested_amount):
        if requested_amount < self.min_loan_amount or requested_amount > self.max_loan_amount:
            return False, f"Loan amount must be between ₹{self.min_loan_amount} and ₹{self.max_loan_amount}"
        credit_score = self.calculate_credit_score(user_id)
        if credit_score < 400:
            return False, "Credit score too low. Build your credit history first."
        db = next(get_db())
        try:
            active_loans = db.query(Loan).filter(
                Loan.user_id == user_id,
                Loan.status.in_(['pending', 'active'])
            ).count()
            if active_loans > 0:
                return False, "You already have an active loan. Please complete it first."
            return True, "You are eligible for this loan!"
        finally:
            db.close()
    
    def process_loan_application(self, user_id, amount, duration_months=6):
        db = next(get_db())
        try:
            eligible, message = self.check_loan_eligibility(user_id, amount)
            if not eligible:
                return False, message
            monthly_payment = (amount * (1 + self.base_interest_rate)) / duration_months
            loan = Loan(
                user_id=user_id,
                amount=amount,
                interest_rate=self.base_interest_rate,
                duration_months=duration_months,
                monthly_payment=monthly_payment,
                status='pending'
            )
            db.add(loan)
            db.commit()
            return True, f"Loan application submitted! Monthly payment: ₹{monthly_payment:.2f}"
        finally:
            db.close()
    
    def get_savings_balance(self, user_id):
        db = next(get_db())
        try:
            savings = db.query(Savings).filter(Savings.user_id == user_id).first()
            if not savings:
                savings = Savings(user_id=user_id)
                db.add(savings)
                db.commit()
            return savings.balance
        finally:
            db.close()
    
    def add_savings(self, user_id, amount):
        db = next(get_db())
        try:
            savings = db.query(Savings).filter(Savings.user_id == user_id).first()
            if not savings:
                savings = Savings(user_id=user_id)
                db.add(savings)
            savings.balance += amount
            savings.last_updated = datetime.utcnow()
            db.commit()
            transaction = Transaction(
                user_id=user_id,
                transaction_type='savings',
                amount=amount,
                description=f"Savings deposit of ₹{amount}"
            )
            db.add(transaction)
            db.commit()
            return True, f"₹{amount} added to savings. New balance: ₹{savings.balance}"
        finally:
            db.close()
    
    def get_insurance_recommendations(self, user_id):
        return [
            {
                'type': 'Livestock Insurance',
                'premium': '₹50/year',
                'coverage': 'Up to ₹5,000 per animal',
                'description': 'Protects against livestock death/disease'
            },
            {
                'type': 'Crop Insurance',
                'premium': '₹100/year',
                'coverage': 'Up to ₹10,000 per acre',
                'description': 'Protects against crop failure'
            },
            {
                'type': 'Health Insurance',
                'premium': '₹200/year',
                'coverage': 'Up to ₹50,000',
                'description': 'Basic health coverage for family'
            }
        ]

# For testing
if __name__ == "__main__":
    fs = FinancialServices()
    user_id = 1  # Replace with a real user ID from your database
    print("➡️ Insurance options:")
    print(fs.get_insurance_recommendations(user_id))
