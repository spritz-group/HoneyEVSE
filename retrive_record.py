import os
from datetime import datetime

import numpy as np
import pandas as pd
import pytz
from dotenv import load_dotenv

from acnportal import acndata

load_dotenv()
API_KEY = os.getenv("API_KEY")

df = pd.read_csv("./all.csv")

#print(df.groupby("stationID").count())

print(df[["stationID", "connectionTime", "disconnectTime", "doneChargingTime", "kWhDelivered"]].sort_values(by="stationID")[df.stationID == "2-39-123-23"])



""" client = acndata.DataClient(API_KEY)

df = pd.DataFrame(client.get_sessions("caltech"))

df.to_csv("./all.csv")

print("Done") """