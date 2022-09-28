#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.

from hpctlib.ext.interfaces.file import FileDataInterface
from hpctlib.interface import interface_registry
from hpctlib.interface.relation import RelationSuperInterface, UnitBucketInterface
from hpctlib.interface.value import String


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
