import sfdc.simple_client as sc

Source_Client = sc.init_client_from_config('source')
Dest_Client = sc.init_client_from_config('dest')