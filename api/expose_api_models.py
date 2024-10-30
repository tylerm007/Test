from safrs import SAFRSAPI
import safrs
import importlib
import pathlib
import logging as logging

# use absolute path import for easier multi-{app,model,db} support
database = __import__('database')

app_logger = logging.getLogger(__name__)

app_logger.debug("\napi/expose_api_models.py - endpoint for each table")


def expose_models(api, method_decorators = []): 
    """
        Declare API - on existing SAFRSAPI to expose each model - API automation 
        - Including get (filtering, pagination, related data access) 
        - And post/patch/update (including logic enforcement) 

        Invoked at server startup (api_logic_server_run) 

        You typically do not customize this file 
        - See https://apilogicserver.github.io/Docs/Tutorial/#customize-and-debug 
    """
    api.expose_object(database.models.Barn, method_decorators= method_decorators)
    api.expose_object(database.models.Farm, method_decorators= method_decorators)
    api.expose_object(database.models.Cattle, method_decorators= method_decorators)
    api.expose_object(database.models.CattlePen, method_decorators= method_decorators)
    api.expose_object(database.models.Pen, method_decorators= method_decorators)
    api.expose_object(database.models.Employee, method_decorators= method_decorators)
    api.expose_object(database.models.FeedingSchedule, method_decorators= method_decorators)
    api.expose_object(database.models.HealthCheck, method_decorators= method_decorators)
    api.expose_object(database.models.Supplier, method_decorators= method_decorators)
    api.expose_object(database.models.SupplyItem, method_decorators= method_decorators)
    api.expose_object(database.models.SupplyOrder, method_decorators= method_decorators)
    api.expose_object(database.models.VetVisit, method_decorators= method_decorators)
    api.expose_object(database.models.Veterinary, method_decorators= method_decorators)
    return api
