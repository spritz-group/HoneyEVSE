import os
import signal
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from numpy import repeat

from acnportal import acnsim, algorithms

load_dotenv()

API_KEY = os.getenv("API_KEY")

TIMEZONE = pytz.timezone("America/Los_Angeles")

PERIOD = 1 # minutes

VOLTAGE = 220  # volts

DEFAULT_BATTERY_POWER = 32 * VOLTAGE / 1000  # kW

SITE = "caltech"

SCH = algorithms.UncontrolledCharging()

def signal_handler(sig, frame):
    print("Blocking the simulations...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def simulate(ndevices=1):
    """
    Given a number of device to simulate, the function simaltes their recharge in the acn portal.
    It return a dataframe containing the siumaltions of recharge.
    """
    start = datetime(2020, 3, 1)
    end = datetime(2020, 3, 30)

    df_simulations = pd.DataFrame(columns=["id", "energy"])
    cn = acnsim.sites.caltech_acn(basic_evse=True, voltage=VOLTAGE)

    for i in range(ndevice):

        events = acnsim.acndata_events.generate_events(
            API_KEY, SITE, TIMEZONE.localize(start), TIMEZONE.localize(end), PERIOD, VOLTAGE, DEFAULT_BATTERY_POWER
        )
        sim = acnsim.Simulator(cn, SCH, events, TIMEZONE.localize(start), period=PERIOD)
        sim.run()

        # Print energy delivered
        array_power = acnsim.aggregate_power(sim)
        # Generate the id for the ev
        array_id = repeat(f"id{i}", array_power.shape[0])

        _df_partial = pd.DataFrame({"id": array_id, "energy": array_power})

        df_simulations = pd.concat([df_simulations, _df_partial], ignore_index=True)

        # new device, new month
        start += relativedelta(months=1)
        end += relativedelta(months=1)

    df_simulations.to_csv("./static/simulations.csv", index=False)
    return df_simulations

simulate(2)