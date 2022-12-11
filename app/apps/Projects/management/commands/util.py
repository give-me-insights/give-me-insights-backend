import kafka
import json

from django.core.management.base import CommandError

from apps.Projects.models import DataSource
from . import _KAFKA_CREDENTIALS, _KAFKA_GROUP_ID


def get_dict_depth(d: dict):
    if isinstance(d, dict):
        return 1 + (max(map(get_dict_depth, d.values())) if d else 0)
    return 0


class BaseKafkaConsumer:
    _consumer = kafka.KafkaConsumer(
        group_id=_KAFKA_GROUP_ID,
        # enable_auto_commit=False,
        auto_offset_reset='earliest',
        **_KAFKA_CREDENTIALS,
    )

    _producer = kafka.KafkaProducer(
        **_KAFKA_CREDENTIALS
    )

    def get_source_data_from_topic(self, topic: str) -> DataSource:
        _, company_key, project_key, source_key = topic.split("--")
        try:
            return DataSource.objects.get(
                key=source_key,
                project__key=project_key,
                project__company__key=company_key,
            )
        except DataSource.DoesNotExist:
            raise CommandError(f"No Datasource exists for topic {topic}")

    def get_message_dict(self, message: bytes) -> dict:
        encoded_message = json.loads(message.decode())
        depth = get_dict_depth(encoded_message)
        if depth != 1:
            raise CommandError("Bad Format for Message!")
        return encoded_message
