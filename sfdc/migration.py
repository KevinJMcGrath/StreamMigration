import sfdc

from models import payload as p

def migrate_stream_users(limit: int=200):
    contact_list = query_source_contacts(limit)
    account_list = extract_account_list(contact_list)

    account_payload_list = build_account_payloads(account_list)
    contact_payload_list = build_contact_payloads(contact_list)

    account_insert_results = insert_account_payloads(account_payload_list)

    account_lead_link_payload_list = build_ALL_payloads(account_list, account_insert_results)



def query_source_contacts(limit: int):
    soql = "SELECT Id, FirstName, LastName, Email, People_Status__c, Stream_Client_Type_contact__c, Stream_Role__c, " \
            "Date_Became_Paid__c, First_login__c, Last_login__c, Stream_Active_User__c, Paid__c, " \
            "Stream_Portal_Expert_Id__c, " \
            "AccountId, Account.Name, Account.Website, Account.Mosaic_Account_Id__c, Account.Stream_Client_Type__c, " \
            "Account.Portal_Account_ID__c, Account.Domain__c, Account.AlphaSense_Account__c, " \
            "Account.AlphaSense_Account_Type__c, Account.Stream_Date_Signed_Call_Agreement__c " \
            "FROM Contact " \
            "WHERE Stream_Active_User__c = true AND Account.AlphaSense_Account__c = false " \
            "ORDER BY AccountId"

    if limit and limit > 0:
        soql += f" LIMIT {limit}"

    return sfdc.Source_Client.query(soql)

def extract_account_list(contact_list):
    account_dict = {}

    for c in contact_list:
        a = c['Account']
        aid = a['Id']

        if aid not in account_dict:
            account_dict[aid] = a

    return account_dict.values()

def build_account_payloads(account_list):
    account_payload_list = []

    for a in account_list:
        account_payload_list.append(p.Account(a))

    return account_payload_list

def build_contact_payloads(contact_list):
    contact_payload_list = []

    for c in contact_list:
        contact_payload_list.append(p.Contact(c))

    return contact_payload_list


def build_ALL_payloads(account_list, account_insert_result_list):
    all_payload_list = []

    for i, (a_result, a) in enumerate(zip(account_insert_result_list, account_list)):
        domain_str = a['Domain__c']
        aid = a_result['id']
        payload = p.AccountLeadLink(aid, domain_str)

        all_payload_list.append(payload)

    return all_payload_list

def insert_account_payloads(account_payloads):
    return sfdc.Dest_Client.inner_client.bulk.Account.create(account_payloads)

def insert_contact_payloads(contact_payloads):
    return sfdc.Dest_Client.inner_client.bulk.Contact.create(contact_payloads)

def insert_all_payloads(all_payloads):
    return sfdc.Dest_Client.inner_client.bulk.Account_Lead_Link__c.create(all_payloads)