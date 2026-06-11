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
    },
}
```

### Available Settings

#### UI Card Positions

| Setting | Default | Description |
|---------|---------|-------------|
| `lifecycle_card_position` | `right_page` | Position of the Hardware Lifecycle Info card on DeviceType and ModuleType detail pages. Options: `left_page`, `right_page`, `full_width_page`. |
| `contract_card_position` | `right_page` | Position of the Support Contracts card on Device and VirtualMachine detail pages. Options: `left_page`, `right_page`, `full_width_page`. |
| `license_card_position` | `right_page` | Position of the Licenses card on Device and VirtualMachine detail pages. Options: `left_page`, `right_page`, `full_width_page`. |

### EoX Integration

The plugin includes a vendor-agnostic EoX sync system. Each row in **EoX Settings** (`/lifecycle/eox/`) configures one endpoint — driver, URL, OAuth credentials, sync interval, and a set of in-scope manufacturers. Multiple rows per driver are permitted (e.g. distinct credentials per environment). The OAuth client secret is stored Fernet-encrypted at rest using a key derived from Django's `SECRET_KEY`.

Drivers are pluggable. The currently shipped driver is **Cisco EoX**; add a vendor by implementing `BaseEoXDriver` under `netbox_lifecycle/utilities/eox/drivers/` and registering it in `DRIVERS`.

**Two background jobs:**

- `EoXSyncJob` — automatically scheduled per row via `enqueue_once(interval=row.sync_interval)` whenever the row is saved with `enabled=True`. Re-enqueues itself at the end of each run so interval changes are honored.
- `EoXManualSyncJob` — one-shot, triggered by the **Run Now** action on the row's detail page.

**Lookup order per DeviceType / ModuleType (Cisco driver):**

1. Finds a serial number from a related Device or Module and queries `EOXBySerialNumber`.
2. Falls back to the `part_number` field and queries `EOXByProductID` if no serial is available or the serial lookup returns no data.

**Fields populated by the Cisco driver:**

| Cisco API field | HardwareLifecycle field |
|---|---|
| `EndOfSaleDate` | `end_of_sale` |
| `EndOfSWMaintenanceReleases` | `end_of_maintenance` |
| `EndOfSecurityVulSupportDate` | `end_of_security` |
| `LastDateOfSupport` | `end_of_support` |
| `EndOfServiceContractRenewal` | `last_contract_renewal` |
| `LinkToProductBulletinURL` | `documentation` |

Cisco EoX API access requires an active SNTC or PSS agreement and an OAuth client registered at [apiconsole.cisco.com](https://apiconsole.cisco.com/). Job history is visible on the row's detail page and in NetBox's built-in **System → Jobs** view.

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

