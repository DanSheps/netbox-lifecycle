# NetBox Lifecycle Plugin

The NetBox Lifecycle plugin adds hardware EOS/EOL, license and support contract tracking to NetBox.

## Features

* Tracking EOL/EOS data for device types and module types
* Tracking licenses, assignable to devices and virtual machines
* Tracking support contracts, assignable to devices, modules and virtual machines

## Requirements

* NetBox 4.5 or later
* Python 3.12 or later

## Compatibility Matrix

| NetBox Version | Plugin Version |
| -------------- | -------------- |
| 4.1.x | 1.1.5 |
| 4.2.x | 1.1.5 |
| 4.3.x | 1.1.6 |
| 4.4.x | 1.1.6 |
| 4.5.x | 1.1.8 |
| 4.6.x | 1.1.9 |

## Installation

The plugin is published on PyPI as [netbox-lifecycle](https://pypi.org/project/netbox-lifecycle/) and follows the standard [NetBox plugin installation procedure](https://netboxlabs.com/docs/netbox/plugins/#installing-plugins). The steps below assume a NetBox installation at `/opt/netbox`; adjust paths to match your environment.

1. Install the package into the NetBox virtual environment:

   ```shell
   source /opt/netbox/venv/bin/activate
   pip install netbox-lifecycle
   ```

2. Add the package to `local_requirements.txt` in the NetBox root directory so it is reinstalled automatically whenever NetBox is upgraded:

   ```shell
   echo netbox-lifecycle >> /opt/netbox/local_requirements.txt
   ```

3. Enable the plugin in the `PLUGINS` section of `configuration.py`:

   ```python
   PLUGINS = [
       'netbox_lifecycle',
   ]
   ```

4. Apply the database migrations:

   ```shell
   python3 /opt/netbox/netbox/manage.py migrate
   ```

5. Restart NetBox to load the plugin. How to do this depends on how NetBox is deployed.

If you run NetBox in Docker, install the plugin by building a custom image as described in the [netbox-docker plugin documentation](https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins) instead of steps 1 and 2.

## Configuration

The plugin can be configured via `PLUGINS_CONFIG` in your NetBox configuration file:

```python
PLUGINS_CONFIG = {
    'netbox_lifecycle': {
        'lifecycle_card_position': 'right_page',
        'contract_card_position': 'right_page',
        'license_card_position': 'right_page',
    },
}
```

### Available Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `lifecycle_card_position` | `right_page` | Position of the Hardware Lifecycle Info card on Device, Module, DeviceType, and ModuleType detail pages. Options: `left_page`, `right_page`, `full_width_page`. |
| `contract_card_position` | `right_page` | Position of the Support Contracts card on Device, Module, and VirtualMachine detail pages. Options: `left_page`, `right_page`, `full_width_page`. |
| `license_card_position` | `right_page` | Position of the Licenses card on Device and VirtualMachine detail pages. Options: `left_page`, `right_page`, `full_width_page`. |

### Hardware Lifecycle Info Card

Displays EOL/EOS information for the hardware type on Device, Module, DeviceType, and ModuleType detail pages.

### Support Contracts Card

Displays all contract assignments on Device, Module, and VirtualMachine detail pages, grouped by status:

- **Active**: Contracts currently in effect
- **Future**: Contracts with a start date in the future
- **Unspecified**: Contracts without an end date
- **Expired**: Contracts that have ended (lazy-loaded for performance)

### Licenses Card

Displays all license assignments on Device and VirtualMachine detail pages.

## Contribute

Contributions are always welcome! Please open an issue first before contributing as the scope is going to be kept
intentionally narrow.
