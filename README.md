# DSS Plugin - Palo Alto Cortex XSIAM

This Dataiku DSS plugin provides python connectors to load data from a Palo Alto Cortex XSIAM platform.

## Compatibility

* Dataiku DSS 12.0 or higher

## Plugin configuration
The following parameter can be configured globally :
* **FQDN** : The raw FQDN of the Palo Alto Cortex XSIAM tenant (without https:// or / at the end).
* **API key ID** : The API Cortex XSIAM API key ID, available in the **ID field** on the **Settings > Configurations > Integrations > API Keys** XSIAM configuration page. Check https://cortex-panw.stoplight.io/docs/cortex-xsiam-1 for detailed informations.
* **API key** : The Cortex XSIAM API key