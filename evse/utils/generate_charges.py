import json
import os
from datetime import datetime

import pytz
from acnportal import acnsim, algorithms
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

from utils.ev_charge import EvCharge

load_dotenv()

API_KEY = os.getenv("API_KEY")

TIMEZONE = pytz.timezone("America/Los_Angeles")

PERIOD = 5 # minutes

VOLTAGE = 220  # volts

DEFAULT_BATTERY_POWER = 32 * VOLTAGE / 1000  # kW

SITE = "caltech"

SCH = algorithms.UncontrolledCharging()

def simulate(nsimulations=1, file_path="../static/charges.json"):
    """
    Given a number of device to simulate, the function simaltes their recharge in the acn portal.
    It return a dataframe containing the siumaltions of recharge.
    """
    start = datetime(2020, 3, 1)
    end = datetime(2020, 3, 2)

    list_ev_charges = []
    cn = acnsim.sites.caltech_acn(basic_evse=True, voltage=VOLTAGE)

    for i in range(nsimulations):

        events = acnsim.acndata_events.generate_events(
            API_KEY, SITE, TIMEZONE.localize(start), TIMEZONE.localize(end), PERIOD, VOLTAGE, DEFAULT_BATTERY_POWER
        )
        sim = acnsim.Simulator(cn, SCH, events, TIMEZONE.localize(start), period=PERIOD)
        sim.run()

        df_charging_rates = sim.charging_rates_as_df()
        dict_ev = sim.ev_history

        for ev in dict_ev.values():
            id = "ev" + str(i)
            ev_charge = EvCharge(id, ev.arrival, ev.departure, ev.requested_energy, ev.station_id)
            valid_charging_rates = df_charging_rates.loc[ev_charge.arrival : ev_charge.departure, ev_charge.station_id]
            for charging_rate in valid_charging_rates:
                ev_charge.set_current_charging_rate(charging_rate)
                list_ev_charges.append(ev_charge.to_dict())

        # new device, new month
        start += relativedelta(days=1)
        end += relativedelta(days=1)

    
    with open(file_path, "w") as fout:
        if not fout:
            fout.write("")
        json.dump(list_ev_charges, fout)
