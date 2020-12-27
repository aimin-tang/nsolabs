# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


class ServiceCallbacks(Service):

    def get_service_params(self, service):
        name = service.list_name
        desc = service.description
        device = service.device
        entries = service.prefix_entry

        return name, desc, device, entries

    def get_entry_leaves(self, entry):
        return entry.subnet, entry.op.prefix_length_op, entry.op.prefix_length

    def create_prefix(self, prefixes, name, desc):
        prefix = prefixes.create(name)


    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')
        with ncs.maapi.single_write_trans('admin', 'python') as t:
            root = ncs.maagic.get_root(t)
            # name, desc, device, entries = self.get_service_params(service)
            # device = root.devices.device[device]
            # prefixes = device.config.nx__ip.prefixes
            # self.create_prefix(prefixes, name, desc)


    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')
        self.register_service('ip-prefix-rfs-servicepoint', ServiceCallbacks)

    def teardown(self):
        self.log.info('Main FINISHED')
