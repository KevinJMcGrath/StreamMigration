import simple_salesforce

import config

class SFDCClient:
    def __init__(self, simple_salesforce_client: simple_salesforce.Salesforce):
        self.inner_client: simple_salesforce.Salesforce = simple_salesforce_client

    def query(self, soql: str):
        return self.inner_client.query_all(soql)['records']


def init_client_from_config(client_type: str='source'):
    if client_type == 'source':
        u = config.Salesforce_Source.username
        p = config.Salesforce_Source.password
        s = config.Salesforce_Source.security_token
        d = config.Salesforce_Source.domain
    elif client_type == 'dest':
        u = config.Salesforce_Dest.username
        p = config.Salesforce_Dest.password
        s = config.Salesforce_Dest.security_token
        d = config.Salesforce_Dest.domain
    else:
        return

    ss = simple_salesforce.Salesforce(username=u, password=p, security_token=s, domain=d)

    return SFDCClient(ss)

