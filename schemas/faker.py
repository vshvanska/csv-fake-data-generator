from faker import Faker
from schemas.models import Column


class DataFaker:
    def __init__(self, column: Column) -> None:
        self.column = column
        self.fake = Faker()

    def get_integer(self) -> int:
        min = self.column.min_value
        max = self.column.max_value
        if min is not None and max is not None:
            return self.fake.random_int(min, max)
        if max is not None:
            return self.fake.random_int(max=max)
        if min is not None:
            return self.fake.random_int(min=min)
        return self.fake.random_int()

    def get_full_name(self) -> str:
        return self.fake.name()

    def get_job(self) -> str:
        return self.fake.job()

    def get_phone_number(self) -> str:
        return self.fake.phone_number()

    def get_company(self) -> str:
        return self.fake.company()

    def get_text(self) -> str:
        if self.column.max_value is not None:
            return self.fake.text(self.column.max_value)
        return self.fake.text()

    def get_date(self):
        return self.fake.date()

    def get_address(self):
        return self.fake.address()
