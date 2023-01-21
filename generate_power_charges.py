import os
from datetime import datetime

import numpy as np
import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

from acnportal import acnsim, algorithms

load_dotenv()

API_KEY = os.getenv("API_KEY")

TIMEZONE = pytz.timezone("America/Los_Angeles")

PERIOD = 1 # minutes

VOLTAGE = 220  # volts

DEFAULT_BATTERY_POWER = 32 * VOLTAGE / 1000  # kW

SITE = "caltech"

SCH = algorithms.UncontrolledCharging()

def simulate(ndevice=1):
    """
    Given a number of device to simulate, the function simaltes their recharge in the acn portal.
    It return a dataframe containing the siumaltions of recharge.
    """
    start = datetime(2020, 3, 1)
    end = datetime(2020, 3, 30)

    final_df = pd.DataFrame(columns=["Id", "Timestamp", "Power"])
    cn = acnsim.sites.caltech_acn(basic_evse=True, voltage=VOLTAGE)

    for i in range(ndevice):

        events = acnsim.acndata_events.generate_events(
            API_KEY, SITE, TIMEZONE.localize(start), TIMEZONE.localize(end), PERIOD, VOLTAGE, DEFAULT_BATTERY_POWER
        )
        sim = acnsim.Simulator(cn, SCH, events, TIMEZONE.localize(start), period=PERIOD)
        sim.run()

        array_timestamp = acnsim.datetimes_array(sim)
        # Pritn energy delivered
        array_power = acnsim.aggregate_power(sim)
        #cost = acnsim.energy_cost(sim, tariff=None)
        array_id = np.repeat(f"id{i}", array_power.shape[0])

        _df = pd.DataFrame(columns=["Id", "Timestamp", "Power"])
        _df["Id"] = array_id
        _df["Timestamp"] = array_timestamp
        _df["Power"] = array_power

        final_df = pd.concat([final_df, _df], ignore_index=True)

        # new device, new month
        start += relativedelta(months=1)
        end += relativedelta(months=1)

    final_df.to_csv("./static/simulations.csv")
    return final_df

simulate(2)