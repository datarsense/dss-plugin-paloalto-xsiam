import requests
from helpers import cortex_xsiam_api_post

def process(row):
    fqdn = plugin_params.get("cortexXsiamTenantFqdn")
    authTokenId = plugin_params.get("cortexXsiamApiKeyId")
    authToken = plugin_params.get("cortexXsiamApiKey")
    
    endpoint_id_column = params.get('endpoint_id_column')
    
    query = {
      "request_data": {
        "endpoint_id": row[endpoint_id_column]
      }
    }
    
    result = cortex_xsiam_api_post(fqdn, "/endpoints/get_policy",authTokenId, authToken, body=query)
    
    return result["policy_name"]
