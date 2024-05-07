from importlib.metadata import metadata

from netbox.plugins import PluginConfig

metadata = metadata('netbox_lifecycle')


class NetBoxLifeCycle(PluginConfig):
    name = metadata.get('Name').replace('-', '_')
    verbose_name = metadata.get('Summary')
    description = metadata.get('Description')
    version = metadata.get('Version')
    author = metadata.get('Author')
    author_email = metadata.get('Author-email')
    base_url = 'lifecycle'
    min_version = '3.5.0'
    max_version = '4.0.99'
    required_settings = []
    default_settings = {}
    queues = []

    def ready(self):

        super().ready()

        from django.contrib.contenttypes.fields import GenericRelation
        from dcim.models import Device, DeviceType, ModuleType
        from netbox_lifecycle.models import SupportContractAssignment, HardwareLifecycle

        # Add Generic Relations to appropriate models
        GenericRelation(
            to=HardwareLifecycle,
            content_type_field='assigned_object_type',
            object_id_field='assigned_object_id',
            related_name='device_type',
            related_query_name='device_type'
        ).contribute_to_class(DeviceType, 'hardware_lifecycle')
        GenericRelation(
            to=HardwareLifecycle,
            content_type_field='assigned_object_type',
            object_id_field='assigned_object_id',
            related_name='module_type',
            related_query_name='module_type'
        ).contribute_to_class(ModuleType, 'hardware_lifecycle')


config = NetBoxLifeCycle
