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
    min_version = '4.3.0'
    required_settings = []
    default_settings = {
        'contract_card_position': 'right_page',
    }
    queues = []
    graphql_schema = 'graphql.schema.schema'

    def ready(self):

        super().ready()

        from django.contrib.contenttypes.fields import GenericRelation
        from dcim.models import DeviceType, ModuleType
        from netbox_lifecycle.models import (
            HardwareLifecycle,
        )  # ,SupportContractAssignment

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
