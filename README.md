# NetBox Lifecycle Plugin

[![PyPI](https://img.shields.io/pypi/v/netbox-lifecycle)](https://pypi.org/project/netbox-lifecycle/)
[![CI](https://github.com/DanSheps/netbox-lifecycle/actions/workflows/ci.yml/badge.svg)](https://github.com/DanSheps/netbox-lifecycle/actions/workflows/ci.yml)

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

## Upgrading

Upgrade the package inside the NetBox virtual environment, then apply any new migrations and restart NetBox:

```shell
source /opt/netbox/venv/bin/activate
pip install --upgrade netbox-lifecycle
python3 /opt/netbox/netbox/manage.py migrate
```

Release notes are published on the [GitHub releases page](https://github.com/DanSheps/netbox-lifecycle/releases).

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

## Usage

All objects live under the Hardware Lifecycle menu, split into three groups: Lifecycle, Vendor Support and Licensing.

To track hardware EOS/EOL, create a Hardware Lifecycle record and assign it to a device type or module type. The dates then appear on the detail pages of that type and of every device or module built from it.

To track support contracts:

1. Create a Vendor for the party you buy support from (Vendor Support > Vendors).
2. Optionally create Support SKUs for the support products you purchase (Vendor Support > Support SKUs).
3. Create a Support Contract for the vendor with its contract ID and start, renewal and end dates (Vendor Support > Support Contracts).
4. Assign the contract, and optionally a SKU, to devices, modules or virtual machines (Vendor Support > Support Assignments).

To track licenses:

1. Create a License for the product (Licensing > Licenses).
2. Assign it to a device or virtual machine, together with the purchasing vendor and a quantity (Licensing > License Assignments).
3. Optionally cover a license assignment with a support contract by selecting it on a Support Assignment.

## Data Model

The plugin defines seven models:

* `HardwareLifecycle` - EOS/EOL dates for a single device type or module type: end of sale, end of maintenance, end of security, end of support, the last dates to attach or renew a contract, and links to the vendor notice and documentation.
* `Vendor` - a party support or licenses are purchased from.
* `SupportSKU` - a support product, tied to a NetBox manufacturer.
* `SupportContract` - a contract with a vendor, with contract ID and start, renewal and end dates.
* `SupportContractAssignment` - links a contract, and optionally a SKU, to a device, module or virtual machine. It can also cover a license assignment, and can carry its own end date when it differs from the contract.
* `License` - a license product, tied to a NetBox manufacturer.
* `LicenseAssignment` - assigns a license to a device or virtual machine, with the purchasing vendor and a quantity.

Note the distinction between manufacturers and vendors: SKUs and licenses reference the NetBox manufacturer that makes the product, while contracts and license assignments reference the plugin's own Vendor model for the party that sells it.

## API

The plugin follows the standard NetBox REST API conventions (authentication, filtering, pagination) under `/api/plugins/lifecycle/`:

* `/api/plugins/lifecycle/hardwarelifecycle/`
* `/api/plugins/lifecycle/license/`
* `/api/plugins/lifecycle/licenseassignment/`
* `/api/plugins/lifecycle/sku/`
* `/api/plugins/lifecycle/supportcontract/`
* `/api/plugins/lifecycle/supportcontractassignment/`
* `/api/plugins/lifecycle/vendor/`

The plugin also extends the NetBox GraphQL schema; all models can be queried through the standard `/graphql/` endpoint.

## Contribute

Contributions are always welcome! Please open an issue first before contributing as the scope is going to be kept
intentionally narrow.
