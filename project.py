import sys
import json
import pvlib
import pandas as pd

def main(site_id,weather_params):
    site = get_site_params(site_id)
    model = create_model(site)
    weather = pd.DataFrame([[weather_params['ghi'], weather_params['dni'], weather_params['dhi'], weather_params['temp_air'], weather_params['wind_speed'], weather_params['relative_humidity']]],
                       columns=['ghi', 'dni', 'dhi', 'temp_air', 'wind_speed', 'relative_humidity'],
                       index=[pd.Timestamp(weather_params['local_time'], tz=site['tz'])])
    results = get_results(model, weather)
    kpis = {
        "ac": results.ac.iloc[0],
        "dc": {
            "i_sc": results.dc.i_sc.iloc[0],
            "v_oc": results.dc.v_oc.iloc[0],
            "i_mp": results.dc.i_mp.iloc[0],
            "v_mp": results.dc.v_mp.iloc[0],
            "p_mp": results.dc.p_mp.iloc[0],
            "i_x": results.dc.i_x.iloc[0],
            "i_xx": results.dc.i_xx.iloc[0]
        },
        "cell_temperature": results.cell_temperature.iloc[0],
        "effective_irradiance": results.effective_irradiance.iloc[0]
    }
    return kpis

def get_site_params(site_number):
    try:
        site_file = open(f"/workspaces/6899858/project/sites/{site_number}.json")
    except:
        sys.exit("Invalid site number")
    return json.load(site_file)

def create_model(site):
    location = pvlib.location.Location(site['latitude'], site['longitude'])
    mount = pvlib.pvsystem.SingleAxisTrackerMount(
        gcr=site['gcr'],
        backtrack=site['backtrack'],
        max_angle=site['max_angle'],
        axis_azimuth=site['axis_azimuth']
    )
    cec_module_db = pvlib.pvsystem.retrieve_sam('cecmod')
    array = pvlib.pvsystem.Array(
        mount,
        module_parameters=cec_module_db[site['module_model']],
        #module_parameters['Technology'] = site['module_technology'],
        modules_per_string=site['modules_per_string'],
        temperature_model_parameters=site['temperature_model_parameters'],
        strings=site['strings_per_inverter']
    )
    cec_inverter_db = pvlib.pvsystem.retrieve_sam('cecinverter')
    system = pvlib.pvsystem.PVSystem(
        array,
        inverter_parameters=cec_inverter_db[site['inverter_model']],
        losses_parameters=site['losses_parameters']
    )
    model = pvlib.modelchain.ModelChain(
        system,
        location,
        spectral_model=site['spectral_model'],
        aoi_model='physical',
        losses_model='pvwatts'
    )
    return model
    ...

def get_results(model,weather):
    weather["precipitable_water"] = pvlib.atmosphere.gueymard94_pw(weather["temp_air"], weather["relative_humidity"])
    model.run_model(weather)
    return model.results

if __name__ == "__main__":
    main()
