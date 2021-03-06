#
# DBus interface for the manual partitioning module.
#
# Copyright (C) 2018 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
from pyanaconda.dbus.interface import dbus_interface
from pyanaconda.dbus.property import emits_properties_changed
from pyanaconda.dbus.typing import *  # pylint: disable=wildcard-import
from pyanaconda.modules.common.constants.objects import MANUAL_PARTITIONING
from pyanaconda.modules.common.structures.partitioning import MountPointRequest
from pyanaconda.modules.storage.partitioning.base_interface import PartitioningInterface


@dbus_interface(MANUAL_PARTITIONING.interface_name)
class ManualPartitioningInterface(PartitioningInterface):
    """DBus interface for the manual partitioning module."""

    def connect_signals(self):
        """Connect the signals."""
        super().connect_signals()
        self.watch_property("Enabled", self.implementation.enabled_changed)
        self.watch_property("Requests", self.implementation.requests_changed)

    @property
    def Enabled(self) -> Bool:
        """Is the manual partitioning enabled?"""
        return self.implementation.enabled

    @emits_properties_changed
    def SetEnabled(self, enabled: Bool):
        """Is the manual partitioning enabled?

        :param enabled: True if enabled, otherwise False
        """
        self.implementation.set_enabled(enabled)

    @property
    def Requests(self) -> List[Structure]:
        """List of mount point requests."""
        return MountPointRequest.to_structure_list(self.implementation.requests)

    @emits_properties_changed
    def SetRequests(self, requests: List[Structure]):
        """Set the mount point requests.

        :param requests: a list of requests
        """
        self.implementation.set_requests(MountPointRequest.from_structure_list(requests))
