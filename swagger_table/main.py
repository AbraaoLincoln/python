import json
from swagger_to_table import schemas_to_table
from plan import save_p

with open('samples/swagger_schemas.json') as swagger_schemas:
    schemas = json.load(swagger_schemas)
    schemas_to_table(schemas)
    # save_p()

    
    