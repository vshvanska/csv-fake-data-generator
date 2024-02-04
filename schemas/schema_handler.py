import os

from datetime import datetime
from schemas.data_writer import DataWriter
from schemas.faker import DataFaker
from schemas.models import Schema, Column


class SchemaHandler:
    def __init__(self, schema: Schema):
        self.schema = schema
        self.file_name = f"{schema.id}_{schema.user_id}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    def get_columns(self):
        return list(Column.objects.filter(schema=self.schema.id).order_by("order"))

    def get_headers(self):
        columns = self.get_columns()
        return [column.name for column in columns]

    def create_data(self, rows):
        rows_to_write = []
        columns = self.get_columns()
        for row in range(rows):
            row = []
            for column in columns:
                row.append(self.get_column_data(column))
            rows_to_write.append(row)
        return rows_to_write
        self.write_data(headers, rows_to_write)

    @staticmethod
    def get_column_data(column: Column):
        datatype = column.data_type
        faker = DataFaker(column)
        if datatype == "Integer":
            return faker.get_integer()
        if datatype == "Full name":
            return faker.get_full_name()
        if datatype == "Job":
            return faker.get_job()
        if datatype == "Phone number":
            return faker.get_phone_number()
        if datatype == "Company":
            return faker.get_company()
        if datatype == "Text":
            return faker.get_text()
        if datatype == "Date":
            return faker.get_date()
        if datatype == "Address":
            return faker.get_address()

    def write_data(self, headers, rows_to_write):
        writer = DataWriter(headers,
                            rows_to_write,
                            self.file_name,
                            self.schema.column_separator,
                            self.schema.string_character)
        return writer.write_data()
