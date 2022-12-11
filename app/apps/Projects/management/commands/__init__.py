import os


_KAFKA_CREDENTIALS = {
    "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVER"),
    "sasl_plain_username": os.getenv("KAFKA_SASL_PLAIN_USERNAME"),
    "sasl_plain_password": os.getenv("KAFKA_SASL_PLAIN_PASSWORD"),
    "sasl_mechanism": "SCRAM-SHA-512",
    "security_protocol": os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_SSL"),
}

_KAFKA_GROUP_ID = f'gmi-webapp-{os.getenv("ENV", )}'
