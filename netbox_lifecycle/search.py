from netbox.search import SearchIndex, register_search
from netbox_lifecycle.models import SupportContract


@register_search
class SupportContractIndex(SearchIndex):
    model = SupportContract
    fields = (
        ('contract_id', 100),
        ('comments', 5000),
    )
