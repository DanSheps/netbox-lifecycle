from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

APP_LABEL = 'netbox_lifecycle'


def get_model_buttons(model_name, actions=('add',)):
    buttons = []

    if 'add' in actions:
        buttons.append(
            PluginMenuButton(
                link=f'plugins:{APP_LABEL}:{model_name}_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=[f'{APP_LABEL}.add_{model_name}'],
            )
        )

    if 'import' in actions:
        buttons.append(
            PluginMenuButton(
                link=f'plugins:{APP_LABEL}:{model_name}_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=[f'{APP_LABEL}.add_{model_name}'],
            )
        )

    return buttons


def get_model_item(model_name, label, actions=('add',)):
    return PluginMenuItem(
        link=f'plugins:{APP_LABEL}:{model_name}_list',
        link_text=label,
        permissions=[f'{APP_LABEL}.view_{model_name}'],
        buttons=get_model_buttons(model_name, actions),
    )


hardwarelifecycle_item = get_model_item('hardwarelifecycle', 'Hardware Lifecycle')
vendor_item = get_model_item('vendor', 'Vendors')
supportsku_item = get_model_item('supportsku', 'Support SKUs')
supportcontract_item = get_model_item('supportcontract', 'Contracts')
supportcontractassignment_item = get_model_item('supportcontractassignment', 'Contract Assignments')
license_item = get_model_item('license', 'Licenses')
licenseassignment_item = get_model_item('licenseassignment', 'License Assignments')

menu = PluginMenu(
    label='Hardware Lifecycle',
    groups=(
        ('Lifecycle', (hardwarelifecycle_item,)),
        ('Support Contracts', (vendor_item, supportsku_item, supportcontract_item, supportcontractassignment_item)),
        ('Licensing', (license_item, licenseassignment_item)),
    ),
    icon_class='mdi mdi-server',
)
