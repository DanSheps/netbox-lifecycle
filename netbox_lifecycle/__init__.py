from extras.plugins import PluginConfig
from importlib.metadata import metadata

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
    max_version = '3.5.99'
    required_settings = []
    default_settings = {}
    queues = []


config = NetBoxLifeCycle
