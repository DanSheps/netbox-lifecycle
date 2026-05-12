from netbox.ui.panels import Panel, ObjectsTablePanel
from utilities.querydict import dict_to_querydict
from utilities.string import title
from utilities.views import get_viewname


class TabbedTablePanel(Panel):
    """
    A panel which displays panels within tabs.
    """

    template_name = 'netbox_lifecycle/ui/panels/tabbed_table.html'

    def __init__(self, tabs: dict, **kwargs):
        super().__init__(**kwargs)
        for tab in tabs.values():
            if tab is ObjectsTablePanel:
                raise TypeError(
                    f"TabbedTablePanel only accepts ObjectsTablePanel instances, got {type(tab)}"
                )
        self.tabs = tabs

    def get_context(self, context):
        tabs = []
        first = True
        for name, panel in self.tabs.items():
            # If no title is specified, derive one from the model name
            url_params = {
                k: v(context) if callable(v) else v for k, v in panel.filters.items()
            }

            if 'return_url' not in url_params and 'object' in context:
                url_params['return_url'] = context['object'].get_absolute_url()
            if panel.include_columns:
                url_params['include_columns'] = ','.join(panel.include_columns)
            if panel.exclude_columns:
                url_params['exclude_columns'] = ','.join(panel.exclude_columns)

            tab = {
                'name': name,
                'model': panel.model,
                'viewname': get_viewname(panel.model, 'list'),
                'title': panel.title or title(panel.model._meta.verbose_name_plural),
                'active': first,
                'url_params': dict_to_querydict(url_params),
            }
            first = False
            tabs.append(tab)

        return {
            **super().get_context(context),
            'title': self.title,
            'tabs': tabs,
        }
