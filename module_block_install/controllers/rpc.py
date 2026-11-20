# Copyright 2026 Trobz
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import contextvars

from odoo.http import request, route

from odoo.addons.rpc.controllers import RPC

# The HTTP request of an ``/xmlrpc`` or ``/jsonrpc`` call.
rpc_request = contextvars.ContextVar("module_block_install_rpc_request", default=None)


class ModuleBlockInstallRPC(RPC):
    """Remember the request of the ``/xmlrpc``, ``/xmlrpc/2`` and ``/jsonrpc``
    calls.

    ``odoo.http.router.dispatch_rpc`` unbinds ``odoo.http.request`` while it
    runs the call, as in a script run on the server. Keep it at hand so these
    calls are still seen as HTTP requests.
    """

    def _module_block_install_run(self, func, *args):
        token = rpc_request.set(request._get_current_object())
        try:
            return func(*args)
        finally:
            rpc_request.reset(token)

    def _xmlrpc(self, service):
        return self._module_block_install_run(super()._xmlrpc, service)

    @route()
    def jsonrpc(self, service, method, args):
        return self._module_block_install_run(super().jsonrpc, service, method, args)
