from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from apps.Projects.models import SourceDataRowRaw, DataSource

from .util import BaseKafkaConsumer


def get_dict_depth(d: dict):
    if isinstance(d, dict):
        return 1 + (max(map(get_dict_depth, d.values())) if d else 0)
    return 0


class Command(BaseCommand, BaseKafkaConsumer):
    def insert_row(self, source: DataSource, message: dict):
        timestamp = datetime.fromtimestamp(int(message.pop("timestamp")))
        try:
            SourceDataRowRaw.objects.create(source=source, timestamp=timestamp, value=message, type="r")
        except IntegrityError:
            raise CommandError(f"Insert Raw Source Data Row {message} for source {source.key} Failed.")

    def handle(self, *args, **options):
        self._consumer.subscribe(pattern="RFMT--(.*?)")
        for message in self._consumer:
            self.stdout.write(f"Consume Inbound Data from Topic {message.topic}")
            try:
                source_data = self.get_source_data_from_topic(message.topic)
                message_value = self.get_message_dict(message.value)
                self.insert_row(source_data, message_value)
            except Exception as e:
                self.stdout.write(f"Failure for message. Message will be ignored. {e}")
