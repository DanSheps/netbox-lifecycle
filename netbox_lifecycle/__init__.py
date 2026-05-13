from importlib.metadata import metadata

from netbox.plugins import PluginConfig

metadata = metadata('netbox_lifecycle')


class NetBoxLifeCycle(PluginConfig):
    name = metadata.get('Name').replace('-', '_')
    verbose_name = metadata.get('Name').replace('-', ' ').title()
    description = metadata.get('Summary')
    version = metadata.get('Version')
    author = metadata.get('Author')
    author_email = metadata.get('Author-email')
    base_url = 'lifecycle'
    min_version = '4.5.0'
    required_settings = []
    default_settings = {
        'lifecycle_card_position': 'right_page',
        'contract_card_position': 'right_page',
        'license_card_position': 'right_page',
        # Cisco EoX API — fallback to PLUGINS_CONFIG when no DB settings exist
        'cisco_eox_enabled': False,
        'cisco_eox_client_id': '',
        'cisco_eox_client_secret': '',
        'cisco_eox_sync_interval': 10080,  # weekly, in minutes
        'cisco_eox_manufacturer_names': 'Cisco',
    }
    queues = []
    graphql_schema = 'graphql.schema.schema'

    def ready(self):

        super().ready()

        from netbox_lifecycle.jobs import CiscoEoXSyncJob  # noqa: F401 — registers job

        from dcim.models import DeviceType, ModuleType
        from django.contrib.contenttypes.fields import GenericRelation

        from netbox_lifecycle.models import HardwareLifecycle

        # Add Generic Relations to appropriate models
        GenericRelation(
            to=HardwareLifecycle,
            content_type_field='assigned_object_type',
            object_id_field='assigned_object_id',
            related_name='device_type',
            related_query_name='device_type',
        ).contribute_to_class(DeviceType, 'hardware_lifecycle')
        GenericRelation(
            to=HardwareLifecycle,
            content_type_field='assigned_object_type',
            object_id_field='assigned_object_id',
            related_name='module_type',
            related_query_name='module_type',
        ).contribute_to_class(ModuleType, 'hardware_lifecycle')


config = NetBoxLifeCycle
