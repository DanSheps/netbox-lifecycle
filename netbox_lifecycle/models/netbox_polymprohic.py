from polymorphic.models import PolymorphicModel
from polymorphic.query import PolymorphicQuerySet

from netbox.models import NetBoxModel

from utilities.querysets import RestrictedQuerySet


class RestrictedPolymorphicQuerySet(PolymorphicQuerySet, RestrictedQuerySet):
    pass


class NetBoxPolymorphicModel(NetBoxModel, PolymorphicModel):
    objects = RestrictedPolymorphicQuerySet.as_manager()

    class Meta:
        abstract = True
