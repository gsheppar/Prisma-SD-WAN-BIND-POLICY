# Prisma SD-WAN Bind Policy
This utility is used to bind a list of sites to a path policy



### Requirements
* Active Prisma SDWAN Account
* Python >=3.6
* Python modules:
    * Prisma SASE (prisma_sase) Python SDK >= 5.5.3b1 - <https://github.com/PaloAltoNetworks/prisma-sase-sdk-python>

### License
MIT

### Installation:
 - **Github:** Download files to a local directory, manually run `copylanconfig.py`. 

### Authentication:
 - Create a Service Account via the Identity & Access menu on Strata Cloud Manager
 - Save Service account details in the prismasase_settings.py file

### Examples of usage:

```
./bind_path_policy.py -S Site_List.csv -N "Prisma SASE (Simple)" 
```

#### Version
| Version | Build | Changes |
| ------- | ----- | ------- |
| **1.0.0** | **b1** | Initial Release. |


#### For more info
 * Get help and additional Prisma SDWAN Documentation at <https://docs.paloaltonetworks.com/prisma/prisma-sd-wan.html>
