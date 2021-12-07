class SalesforceSettings:
    def __init__(self, sfdc_json):
        self.username = sfdc_json['username']
        self.password = sfdc_json['password']
        self.security_token = sfdc_json['security_token']
        self.domain = sfdc_json['domain']