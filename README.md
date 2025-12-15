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
        'lifecycle_card_position': 'right_page',
        'contract_card_position': 'right_page',
    },
}
```

### Available Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `lifecycle_card_position` | `right_page` | Position of the Hardware Lifecycle Info card on Device, Module, DeviceType, and ModuleType detail pages. Options: `left_page`, `right_page`, `full_width_page`. |
| `contract_card_position` | `right_page` | Position of the Support Contracts card on Device and VirtualMachine detail pages. Options: `left_page`, `right_page`, `full_width_page`. |

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

