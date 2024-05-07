from netbox.plugins import PluginMenuItem, PluginMenu

lifecycle = PluginMenuItem(
    link='plugins:netbox_lifecycle:hardwarelifecycle_list',
    link_text='Hardware Lifecycle',
    permissions=['netbox_lifecycle.view_hardwarelifecycle'],
)

vendors = PluginMenuItem(
    link='plugins:netbox_lifecycle:vendor_list',
    link_text='Vendors',
    permissions=['netbox_lifecycle.view_vendor'],
)
skus = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportsku_list',
    link_text='Support SKUs',
    permissions=['netbox_lifecycle.view_supportsku'],
)
contracts = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportcontract_list',
    link_text='Contracts',
    permissions=['netbox_lifecycle.view_supportcontrnact'],
)
contract_assignments = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportcontractassignment_list',
    link_text='Contract Assignments',
    permissions=['netbox_lifecycle.view_supportcontractassignment'],
)
licenses = PluginMenuItem(
    link='plugins:netbox_lifecycle:license_list',
    link_text='Licenses',
    permissions=['netbox_lifecycle.view_license'],
)
license_assignments = PluginMenuItem(
    link='plugins:netbox_lifecycle:licenseassignment_list',
    link_text='License Assignments',
    permissions=['netbox_lifecycle.view_licenseassignment'],
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
