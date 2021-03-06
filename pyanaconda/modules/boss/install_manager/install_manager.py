# Handle installation tasks from modules.
#
# Copyright (C) 2017 Red Hat, Inc.
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
from pyanaconda.core import util
from pyanaconda.dbus import DBus
from pyanaconda.modules.boss.install_manager.installation import SystemInstallationTask

from pyanaconda.anaconda_loggers import get_module_logger
log = get_module_logger(__name__)


class InstallManager(object):
    """Manager of the system installation."""

    def __init__(self):
        """ Create installation manager."""
        self._module_observers = []

    @property
    def module_observers(self):
        """Get all module observers which will be used for installation."""
        return self._module_observers

    @module_observers.setter
    def module_observers(self, modules):
        """Set module observers which will be used for installation.

        :param modules: Module observers list.
        :type modules: list
        """
        self._module_observers = modules

    def install_system_with_task(self):
        """Install the system.

        :return: an instance of the main installation task
        """
        installation_tasks = self._collect_installation_tasks()
        system_task = SystemInstallationTask(installation_tasks)
        return system_task

    def _collect_installation_tasks(self):
        """Collect installation tasks from modules.

        :return: a list of tasks proxies
        """
        tasks = []

        # FIXME: We need to figure out how to handle the sysroot.
        sysroot = util.getSysroot()

        if not self._module_observers:
            log.error("Starting installation without available modules.")

        for observer in self._module_observers:
            # FIXME: This check is here for testing purposes only.
            # Normally, all given modules should be available once
            # we start the installation.
            if not observer.is_service_available:
                log.error("Module %s is not available!", observer.service_name)
                continue

            service_name = observer.service_name
            task_paths = observer.proxy.InstallWithTasks(sysroot)

            for object_path in task_paths:
                log.debug("Getting task %s from module %s", object_path, service_name)
                task_proxy = DBus.get_proxy(service_name, object_path)
                tasks.append(task_proxy)

        return tasks
