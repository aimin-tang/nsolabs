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
        # all in str format
        return str(entry.sm_verb), entry.subnet_mask, str(entry.op_verb), entry.op_length

    def create_prefix(self, prefixes, ip_prefix_name, desc, entries):
        prefix = prefixes.create(ip_prefix_name)
        prefix.description = desc
        for i, entry in enumerate(entries):
            sm_verb, subnet_mask, op_verb, op_length = self.get_entry_leaves(entry)
            print("========")
            print(sm_verb, type(sm_verb))
            print(subnet_mask, type(subnet_mask))
            print(op_verb, type(op_verb))
            print(op_length, type(op_length))
            print("--------")
            seq = (i + 1) * 5
            prefix.seq.create(seq)
            if sm_verb == 'permit':
                prefix.seq[seq].permit = subnet_mask
            elif sm_verb == 'deny':
                prefix.seq[seq].deny = subnet_mask
            if op_verb == 'le':
                prefix.seq[seq].le = op_length
            elif op_verb == 'gt':
                prefix.seq[seq].gt = op_length
            elif op_verb == 'eq':
                prefix.seq[seq].eq = op_length

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')
        # with ncs.maapi.Maapi() as m:
        #     with ncs.maapi.Session(m, 'admin', 'python'):
        #         with m.start_write_trans() as t:
        #             ip_prefix_name, desc, device_name, entries = self.get_service_params(service)
        #             device = root.devices.device[device_name]
        #             prefixes = device.config.nx__ip.prefix_list.prefixes
        #             self.create_prefix(prefixes, ip_prefix_name, desc, entries)
        #             t.apply()

        ip_prefix_name, desc, device_name, entries = self.get_service_params(service)
        vars = ncs.template.Variables()
        vars.add('IP_PREFIX_NAME', ip_prefix_name)
        vars.add('DESC', desc)
        template = ncs.template.Template(service)
        template.apply('ip_prefix_rfs-template', vars)

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
