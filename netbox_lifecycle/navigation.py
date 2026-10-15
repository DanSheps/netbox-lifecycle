from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton

COL_ADD = 'mdi mdi-plus'
COL_IMPORT = 'mdi mdi-upload'

lifecycle = PluginMenuItem(
    link='plugins:netbox_lifecycle:hardwarelifecycle_list',
    link_text='Hardware Lifecycle',
    permissions=['netbox_lifecycle.view_hardwarelifecycle'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_lifecycle:hardwarelifecycle_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_lifecycle.add_hardwarelifecycle'],
        ),
        PluginMenuButton(
            link='plugins:netbox_lifecycle:hardwarelifecycle_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_lifecycle.add_hardwarelifecycle'],
        ),
    ),
)

vendors = PluginMenuItem(
    link='plugins:netbox_lifecycle:vendor_list',
    link_text='Vendors',
    permissions=['netbox_lifecycle.view_vendor'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_lifecycle:vendor_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_lifecycle.add_vendor'],
        ),
        PluginMenuButton(
            link='plugins:netbox_lifecycle:vendor_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_lifecycle.add_vendor'],
        ),
    ),
)
skus = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportsku_list',
    link_text='Support SKUs',
    permissions=['netbox_lifecycle.view_supportsku'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_lifecycle:supportsku_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_lifecycle.add_supportsku'],
        ),
        PluginMenuButton(
            link='plugins:netbox_lifecycle:supportsku_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_lifecycle.add_supportsku'],
        ),
    ),
)
contracts = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportcontract_list',
    link_text='Support Contracts',
    permissions=['netbox_lifecycle.view_supportcontract'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_lifecycle:supportcontract_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_lifecycle.add_supportcontract'],
        ),
        PluginMenuButton(
            link='plugins:netbox_lifecycle:supportcontract_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_lifecycle.add_supportcontract'],
        ),
    ),
)
contract_assignments = PluginMenuItem(
    link='plugins:netbox_lifecycle:supportcontractassignment_list',
    link_text='Support Assignments',
    permissions=['netbox_lifecycle.view_supportcontractassignment'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_lifecycle:supportcontractassignment_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_lifecycle.add_supportcontractassignment'],
        ),
        PluginMenuButton(
            link='plugins:netbox_lifecycle:supportcontractassignment_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_lifecycle.add_supportcontractassignment'],
        ),
    ),
)
licenses = PluginMenuItem(
    link='plugins:netbox_lifecycle:license_list',
    link_text='Licenses',
    permissions=['netbox_lifecycle.view_license'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_lifecycle:license_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_lifecycle.add_license'],
        ),
        PluginMenuButton(
            link='plugins:netbox_lifecycle:license_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_lifecycle.add_license'],
        ),
    ),
)
license_assignments = PluginMenuItem(
    link='plugins:netbox_lifecycle:licenseassignment_list',
    link_text='License Assignments',
    permissions=['netbox_lifecycle.view_licenseassignment'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_lifecycle:licenseassignment_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_lifecycle.add_licenseassignment'],
        ),
        PluginMenuButton(
            link='plugins:netbox_lifecycle:licenseassignment_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_lifecycle.add_licenseassignment'],
        ),
    ),
)
eox_settings = PluginMenuItem(
    link='plugins:netbox_lifecycle:eoxapisettings_list',
    link_text='EoX Settings',
    permissions=['netbox_lifecycle.view_eoxapisettings'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_lifecycle:eoxapisettings_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_lifecycle.add_eoxapisettings'],
        ),
        PluginMenuButton(
            link='plugins:netbox_lifecycle:eoxapisettings_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_lifecycle.add_eoxapisettings'],
        ),
    ),
)
menu = PluginMenu(
    label='Hardware Lifecycle',
    groups=(
        ('Lifecycle', (lifecycle,)),
        ('Vendor Support', (vendors, skus, contracts, contract_assignments)),
        ('Licensing', (licenses, license_assignments)),
        ('EoX API Config', (eox_settings,)),
    ),
    icon_class='mdi mdi-server',
)
