# NetBox Lifecycle Plugin

The Netbox Lifecycle plugin is a Hardware EOS/EOL, License and Support Contract tracking plugin for NetBox.

## Features

* Tracking EOL/EOS data for DeviceTypes and ModuleTypes
* Tracking Licenses (assignable to Devices and Virtual Machines)
* Tracking Support Contracts (assignable to Devices, Modules, and Virtual Machines)

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

The plugin can be configured via `PLUGINS_CONFIG` in your NetBox configuration file:

```python
PLUGINS_CONFIG = {
    'netbox_lifecycle': {
        # UI card positions
        'lifecycle_card_position': 'right_page',
        'contract_card_position': 'right_page',
        'license_card_position': 'right_page',

        # Cisco EoX API sync (optional — can also be configured via the Web UI)
        'cisco_eox_enabled': False,
        'cisco_eox_client_id': '',
        'cisco_eox_client_secret': '',
        'cisco_eox_sync_interval': 10080,  # minutes (default: weekly)
        'cisco_eox_manufacturer_names': 'Cisco',
    },
}
```

> **Note:** Cisco EoX credentials configured here are read as plain text from your configuration file.
> For production deployments it is recommended to configure them instead through the Web UI
> (`/lifecycle/cisco-eox/settings/`), where the client secret is stored Fernet-encrypted at rest.

### Available Settings

#### UI Card Positions

| Setting | Default | Description |
|---------|---------|-------------|
| `lifecycle_card_position` | `right_page` | Position of the Hardware Lifecycle Info card on DeviceType and ModuleType detail pages. Options: `left_page`, `right_page`, `full_width_page`. |
| `contract_card_position` | `right_page` | Position of the Support Contracts card on Device and VirtualMachine detail pages. Options: `left_page`, `right_page`, `full_width_page`. |
| `license_card_position` | `right_page` | Position of the Licenses card on Device and VirtualMachine detail pages. Options: `left_page`, `right_page`, `full_width_page`. |

#### Cisco EoX API (`PLUGINS_CONFIG` fallback)

These settings are only used when no database configuration record exists. The Web UI (`/lifecycle/cisco-eox/settings/`) takes precedence when configured.

| Setting | Default | Description |
|---------|---------|-------------|
| `cisco_eox_enabled` | `False` | Enable the Cisco EoX background sync job. |
| `cisco_eox_client_id` | `''` | OAuth Client ID from [Cisco API Console](https://apiconsole.cisco.com/). Requires an active SNTC or PSS agreement. |
| `cisco_eox_client_secret` | `''` | OAuth Client Secret. Stored as plain text here; use the Web UI for encrypted storage. |
| `cisco_eox_sync_interval` | `10080` | Sync frequency in minutes. Common values: `60` (hourly), `1440` (daily), `10080` (weekly), `20160` (biweekly), `43200` (monthly). |
| `cisco_eox_manufacturer_names` | `'Cisco'` | Comma-separated list of manufacturer names whose DeviceTypes and ModuleTypes are queried (e.g. `'Cisco,Cisco Systems'`). |

### Cisco EoX Integration

The plugin includes a background job (`CiscoEoXSyncJob`) that automatically populates `HardwareLifecycle` records with end-of-life dates from the [Cisco EoX API](https://developer.cisco.com/docs/support-apis/eox/).

**Lookup order per DeviceType / ModuleType:**

1. Finds a serial number from a related Device or Module and queries `EOXBySerialNumber`.
2. Falls back to the `part_number` field and queries `EOXByProductID` if no serial is available or the serial lookup returns no data.

**Fields populated:**

| Cisco API field | HardwareLifecycle field |
|---|---|
| `EndOfSaleDate` | `end_of_sale` |
| `EndOfSWMaintenanceReleases` | `end_of_maintenance` |
| `EndOfSecurityVulSupportDate` | `end_of_security` |
| `LastDateOfSupport` | `end_of_support` |
| `EndOfServiceContractRenewal` | `last_contract_renewal` |
| `LinkToProductBulletinURL` | `documentation` |

**Web UI configuration** is available at `/lifecycle/cisco-eox/settings/`. After entering credentials and enabling the sync, the job is automatically scheduled at the configured interval. An on-demand **Run Now** button is also provided. Job history is displayed on the settings page and in NetBox's built-in **System → Jobs** view.

### Hardware Lifecycle Info Card

Displays EOL/EOS information for the hardware type on Device, Module, DeviceType, and ModuleType detail pages.

### Support Contracts Card

Displays all contract assignments on Device and VirtualMachine detail pages, grouped by status:

- **Active**: Contracts currently in effect
- **Future**: Contracts with a start date in the future
- **Unspecified**: Contracts without an end date
- **Expired**: Contracts that have ended (lazy-loaded for performance)

## Usage

TBD

## Additional Notes

TBD

## Contribute

Contributions are always welcome!  Please open an issue first before contributing as the scope is going to be kept
intentionally narrow

