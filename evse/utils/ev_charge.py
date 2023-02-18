import json

class EvCharge():
    """Class to model a single istance of charge of an Electrical Vehicle (ev).

    Args:
        arrival (int): Arrival time of the ev. [periods]
        departure (int): Departure time of the ev. [periods]
        requested_energy (float): Energy requested by the ev on arrival. [kWh]
        station_id (str): Identifier of the station used by this ev.
    """

    def __init__(
        self,
        id,
        arrival,
        departure,
        requested_energy,
        station_id,
        discharge,
        estimated_departure=None,
    ):
        # User Defined Parameters
        self._id = id
        self._arrival = arrival
        self._departure = departure
        self._station_id = station_id
        self._discharge = discharge

        # Estimate of session parameters
        self._requested_energy = requested_energy
        self._estimated_departure = (
            estimated_departure if estimated_departure is not None else departure
        )

        # Internal State
        self._energy_delivered = 0
        self._current_charging_rate = 0

    def __str__(self) -> str:
        return "Arrival: " + str(self.arrival) + "\n" +\
        "Departure: " + str(self.departure) + "\n" +\
        "Requested Energy: " + str(self.requested_energy) + "\n" +\
        "Station ID: " + str(self.station_id) + "\n" +\
        "Estimated Departure: " + str(self.estimated_departure) + "\n" +\
        "Energy Delivered: " + str(self.energy_delivered) + "\n" +\
        "Charging Rate: " + str(self.current_charging_rate) + "\n"

    @property
    def id(self):
        """ Return the id of the EV."""
        return self._id

    @property
    def arrival(self):
        """ Return the arrival time of the EV."""
        return self._arrival

    @arrival.setter
    def arrival(self, value):
        """ Set the arrival time of the EV. (int) """
        self._arrival = value

    @property
    def departure(self):
        """ Return the departure time of the EV. (int) """
        return self._departure

    @departure.setter
    def departure(self, value):
        """ Set the departure time of the EV. (int) """
        self._departure = value

    @property
    def estimated_departure(self):
        """ Return the estimated departure time of the EV."""
        return self._estimated_departure

    @estimated_departure.setter
    def estimated_departure(self, value):
        """ Set the estimated departure time of the EV. (int) """
        self._estimated_departure = value

    @property
    def requested_energy(self):
        """ Return the energy request of the EV for this session. (float) [acnsim units]. """
        return self._requested_energy

    @property
    def station_id(self):
        """ Return the unique identifier for the EVSE used for this charging session. """
        return self._station_id

    @property
    def discharge(self):
        """ Return a factor od discharge in order to have a better representation of precent charging. """
        return self._discharge

    @property
    def energy_delivered(self):
        """ Return the total energy delivered so far in this charging session. (float) """
        return self._energy_delivered

    @property
    def current_charging_rate(self):
        """ Return the current charging rate of the EV. (float) """
        return self._current_charging_rate
    
    def set_current_charging_rate(self, value):
        """ Set the current charging rate of the EV. (float) """
        self._current_charging_rate = value
        self._update_energy_delivered()

    @property
    def remaining_demand(self):
        """ Return the remaining energy demand of this session. (float)

        Defined as the difference between the requested energy of the session and the energy delivered so far.
        """
        return self.requested_energy - self.energy_delivered

    @property
    def fully_charged(self):
        """ Return True if the EV's demand has been fully met. (bool)"""
        return not (self.remaining_demand > 1e-3)

    @property
    def percent_complete(self):
        """ Return the percent of demand which still needs to be fulfilled. (float)

        Defined as the ratio of remaining demand and requested energy. """
        return 100 - self.remaining_demand / self.requested_energy

    @property
    def cost(self):
        """ Return the cost of recharge so far for this charging session. (float)"""
        return 0.60 * self.energy_delivered

    def _update_energy_delivered(self):
        self._energy_delivered += (self.current_charging_rate * 220) / 1000 * (1 / 60)
        
    def to_json(self) -> str:
        _d = {
            "id": self.id,
            "arrival": self.arrival,
            "departure": self.departure,
            "current_charge": self.current_charging_rate,
            "energy_delivered": self.energy_delivered,
            "percent_complete": self.percent_complete,
            "cost": self.cost
        }
        return json.dumps(_d)

    def to_dict(self):
        return {
            "id": self.id,
            "arrival": self.arrival,
            "departure": self.departure,
            "current_charge": self.current_charging_rate,
            "energy_delivered": self.energy_delivered,
            "percent_complete": self.percent_complete,
            "cost": self.cost
        }