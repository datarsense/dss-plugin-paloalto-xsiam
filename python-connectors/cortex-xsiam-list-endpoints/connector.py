# This file is the actual code for the custom Python dataset paloalto-xsiam_endpoints-list-get

# import the base class for the custom dataset
import requests
from six.moves import xrange
from dataiku.connector import Connector
from helpers import raise_if_apitoken_missing, cortex_xsiam_api_post

class GetEndpointList(Connector):

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

  def get_read_schema(self):
    return {
      "columns" : [
        { "name" : "agent_id", "type" : "string" },
        { "name" : "agent_status", "type" : "string" },
        { "name" : "operational_status", "type" : "string" },
        { "name" : "host_name", "type" : "string" },
        { "name" : "agent_type", "type" : "string" },
        { "name" : "ip", "type" : "array" },
        { "name" : "last_seen", "type" : "int" },
        { "name" : "tags", "type" : "object" },
        { "name" : "users", "type" : "array" }
      ]
    }

  def generate_rows(self, dataset_schema=None, dataset_partitioning=None, partition_id=None, records_limit = -1):
    # Raise an error if API auth token is missing
    raise_if_apitoken_missing(self.authTokenId, self.authToken)
    result = cortex_xsiam_api_post(self.fqdn, "/endpoints/get_endpoints",self.authTokenId, self.authToken)
    
    for item in result:
      yield item

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

