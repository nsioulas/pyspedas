import logging
from viresclient import SwarmRequest
from pyspedas import time_datetime
from pytplot import store_data


def load(trange=None,
         collection=None,
         measurements=None,
         models=None,
         sampling_step=None,
         auxiliaries=None,
         residuals=False):
    """

    """
    if trange is None:
        logging.error('No time range specified')
        return

    tr = time_datetime(trange)

    if not isinstance(measurements, list):
        measurements = [measurements]

    if not isinstance(auxiliaries, list):
        auxiliaries = [auxiliaries]

    if models is not None:
        if not isinstance(models, list):
            models = [models]

    request = SwarmRequest()
    if isinstance(collection, list):
        request.set_collection(*collection)
    else:
        request.set_collection(collection)

    request.set_products(measurements=measurements, auxiliaries=auxiliaries, models=models, sampling_step=sampling_step, residuals=residuals)
    data = request.get_between(start_time=tr[0], end_time=tr[1])
    return xarray_to_tplot(data.as_xarray())


def xarray_to_tplot(xr):
    out = []
    for key in xr.keys():
        times = xr[key].coords['Timestamp'].to_numpy()
        saved = store_data(key, data={'x': times, 'y': xr[key].data})
        if saved:
            out.append(key)
        else:
            logging.warning('Problem saving: ' + key)
    return out
