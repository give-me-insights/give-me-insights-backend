import json

from collections import OrderedDict

from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand

from apps.Projects.models import DataSource, SourceDataSchemaMapping

from .util import BaseKafkaConsumer


def get_dict_depth(d: dict):
    if isinstance(d, dict):
        return 1 + (max(map(get_dict_depth, d.values())) if d else 0)
    return 0


class Command(BaseCommand, BaseKafkaConsumer):
    def register_field_mapping(self, source: DataSource, *message_keys):
        filtered_message_keys = [key for key in message_keys if key != "timestamp"]
        mapping = {f'key_{i}': key for i, key in enumerate(filtered_message_keys)}
        try:
            SourceDataSchemaMapping.objects.create(source=source, mapping=mapping)
        except IntegrityError:
            return

    def generalize_message(self, message: dict) -> dict:
        timestamp = message.pop("timestamp")
        generalized_message = OrderedDict([(f"key_{i}", value) for i, value in enumerate(message.values())])
        generalized_message.update({"timestamp": timestamp})
        generalized_message.move_to_end("timestamp", last=False)
        return dict(generalized_message)

    def get_outbound_topic(self, source: DataSource):
        # RFMT: Raw Formatted Message Topic (trusted topic)
        return f"RFMT--{source.project.company.key}--{source.project.key}--{source.key}"

    def handle(self, *args, **options):
        # TODO - High: Resubscribe -> Topic Spawn in Multithread?
        self._consumer.subscribe(pattern="DIT--(.*?)")
        for message in self._consumer:
            try:
                self.stdout.write(f"Consume Inbound Data from Topic {message.topic}")
                source_data = self.get_source_data_from_topic(message.topic)
                message_value = self.get_message_dict(message.value)
                self.register_field_mapping(source_data, *list(message_value.keys()))
                generalized_message = self.generalize_message(message_value)
                outbound_topic = self.get_outbound_topic(source_data)
                self._producer.send(topic=outbound_topic, value=json.dumps(generalized_message).encode())
            except Exception as e:
                self.stdout.write(f"Failure for message. Message will be ignored. {e}")
