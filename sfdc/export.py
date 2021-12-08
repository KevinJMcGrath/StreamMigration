import csv
import inspect
import logging

import config

from datetime import datetime
from pathlib import Path

def export_record_results(payload_list, result_list, object_name: str):
    first_payload = payload_list[0]
    prop_definitions = inspect.getmembers(first_payload, lambda prop:not inspect.isroutine(prop))
    prop_names = [prop[0] for prop in prop_definitions if not (prop[0].startswith('__') and prop[0].endswith('__'))]

    csv_columns = prop_names
    csv_columns.append('dest_Id')
    csv_columns.append('errors')

    timestamp = datetime.now().timestamp()

    csv_file_path = Path(f'./export/{config.Salesforce_Dest.name}_{object_name}_{timestamp}.csv')

    with open(csv_file_path, 'w') as export_file:
        writer = csv.DictWriter(export_file, fieldnames=csv_columns, extrasaction='ignore', lineterminator='\n')

        writer.writeheader()

        for i, (payload, result) in enumerate(zip(payload_list, result_list)):
            payload['dest_Id'] = result['id']
            payload['errors'] = '|'.join(result['errors'])

            writer.writerow(payload)


    logging.info('Export complete')