from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

lifecycle = PluginMenuItem(
    link='plugins:netbox_lifecycle:hardwarelifecycle_list',
    link_text='Hardware Lifecycle',
    permissions=['netbox_lifecycle.view_hardwarelifecycle'],
    buttons=[
        PluginMenuButton(
            link="plugins:netbox_lifecycle:hardwarelifecycle_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
        ),
    ]
)

vendors = PluginMenuItem(
    link='plugins:netbox_lifecycle:vendor_list',
    link_text='Vendors',
    permissions=['netbox_lifecycle.view_vendor'],
    buttons=[
        PluginMenuButton(
            link="plugins:netbox_lifecycle:vendor_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
        ),
    ]
)
skus = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportsku_list',
    link_text='Support SKUs',
    permissions=['netbox_lifecycle.view_supportsku'],
    buttons=[
        PluginMenuButton(
            link="plugins:netbox_lifecycle:supportsku_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
        ),
    ]
)
contracts = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportcontract_list',
    link_text='Contracts',
    permissions=['netbox_lifecycle.view_supportcontract'],
    buttons=[
        PluginMenuButton(
            link="plugins:netbox_lifecycle:supportcontract_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
        ),
    ]
)
contract_assignments = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportcontractassignment_list',
    link_text='Contract Assignments',
    permissions=['netbox_lifecycle.view_supportcontractassignment'],
    buttons=[
        PluginMenuButton(
            link="plugins:netbox_lifecycle:supportcontractassignment_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
        ),
    ]
)
licenses = PluginMenuItem(
    link='plugins:netbox_lifecycle:license_list',
    link_text='Licenses',
    permissions=['netbox_lifecycle.view_license'],
    buttons=[
        PluginMenuButton(
            link="plugins:netbox_lifecycle:license_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
        ),
    ]
)
license_assignments = PluginMenuItem(
    link='plugins:netbox_lifecycle:licenseassignment_list',
    link_text='License Assignments',
    permissions=['netbox_lifecycle.view_licenseassignment'],
    buttons=[
        PluginMenuButton(
            link="plugins:netbox_lifecycle:licenseassignment_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
        ),
    ]
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
