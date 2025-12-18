from datetime import datetime
from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.core.database import SessionLocal

class ExpenseService:
    def __init__(self):
        pass

    def save_expense(self, description: str, amount: float, category: str, user_phone: str):
        db = SessionLocal()
        try:
            db_expense = Expense(
                description=description,
                amount=amount,
                category=category,
                user_phone=user_phone,
                date=datetime.now()
            )
            db.add(db_expense)
            db.commit()
            db.refresh(db_expense)
            return db_expense
        finally:
            db.close()

    def get_summary(self, user_phone: str):
        db = SessionLocal()
        try:
            results = db.query(Expense).filter(Expense.user_phone == user_phone).all()
            total = sum(e.amount for e in results)
            
            # Agrupamento por categoria
            by_category = {}
            for e in results:
                cat = e.category or "Outros"
                by_category[cat] = by_category.get(cat, 0.0) + e.amount
                
            return {
                "count": len(results),
                "total": total,
                "by_category": by_category,
                "expenses": results[-10:] # Retorna os últimos 10 para detalhar se precisar
            }
        finally:
            db.close()

    def get_monthly_report(self, user_phone: str, month: int, year: int):
        db = SessionLocal()
        try:
            # Simplificado para o exemplo, em prod usaria extract do sqlalchemy
            all_expenses = db.query(Expense).filter(Expense.user_phone == user_phone).all()
            filtered = [
                e for e in all_expenses 
                if e.date.month == month and e.date.year == year
            ]
            total = sum(e.amount for e in filtered)
            return {
                "month": month,
                "year": year,
                "total": total,
                "count": len(filtered),
                "expenses": filtered
            }
        finally:
            db.close()
