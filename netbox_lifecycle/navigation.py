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
contracts = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportcontract_list',
    link_text='Contracts',
)
licenses = PluginMenuItem(
    link='plugins:netbox_lifecycle:license_list',
    link_text='Licenses',
)


menu = PluginMenu(
    label='Hardware Lifecycle',
    groups=(
        ('Lifecycle', (lifecycle, )),
        ('Support Contracts', (vendors, contracts, )),
        ('Licensing', (licenses, )),
    ),
    icon_class='mdi mdi-router'
)
