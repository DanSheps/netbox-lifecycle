# NetBox Lifecycle Plugin

The Netbox Lifecycle plugin is a Hardware EOS/EOL, License and Support Contract tracking plugin for NetBox.

## Features

* Tracking EOL/EOS data
* Tracking License
* Tracking Support Contracts

# Requirements

* Netbox 4.1+
* Python 3.10+

## Compatibility Matrix

|        | Netbox 3.2.x   | NetBox 4.1.x   | 
|--------|----------------|----------------|
| 1.0.0+ | Compatible     | Not Compatible |
| 1.1.3+ | Not Compatible | Compatible     |

## Installation

To install, simply include this plugin in the plugins configuration section of netbox.

Example:
```python
    PLUGINS = [
        'netbox_lifecycle'
    ],
```

## Configuration

To use the sync_cisco_hw_eox_data command, you need to generate a client id and secret in the Cisco API console
for the support API and include them as part of the plugin configuration.

```python
    PLUGINS_CONFIG = [
        'netbox_lifecycle': {
            'cisco_support_api_client_id': '',     # Client ID for the Cisco Support API
            'cisco_support_api_client_secret': ''  # Client Secret for the Cisco Support API
    ],
```

## Usage

TBD

## Additional Notes

TBD

## Contribute

Contributions are always welcome!  Please open an issue first before contributing as the scope is going to be kept
intentionally narrow

