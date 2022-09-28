#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Sendfile client.
"""

import logging
import os

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus

from hpctlib.interface import interface_registry

# load
import interfaces.sendfile

logger = logging.getLogger(__name__)

SAVEDIR = "/tmp/sendfile-client"


class HpctSendfileClientCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.update_status, self._on_update_status)

        self.framework.observe(self.on.sendfile_relation_joined, self._on_sendfile_relation_joined)
        self.framework.observe(
            self.on.sendfile_relation_changed, self._on_sendfile_relation_changed
        )

        self.framework.observe(self.on.list_files_action, self._on_list_files_action)

        self.siface = interface_registry.load("relation-unit-sendfile", self, "sendfile")

    def _on_config_changed(self, event):
        pass

    def _on_start(self, event):
        try:
            os.makedirs(SAVEDIR)
        except:
            pass

        self.unit.status = ActiveStatus("ready")

    def _on_update_status(self, event):
        pass

    def _on_sendfile_relation_joined(self, event):
        pass

    def _on_sendfile_relation_changed(self, event):
        server_iface = self.siface.select(event.unit)
        client_iface = self.siface.select(self.unit)

        if server_iface.file.nonce == "":
            # nothing ready to get
            return

        name = server_iface.file.name
        if "/" in name:
            event.log(f"bad filename ({name})")

        path = f"{SAVEDIR}/{name}"
        metapath = f"{SAVEDIR}/{name}.meta"

        # dump to disk
        server_iface.file.save(path)
        # TODO: dump metadata to metapath file
        logger.debug(f"save file ({path})")

        # acknowledge receipt
        client_iface.nonce = server_iface.file.nonce
        logger.debug(f"acknowledging receipt for file ({path}) nonce ({client_iface.nonce})")

    def _on_list_files_action(self, event):
        logger.debug(f"files received ({os.listdir(SAVEDIR)})")


if __name__ == "__main__":
    main(HpctSendfileClientCharm)
