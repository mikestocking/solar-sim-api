import project
import api
import pytest
import pandas as pd

def test_get_site_params_go():
    assert project.get_site_params("9068")["tz"] == "US/Arizona"

def test_get_site_params_nogo():
    with pytest.raises(SystemExit):
        project.get_site_params("0000")

    with pytest.raises(SystemExit):
        project.get_site_params("abcd")

def test_create_model_go():
    site = project.get_site_params(9068)
    assert f"{type(project.create_model(site))}" == "<class 'pvlib.modelchain.ModelChain'>"

def test_create_model_nogo():
    with pytest.raises(TypeError):
        project.create_model("abc")

def test_get_results_go():
    site = project.get_site_params(9068)
    model = project.create_model(site)
    weather = pd.DataFrame([[1050, 1000, 500, 30, 5, 50]],
                       columns=['ghi', 'dni', 'dhi', 'temp_air', 'wind_speed', 'relative_humidity'],
                       index=[pd.Timestamp('20170401 1200', tz="US/Arizona")])
    results = project.get_results(model, weather)
    assert f"{type(results)}" == "<class 'pvlib.modelchain.ModelChainResult'>"

def test_get_results_nogo():
    site = project.get_site_params(9068)
    model = project.create_model(site)
    weather = pd.DataFrame([['abcd', 1000, 500, 30, 5, 50]],
                       columns=['ghi', 'dni', 'dhi', 'temp_air', 'wind_speed', 'relative_humidity'],
                       index=[pd.Timestamp('20170401 1200', tz="US/Arizona")])
    with pytest.raises(TypeError):
        project.get_results(model, weather)


