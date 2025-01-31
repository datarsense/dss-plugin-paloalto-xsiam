import gzip
import json
import logging
import requests
import time
from io import BytesIO

# Raise an error if API authentication token is null or contains only blank chars
def raise_if_apitoken_missing(tokenId, token):
    if tokenId is None or tokenId.strip() == "":
      raise Exception('Error : API key ID is missing, please configure it in plugin parameters')
    
    if token is None or token.strip() == "":
      raise Exception('Error : API key is missing, please configure it in plugin parameters')

# Raise first / char of a string
def remove_first_slash(s):
    if (s[0] == "/"):
        return s[1:]
    else: 
        return(s)

# https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/xql-apis/start-xql-query.html
def cortex_xsiam_api_post(fqdn, api_endpoint, api_key_id, api_key, query_params=None, body=None):

  url = "https://api-%s/public_api/v1/%s" % (fqdn, remove_first_slash(api_endpoint))
  headers = {
     'Content-Type': 'application/json',
     'x-xdr-auth-id': api_key_id,
     'Authorization': api_key
  }

  r = requests.post(url, params=query_params, headers=headers, json=body)

  if r.status_code == 200 and 'application/json' in r.headers.get('Content-Type', '') and len(r.content):
     return r.json()["reply"]
  
  elif r.status_code == 429 or r.status_code == 504 or r.status_code == 599:
      time.sleep(15)
  else:
      raise Exception('Error when calling palo Alto Cortex XSIAM API. Error code:' + str(r.status_code) + ". Error message: " + r.text)

  
# https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/xql-apis/get-xql-query-results.html
def stream_xql_query_results(fqdn, api_key_id, api_key, queryid):
  url = "https://api-%s/public_api/v1/xql/get_query_results" %(fqdn)
  headers = {
     'Content-Type': 'application/json',
     'x-xdr-auth-id': api_key_id,
     'Authorization': api_key
  }

  body = {
      "request_data": {
        "query_id": queryid,
        "pending_flag": False,
        "format": "json"
      }
    }

  r = requests.post(url, headers=headers, json=body)

  if r.status_code == 200 and 'application/json' in r.headers.get('Content-Type', '') and len(r.content):
    reply_data = r.json()["reply"]
     
    if 'data' in reply_data["results"].keys():
      for item in reply_data["results"]["data"]:
        yield item
    
    elif 'stream_id' in reply_data["results"].keys():
       streamId = reply_data["results"]["stream_id"]
       yield from get_large_xql_query_results(fqdn, api_key_id, api_key, streamId)
  
  elif r.status_code == 429 or r.status_code == 504 or r.status_code == 599:
      time.sleep(15)
  else:
      raise Exception('Error when calling palo Alto Cortex XSIAM API. Error code:' + str(r.status_code) + ". Error message: " + r.text)


# https://docs.paloaltonetworks.com/cortex/cortex-xdr/cortex-xdr-api/cortex-xdr-apis/xql-apis/get-xql-query-exported-data.html
def get_large_xql_query_results(fqdn, api_key_id, api_key, streamid):
  url = "https://api-%s/public_api/v1/xql/get_query_results_stream" %(fqdn)
  headers = {
     'Content-Type': 'application/json',
     'Accept-Encoding': 'gzip',
     'x-xdr-auth-id': api_key_id,
     'Authorization': api_key
  }

  body = {
      "request_data": {
        "stream_id": streamid,
        "is_gzip_compressed": True
      }
    }

  r = requests.post(url, headers=headers, json=body)

  buffer = BytesIO(r.content)
  data = gzip.GzipFile(fileobj=buffer).read().decode("utf-8")
  
  for line in data.splitlines(): 
     if line.strip() != "":
        yield json.loads(line) 
  