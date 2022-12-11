import kafka
import json

from collections import OrderedDict

from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand, CommandError

from apps.Projects.models import DataSource, SourceDataSchemaMapping

from . import _KAFKA_CREDENTIALS, _KAFKA_GROUP_ID


def get_dict_depth(d: dict):
    if isinstance(d, dict):
        return 1 + (max(map(get_dict_depth, d.values())) if d else 0)
    return 0


class Command(BaseCommand):
    _consumer = kafka.KafkaConsumer(
        group_id=_KAFKA_GROUP_ID,
        # enable_auto_commit=False,
        auto_offset_reset='earliest',
        **_KAFKA_CREDENTIALS,
    )

    _producer = kafka.KafkaProducer(
        **_KAFKA_CREDENTIALS
    )

    def get_source_data_from_dip_topic(self, topic: str) -> DataSource:
        _, company_key, project_key, source_key = topic.split("--")
        try:
            return DataSource.objects.get(
                key=source_key,
                project__key=project_key,
                project__company__key=company_key,
            )
        except DataSource.DoesNotExist:
            raise CommandError(f"No Datasource exists for topic {topic}")

    def register_field_mapping(self, source: DataSource, *message_keys):
        filtered_message_keys = [key for key in message_keys if key != "timestamp"]
        mapping = {f'key_{i}': key for i, key in enumerate(filtered_message_keys)}
        try:
            SourceDataSchemaMapping.objects.create(source=source, mapping=mapping)
        except IntegrityError:
            return

    def get_message_dict(self, message: bytes) -> dict:
        encoded_message = json.loads(message.decode())
        depth = get_dict_depth(encoded_message)
        if depth != 1:
            raise CommandError("Bad Format for Message!")
        return encoded_message

    def generalize_message(self, message: dict) -> dict:
        timestamp = message.pop("timestamp")
        generalized_message = OrderedDict([(f"key_{i}", value) for i, value in enumerate(message.values())])
        generalized_message.update({"timestamp": timestamp})
        generalized_message.move_to_end("timestamp", last=False)
        return dict(generalized_message)

    def get_outbound_topic(self, source: DataSource):
        # RFMT: Raw Formatted Message Topic
        return f"RFMV--{source.project.company.key}--{source.project.key}--{source.key}"

    def handle(self, *args, **options):
        self._consumer.subscribe(pattern="DIT--(.*?)")
        for message in self._consumer:
            try:
                source_data = self.get_source_data_from_dip_topic(message.topic)
                message_value = self.get_message_dict(message.value)
                self.register_field_mapping(source_data, *list(message_value.keys()))
                generalized_message = self.generalize_message(message_value)
                outbound_topic = self.get_outbound_topic(source_data)
                self._producer.send(topic=outbound_topic, value=json.dumps(generalized_message).encode())
            except Exception as e:
                self.stdout.write(f"Failure for message. Message will be ignored. {e}")
