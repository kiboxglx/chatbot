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

    def get_summary(self, user_phone: str, start_date: datetime = None, end_date: datetime = None):
        db = SessionLocal()
        try:
            query = db.query(Expense).filter(Expense.user_phone == user_phone)
            
            if start_date:
                query = query.filter(Expense.date >= start_date)
            if end_date:
                query = query.filter(Expense.date <= end_date)
                
            results = query.all()
            
            if not results:
                return {
                    "total": 0.0,
                    "count": 0,
                    "average": 0.0,
                    "top_category": None,
                    "categories": [],
                    "period_label": "Nenhum dado no período"
                }

            total = sum(e.amount for e in results)
            count = len(results)
            average = total / count if count > 0 else 0
            
            # Agrupamento e cálculo de porcentagens
            cat_map = {}
            for e in results:
                cat_name = e.category or "Outros"
                cat_map[cat_name] = cat_map.get(cat_name, 0.0) + e.amount
            
            # Ordena categorias do maior para menor
            sorted_cats = sorted(cat_map.items(), key=lambda x: x[1], reverse=True)
            
            categories_data = []
            for name, amount in sorted_cats:
                pct = (amount / total * 100) if total > 0 else 0
                categories_data.append({
                    "name": name,
                    "amount": amount,
                    "percentage": pct
                })
                
            top_category = categories_data[0] if categories_data else None

            return {
                "count": count,
                "total": total,
                "average": average,
                "top_category": top_category,
                "categories": categories_data,
                "expenses": results[-5:] # Últimos 5 para log
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
