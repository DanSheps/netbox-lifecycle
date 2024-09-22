import datetime

from netaddr.ip import IPAddress


class DateFieldMixin:
    def model_to_dict(self, instance, fields, api=False):
        model_dict = super().model_to_dict(instance, fields, api)
        for key, value in list(model_dict.items()):
            if api:
                if type(value) is datetime.date:
                    model_dict[key] = str(value)
        return model_dict


class HardwareLifecycleViewMixin:
    def model_to_dict(self, instance, fields, api=False):
        model_dict = super().model_to_dict(instance, fields, api)
        for key, value in list(model_dict.items()):
            if type(value) is datetime.date:
                model_dict[key] = str(value)
            elif key in ['device_type', 'module_type'] and isinstance(value, object):
                model_dict[key] = value.first().pk
        return model_dict
