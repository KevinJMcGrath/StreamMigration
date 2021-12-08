import jsonpickle
import logging

import config
import sfdc
import sfdc.export as export

from models import payload as p

def migrate_stream_users(limit: int=200, only_client_users: bool=False):
    contact_list = query_source_contacts(limit, only_client_users)
    account_list = extract_account_list(contact_list)

    account_payload_list = build_account_payloads(account_list)
    contact_payload_list = build_contact_payloads(contact_list)

    account_insert_results = insert_account_payloads(account_payload_list)

    export.export_record_results(account_payload_list, account_insert_results, 'Account')

    account_lead_link_payload_list = build_ALL_payloads(account_list, account_insert_results)
    ALL_insert_results = insert_all_payloads(account_lead_link_payload_list)

    export.export_record_results(account_lead_link_payload_list, ALL_insert_results, 'Account_Lead_Link')

    contact_insert_results = insert_contact_payloads(contact_payload_list)

    export.export_record_results(contact_payload_list, contact_insert_results, 'Contact')

    logging.info('Operation complete.')

def query_source_contacts(limit: int, only_client_users: bool):
    logging.info(f'Loading source Contacts from {config.Salesforce_Source.name}...')

    soql = "SELECT Id, FirstName, LastName, Email, AccountId, People_Status__c, Stream_Client_Type_contact__c, " \
           "Stream_Role__c, Date_Became_Paid__c, First_login__c, Last_login__c, Stream_Active_User__c, Paid__c, " \
           "Stream_Portal_Expert_Id__c, " \
           "Account.Id, Account.Name, Account.Website, Account.Mosaic_Account_Id__c, Account.Stream_Client_Type__c, " \
           "Account.Portal_Account_ID__c, Account.Domain__c, Account.AlphaSense_Account__c, " \
           "Account.AlphaSense_Account_Type__c, Account.Stream_Date_Signed_Call_Agreement__c " \
           "FROM Contact " \
           "WHERE Stream_Active_User__c = true AND Account.AlphaSense_Account__c = false AND AccountId != NULL "

    if only_client_users:
        soql += " AND Paid__c = true"

    soql += " ORDER BY AccountId"

    if limit and limit > 0:
        soql += f" LIMIT {limit}"

    return sfdc.Source_Client.query(soql)

def extract_account_list(contact_list):
    logging.info(f'Parsing source Accounts from Contact list...')

    account_dict = {}

    for c in contact_list:
        a = c['Account']
        aid = a['Id']

        if aid not in account_dict:
            account_dict[aid] = a

    return account_dict.values()

def build_account_payloads(account_list):
    logging.info(f'Building Account payloads for Destination: {config.Salesforce_Dest.name}...')

    account_payload_list = []

    for a in account_list:
        account_payload_list.append(jsonpickle.decode(jsonpickle.encode(p.Account(a), unpicklable=False)))

    return account_payload_list

def build_contact_payloads(contact_list):
    logging.info(f'Building Contact payloads for Destination: {config.Salesforce_Dest.name}...')

    contact_payload_list = []

    for c in contact_list:
        contact_payload_list.append(jsonpickle.decode(jsonpickle.encode(p.Contact(c), unpicklable=False)))

    return contact_payload_list


def build_ALL_payloads(account_list, account_insert_result_list):
    logging.info(f'Building Account_Lead_Link payloads for Destination: {config.Salesforce_Dest.name}...')

    all_payload_list = []

    for i, (a_result, a) in enumerate(zip(account_insert_result_list, account_list)):
        domain_str = a['Domain__c']
        aid = a_result['id']
        payload = jsonpickle.decode(jsonpickle.encode(p.AccountLeadLink(aid, domain_str), unpicklable=False))

        all_payload_list.append(payload)

    return all_payload_list

def insert_account_payloads(account_payloads):
    logging.info(f'Inserting new Account records at {config.Salesforce_Dest.name}')
    # return sfdc.Dest_Client.inner_client.bulk.Account.create(account_payloads)
    return sfdc.Dest_Client.inner_client.bulk.Account.upsert(account_payloads, 'Stream_SFDC_Id__c')

def insert_contact_payloads(contact_payloads):
    logging.info(f'Inserting new Contact records at {config.Salesforce_Dest.name}')
    # return sfdc.Dest_Client.inner_client.bulk.Contact.create(contact_payloads)
    return sfdc.Dest_Client.inner_client.bulk.Contact.upsert(contact_payloads, 'Stream_SFDC_Id__c')

def insert_all_payloads(all_payloads):
    logging.info(f'Inserting new Account_Lead_Link records at {config.Salesforce_Dest.name}')
    return sfdc.Dest_Client.inner_client.bulk.Account_Lead_Link__c.insert(all_payloads)