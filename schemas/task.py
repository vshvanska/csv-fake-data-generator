from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from schemas.data_writer import DataWriter
from schemas.models import Schema, DataSet
from schemas.schema_handler import SchemaHandler


@shared_task
def create_fake_data(dataset_id, schema_id):
    schema = Schema.objects.get(pk=schema_id)
    dataset = DataSet.objects.get(pk=dataset_id)
    schema_handler = SchemaHandler(schema)
    headers = schema_handler.get_headers()
    rows_to_write = schema_handler.create_data(dataset.number_of_rows)
    path = schema_handler.file_name
    writer = DataWriter(
        headers,
        rows_to_write,
        path,
        schema_handler.schema.column_separator,
        schema_handler.schema.string_character,
    )
    writer.write_data()
    dataset.file = path
    dataset.is_ready = True
    dataset.save()
    user = get_user_model().objects.get(pk=schema.user_id)
    send_data_ready_email.delay([user.email])


@shared_task()
def send_data_ready_email(emails: list):
    return send_mail(
        "Dataset",
        "Your dataset is ready. You can download it in your personal cabinet",
        "datafakercsv@gmail.com",
        emails,
    )
