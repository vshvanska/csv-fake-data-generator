from celery import shared_task

from schemas.data_writer import DataWriter
from schemas.models import Schema
from schemas.schema_handler import SchemaHandler


@shared_task
def create_fake_data(schema_id):
    schema = Schema.objects.get(pk=schema_id)
    print(schema)
    schema_handler = SchemaHandler(schema)
    headers = schema_handler.get_headers()
    print(headers)
    rows_to_write = schema_handler.create_data()
    print(rows_to_write)
    writer = DataWriter(headers,
                        rows_to_write,
                        schema_handler.file_name,
                        schema_handler.schema.column_separator,
                        schema_handler.schema.string_character)
    return writer.write_data()
