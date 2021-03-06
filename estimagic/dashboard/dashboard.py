"""
Functions that setup and update the dashboard.

These are the main functions of the dashboard.

The functions defined here are not executed directly.
Instead a BokehServer is setup and run to execute the main function run_dashboard.
The functions to setup and run the BokehServer can be found in server_functions.

The functions to build and update each tab can be found in the respective module.

"""
from functools import partial
from threading import Thread
from time import sleep

from bokeh.models.widgets import Tabs

from estimagic.dashboard.convergence_tab import setup_convergence_tab
from estimagic.dashboard.convergence_tab import update_convergence_data


def run_dashboard(doc, queue, start_signal, db_options):
    """Configure the dashboard and update constantly as new parameters arrive.

    This is the main function that is supplied to the bokeh FunctionHandler.
    Note that the first argument must be doc for the FunctionHandler
    to create the bokeh Applications correctly.

    Args:
        doc (bokeh Document):
            document instance where the Dashboard will be stored.
            Note this must stay the first argument for the bokeh FunctionHandler
            to work properly.

        queue (Queue):
            queue to which originally the parameters DataFrame is supplied and to which
            the updated parameter Series will be supplied later.

        start_signal (Queue):
            empty queue. The minimization starts once it stops being empty.

        db_options (dict):
            dictionary with options. Supported so far:
                rollover (int):
                    How many data points to store, default None.

    """
    rollover = db_options["rollover"]
    param_df, initial_fitness, still_running = queue.get()

    doc, data = _configure_dashboard(
        doc=doc, param_df=param_df, initial_fitness=initial_fitness
    )

    # this thread is necessary to not lock the server
    callbacks = partial(
        _update_dashboard, doc=doc, dashboard_data=data, queue=queue, rollover=rollover
    )
    update_data_thread = Thread(target=callbacks)
    update_data_thread.start()
    start_signal.put(True)


def _configure_dashboard(doc, param_df, initial_fitness):
    """
    Setup the basic dashboard.

    Args:
        doc (bokeh Document):
            bokeh document to be configured

        param_df (pandas DataFrame):
            See :ref:`params_df`.

        initial_fitness (float):
            criterion function evaluated at the initial parameters
    """
    conv_data, tab1 = setup_convergence_tab(param_df, initial_fitness)

    tabs = Tabs(tabs=[tab1])
    doc.add_root(tabs)

    return doc, [conv_data]


def _update_dashboard(doc, dashboard_data, queue, rollover):
    """
    Update the dashboard after each call of the criterion function.

    Args:
        doc (bokeh Document):
            Document of the dashboard.

        dashboard_data (list):
            List of datasets used for the dashboard.

        queue (Queue):
            queue to which the updated parameter Series are supplied.

    """
    conv_data, = dashboard_data
    still_running = True
    while still_running:
        if queue.qsize() > 0:
            new_params, new_fitness, still_running = queue.get()

            doc.add_next_tick_callback(
                partial(
                    update_convergence_data,
                    data=conv_data,
                    new_params=new_params,
                    new_fitness=new_fitness,
                    rollover=rollover,
                )
            )
        else:
            sleep(0.001)
