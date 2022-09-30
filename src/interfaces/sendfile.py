#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

from hpctinterfaces import interface_registry
from hpctinterfaces.ext.file import FileDataInterface
from hpctinterfaces.relation import RelationSuperInterface, UnitBucketInterface
from hpctinterfaces.value import String


class UnitSendfileRelationSuperInterface(RelationSuperInterface):
    class FileUnitInterface(UnitBucketInterface):

        file = FileDataInterface()

    class AckUnitInterface(UnitBucketInterface):

        nonce = String()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.interface_classes[("provider", "unit")] = self.FileUnitInterface
        self.interface_classes[("requirer", "unit")] = self.AckUnitInterface


interface_registry.register("relation-unit-sendfile", UnitSendfileRelationSuperInterface)
