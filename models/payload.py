import jsonpickle

import utility as u

class Payload:
    def __init__(self):
        pass

    def toJSON(self):
        return jsonpickle.encode(value=self, unpicklable=False)

class Account(Payload):
    def __init__(self, account_data):
        super().__init__()

        self.Name = account_data['Name']
        self.Website = account_data['Website']
        self.Stream_SFDC_Id__c = account_data['Id']
        self.Customer_Status__c = map_customer_status(account_data['Stream_Client_Type__c'])
        self.Stream_Account_Id__c = account_data['Portal_Account_ID__c']
        self.Type = map_account_type(account_data['AlphaSense_Account_Type__c'])
        self.Initial_Contract_Date__c = account_data['Stream_Date_Signed_Call_Agreement__c']

class AccountLeadLink(Payload):
    def __init__(self, account_id: str, domain: str):
        super().__init__()

        self.Account__c = account_id
        self.Domain__c = domain


class Contact(Payload):
    def __init__(self, contact_data, account_id: str):
        super().__init__()

        self.Skipped = account_id == "-1"

        # Standard Contact Data
        self.AccountId = account_id
        self.FirstName = contact_data['FirstName']
        self.LastName = contact_data['LastName']
        self.Email = contact_data['Email']

        # Analytics
        self.Effective_Date_paying_user__c = contact_data['Date_Became_Paid__c']
        self.First_Login_Stream__c = contact_data['First_login__c']
        self.Last_Login_Stream__c = contact_data['Last_login__c']

        # Legacy Stream Data
        self.Stream_SFDC_Id__c = contact_data['Id']
        self.Stream_User_Id__c = contact_data['Stream_Portal_Expert_Id__c']
        self.Stream_User_Role__c = contact_data['Stream_Role__c']

        # AS Account Setup
        self.Username__c = contact_data['Email']
        self.Password__c = 'Monday01!!21'
        self.Confirm_Password__c = self.Password__c
        self.Status_of_User__c = 'Active'
        self.User_Status__c = 'Paying User (Original ID)'

        # Permissions
        self.Annotate__c = False
        self.Dashboard_v2_AS__c = False
        self.Default_One_Year_Timeframe_Filter_AS__c = False
        self.Expert_Calls__c = True  # Controls the Stream content set
        self.GammaPreview_AS__c = True
        self.Search_Summary_AS__c = False
        self.Stream_App_Access_AS__c = True  # Controls actual access to the Stream app in AS
        self.Support_Chat__c = False

        # Permissions - Disabled
        self.Sharing_Enabled__c = 'Off'
        self.Analyst_Search_Filter_AS__c = False
        self.Similar_Tables_Export__c = False
        self.Custom_Groups__c = 'Off'
        self.Email_Alerts__c = False
        self.Region_s_Subscribed__c = 'None (Empty Container)' # Primary Research (PRM)_AS
        self.Broker_Research_Module__c = 'None' # Broker Research (BRM) (TR) Region_AS
        self.Transcripts_Type__c = 'N/A'

def map_customer_status(status):
    if status == 'Paid':
        return 'Client'

    return status

def map_account_type(account_type):
    if account_type == 'Financial Services':
        return 'Investment Manager (long only)'

    return account_type