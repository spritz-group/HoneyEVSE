from itertools import count
import json
import os
from datetime import datetime
from pathlib import Path
from random import randrange
import numpy as np

import pytz
from acnportal import acnsim, algorithms
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

# from utils.ev_charge import EvCharge
from utils.ev_charge import EvCharge

load_dotenv()

API_KEY = os.getenv("API_KEY")

TIMEZONE = pytz.timezone("America/Los_Angeles")

PERIOD = 1 # minutes

VOLTAGE = 220  # volts

DEFAULT_BATTERY_POWER = 32 * VOLTAGE / 1000  # kW

SITE = "caltech"

SCH = algorithms.UncontrolledCharging()

COUNTER = count()

def simulate(nsimulations=1, file_path=Path()):
    """
    Given a number of device to simulate, the function simaltes their recharge in the acn portal.
    It return a dataframe containing the siumaltions of recharge.
    """
    start = datetime(2020, 3, 1)
    end = datetime(2020, 3, 2)

    list_ev_charges = []
    cn = acnsim.sites.caltech_acn(basic_evse=True, voltage=VOLTAGE)

    for _ in range(nsimulations):

        events = acnsim.acndata_events.generate_events(
            API_KEY, SITE, TIMEZONE.localize(start), TIMEZONE.localize(end), PERIOD, VOLTAGE, DEFAULT_BATTERY_POWER
        )

        sim = acnsim.Simulator(cn, SCH, events, TIMEZONE.localize(start), period=PERIOD)
        sim.run()

        df_charging_rates = sim.charging_rates_as_df()
        dict_ev = sim.ev_history

        for ev in dict_ev.values():
            # Generate a special id for the ev
            id = "ev" + str(next(COUNTER))
            # Create a mask for the valid charges in the df
            mask_valid_charges = df_charging_rates[ev.station_id] != 0
            # List the indexes for acessing the first and last value
            list_indexes = df_charging_rates.index[mask_valid_charges].tolist()
            # Create the fist and last element (took one above and one beyond for have a better range)
            start_charge, end_charge = list_indexes[0] - 1, list_indexes[-1] + 1
            # Generate a random value for the discharge percentage
            discharge_value = randrange(40, 80)


            print(f'EV requested energy: {ev.requested_energy}')

            ev._battery._init_charge = np.float(np.random.uniform(0, 1)) 

            ev_charge = EvCharge(id, start_charge, end_charge, ev.requested_energy, ev.station_id, discharge_value)
            # Iterate to each charges rate for each ev
            for charging_rate in df_charging_rates.loc[start_charge : end_charge, ev.station_id]:
                # Set the current charge rate and save the internal parameter
                ev_charge.set_current_charging_rate(charging_rate)
                list_ev_charges.append(ev_charge.to_dict())


            # ######### TESTING THE DEFAULT VALUES IN THE SIMULATOR ############
            # print(f'Original battery initial charge value: {ev._battery._init_charge}')
            # ev._battery._init_charge = np.float(np.random.uniform(0, 1)) 
            # print(f'Modified values: {ev._battery._init_charge}')
            # break

        # each simulation requires a new day
        start += relativedelta(days=1)
        end += relativedelta(days=1)

    # Save the snapshots of charges in a json file    
    with file_path.open("w") as fp: 
        json.dump(list_ev_charges, fp)

# simulate(1, Path('test.json'))