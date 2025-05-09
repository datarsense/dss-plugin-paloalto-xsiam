# This file is the actual code for the custom Python dataset paloalto-xsiam_xql-query

# import the base class for the custom dataset
import dateutil
import requests
from datetime import datetime
from six.moves import xrange
from dataiku.connector import Connector
from helpers import raise_if_apitoken_missing, cortex_xsiam_api_post, stream_xql_query_results

class XqlQuery(Connector):

  def __init__(self, config, plugin_config):
    Connector.__init__(self, config, plugin_config)  # pass the parameters to the base class
    if (self.config.get("cortexXsiamTenantFqdn") is not None) and (self.config.get("cortexXsiamTenantFqdn")):
      self.fqdn = self.config.get("cortexXsiamTenantFqdn")
    else:
      self.fqdn = self.plugin_config.get("cortexXsiamTenantFqdn")
    
    if (self.config.get("cortexXsiamApiKeyId") is not None) and (self.config.get("cortexXsiamApiKeyId")):
      self.authTokenId = self.config.get("cortexXsiamApiKeyId")
    else:
      self.authTokenId = self.plugin_config.get("cortexXsiamApiKeyId")

    if (self.config.get("cortexXsiamApiKey") is not None) and (self.config.get("cortexXsiamApiKey")):
      self.authToken = self.config.get("cortexXsiamApiKey")
    else:
      self.authToken = self.plugin_config.get("cortexXsiamApiKey")

    self.startDateTimeStr = config.get("startDateTime")
    self.endDateTimeStr = config.get("endDateTime")
    self.xqlQuery = config.get("xqlQuery")

  def get_read_schema(self):
    return None
  

  def generate_rows(self, dataset_schema=None, dataset_partitioning=None, partition_id=None, records_limit = -1):
    # Raise an error if API auth token is missing
    raise_if_apitoken_missing(self.authTokenId, self.authToken)
    
    # Integer in timestamp epoch milliseconds required
    startUnixTimestamp = round(datetime.fromisoformat(self.startDateTimeStr).timestamp()*1000)
    endUnixTimestamp = round(datetime.fromisoformat(self.endDateTimeStr).timestamp()*1000)

    xqlQueryString = self.xqlQuery

    if records_limit > 0:
      xqlQueryString += " | limit %s" % records_limit

    query = {
      "request_data": {
        "query": xqlQueryString,
        "timeframe": {
          "from": startUnixTimestamp,
          "to": endUnixTimestamp
        }
      }
    }

    queryId = cortex_xsiam_api_post(self.fqdn, "/xql/start_xql_query",self.authTokenId, self.authToken, body=query)
    yield from stream_xql_query_results(self.fqdn, self.authTokenId, self.authToken, queryId)


  def get_writer(self, dataset_schema=None, dataset_partitioning=None, partition_id=None):
    raise NotImplementedError


  def get_partitioning(self):
    raise NotImplementedError


  def list_partitions(self, partitioning):
    return []


  def partition_exists(self, partitioning, partition_id):
    raise NotImplementedError


  def get_records_count(self, partitioning=None, partition_id=None):
    raise NotImplementedError

