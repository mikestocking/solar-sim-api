# Web API for Digital Twins of Solar Farm Portfolio
## Video Demo:  <https://youtu.be/jQ3aNI2RXr0>
## Description:

This project creates a web API for digital twins of a portfolio of solar (PV) farms. The digital twins, as currently implemented, are physics-based models that take exogenous weather data as inputs and returns a variety of parameters describing the expected state of the PV system (voltages, amperages, wattages of both DC and AC sides, steady-state module temperature, etc.). As this API is geared towards describing the instaneous state of the system, it does not output any energy measurements (though the underlying libraries and models are entirely capable).

This is useful to solar operations staff in condition monitoring, assessing site performance, detecting anomolies/problems, and performing diagnostics when issues arise.

All of the parameters that define the specifics of a particular solar farm are captured in JSON files in the "sites" directory. Each solar farm is to have one JSON file titled thusly: {site ID number}.JSON. These configuration details are then gathered and parsed when a request comes in specifying that site.  Included is one example site configuration (i.e. site "9068"), derived from [the fantastic PVlib documentation](https://pvlib-python.readthedocs.io/en/stable/gallery/system-models/plot_oedi_9068.html).

### **IMPORTANT NOTE:**
This is a proof of concept exercise, this is not production-ready code.


### Useage
This creates an API at an endpoint at {IP Address}:8000/sites that expects the following query parameters:
* "site_id": int, site ID number (with corresponding JSON file, per description in "Purpose" section above)
* "local_time": str, must be of pandas.Timestamp compatible format
* weather:
    * "ghi": int, global horizontal irradiance [W/m^2]
    * "dni": int, direct normal irradiance [W/m^2]
    * "dhi": int, diffuse horizontal irradiance [W/m^2]
    * "temp_air": float, temperature [ºC]
    * "wind_speed": float, wind speed [m/s]
    * "relative_humidity": float, relative humidity [%]

Example HTTP request:
>{IP}:8000/sites?site_id=9068&ghi=1050&dni=1000&dhi=100&temp_air=30&wind_speed=5&relative_humidity=50&local_time='20170401 1200'

### Output
The API response is a JSON of the following form:
* "ac":float, AC power [W]
* "dc": dict, simulated DC measurements of array
    * "i_sc": float, short circuit current [A]
    * "v_oc": float, open circuit voltage [V]
    * "i_mp": float, current at maximum power point [A]
    * "v_mp":float, voltage at maximum power point [V]
    * "p_mp": float, power at maximum power point [A]
    * "i_x": float, current at module V = 0.5 * V_oc [A]
    * "i_xx":float, current at module V = 0.5 * (V_oc + V_mp) [A]
* "cell_temperature": float, [ºC]
* "effective_irradiance": float, [W/m^2]

Example Response:
>{"ac":1778454.7393018373,"dc":{"i_sc":2049.703399157931,"v_oc":1130.5140114559974,"i_mp":1873.9387371460102,"v_mp":891.1811914918471,"p_mp":1828726.1197545743,"i_x":2007.7941185688383,"i_xx":1287.1605692429468},"cell_temperature":45.43445025638568,"effective_irradiance":896.2688574383329}


## Future Work:
- [ ] Incorporate effects of module degradation
- [ ] More robust input validation
- [ ] Additional testing
- [ ] Alternative calculations on the basis of reasonable assumptions in the case of missing inputs
- [ ] Future energy (forecasting) endpoint
- [ ] Past energy endpoint
- [ ] Performance optimization
- [ ] Security/authentication
- [ ] Allowance for plane-of-array irradiance measurements
- [ ] Direct analysis of digital twin vs. realized performance via additional (optional) inputs
- [ ] Allowance for other types of models, e.g. ML models
- [ ] Allowance for other technology types, e.g. wind turbines, energy storage systems
- [ ] Forecasting support for time intervals
- [ ] Confidence intervals for outputs


## **THANKS**
Props to the devs of the dependencies where 99.999999+% of the work is being done.
