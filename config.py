import jsonpickle

import models.config


with open('./config.json', 'r') as config_file:
    _config = jsonpickle.decode(config_file.read())

LogVerbose = _config['log_verbose']

_source = _dest = None

for sfdc_config in _config['salesforce_orgs']:
    n = sfdc_config['name']

    if n == 'Stream':
        _source = sfdc_config
    elif n == 'ASPartial':
        _dest = sfdc_config

Salesforce_Source = models.config.SalesforceSettings(_source)
Salesforce_Dest = models.config.SalesforceSettings(_dest)
