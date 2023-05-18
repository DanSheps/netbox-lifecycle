from extras.plugins import PluginMenu, PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

lifecycle = PluginMenuItem(
    link='plugins:netbox_lifecycle:hardwarelifecycle_list',
    link_text='Hardware Lifecycle',
)

vendors = PluginMenuItem(
    link='plugins:netbox_lifecycle:vendor_list',
    link_text='Vendors',
)
skus = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportsku_list',
    link_text='Support SKUs',
)
contracts = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportcontract_list',
    link_text='Contracts',
)
contract_assignments = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportcontractassignment_list',
    link_text='Contract Assignments',
)
licenses = PluginMenuItem(
    link='plugins:netbox_lifecycle:license_list',
    link_text='Licenses',
)
license_assignments = PluginMenuItem(
    link='plugins:netbox_lifecycle:licenseassignment_list',
    link_text='License Assignments',
)


menu = PluginMenu(
    label='Hardware Lifecycle',
    groups=(
        ('Lifecycle', (lifecycle, )),
        ('Support Contracts', (vendors, skus, contracts, contract_assignments)),
        ('Licensing', (licenses, license_assignments)),
    ),
    icon_class='mdi mdi-server'
)
