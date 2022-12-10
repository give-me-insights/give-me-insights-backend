import os

if os.environ["ENV"] == "dev":
  from .local import *  # noqa
else:
  from .prod import *  # noqa
