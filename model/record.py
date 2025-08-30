from dataclasses import dataclass
import datetime
from decimal import Decimal

@dataclass
class Record:
    date: datetime.date
    location: str
    category: str
    amount: Decimal

    def __post_init__(self):
        """
        convert date and amount to the correct types
        """
        if not isinstance(self.date, datetime.date):
            try:
                self.date = datetime.date.fromisoformat(self.date)
            except:
                raise ValueError(f'Invalid date initialization: {self.date}')

        if not isinstance(self.amount, Decimal):
            try:
                self.amount = Decimal(str(self.amount))
            except:
                raise ValueError(f'Invalid amount initialization: {self.amount}')

    def is_expense(self) -> bool:
        return self.amount < 0

    def date_str(self) -> str:
        return str(self.date)

    def amount_str(self) -> str:
        return f'{self.amount:.2f}'

    def asdict(self):
        return {'date': self.date_str(), 'location': self.location, 'category': self.category, 'amount': self.amount_str()}
