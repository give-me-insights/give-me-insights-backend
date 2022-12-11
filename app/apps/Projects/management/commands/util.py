import logging

import kafka
import json
import threading
from time import sleep
from functools import partial
from abc import abstractmethod

from django.core.management.base import BaseCommand, CommandError

from apps.Projects.models import DataSource
from . import _KAFKA_CREDENTIALS, _KAFKA_GROUP_ID


def get_dict_depth(d: dict):
    if isinstance(d, dict):
        return 1 + (max(map(get_dict_depth, d.values())) if d else 0)
    return 0


logger = logging.getLogger(__name__)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

# fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)



class BaseKafkaConsumer(BaseCommand):
    _topic_prefix: str = ""

    _consumer = kafka.KafkaConsumer(
        group_id=f"{_KAFKA_GROUP_ID}",
        # enable_auto_commit=False,
        auto_offset_reset='earliest',
        **_KAFKA_CREDENTIALS,
    )

    _producer = kafka.KafkaProducer(
        **_KAFKA_CREDENTIALS
    )

    @abstractmethod
    def handle_message(self, message, **kwargs):
        pass

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

    def handle(self, *args, **options):
        i = 10
        while True:
            if i % 10 == 0:
                self._consumer.subscribe(pattern=f"{self._topic_prefix}--(.*?)")
            poll = self._consumer.poll(timeout_ms=500)
            i += 1
            for _, messages in poll.items():
                for message in messages:
                    try:
                        self.stdout.write(f"Start Processing message from topic {message.topic}")
                        self.handle_message(message)
                    except Exception as e:
                        self.stdout.write(f"Message got not processed. Error: {e}")
