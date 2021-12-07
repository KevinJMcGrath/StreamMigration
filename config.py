import jsonpickle

import models.config


with open('./config.json', 'r') as config_file:
    _config = jsonpickle.decode(config_file.read())

LogVerbose = _config['log_verbose']

Salesforce_Source = models.config.SalesforceSettings(_config['salesforce_source'])
Salesforce_Dest = models.config.SalesforceSettings(_config['salesforce_dest'])
