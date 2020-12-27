import ncs

def get_entry_leaves(entry):
    return 'permit', '1.1.1.1/32', 'le', '32'

def create_prefix(prefixes, ip_prefix_name, desc, entries):
    prefix = prefixes.create(ip_prefix_name)
    prefix.description = desc
    for i, entry in enumerate(entries):
        sm_verb, subnet_mask, op_verb, op_length = get_entry_leaves(entry)
        print("========")
        print(sm_verb, type(sm_verb))
        print(subnet_mask, type(subnet_mask))
        print(op_verb, type(op_verb))
        print(op_length, type(op_length))
        print("--------")
        seq = (i + 1) * 5
        prefix.seq.create(seq)
        if str(sm_verb) == 'permit':
            prefix.seq[seq].permit = subnet_mask
        elif str(sm_verb) == 'deny':
            prefix.seq[seq].deny = subnet_mask
        if op_verb == 'le':
            prefix.seq[seq].le = op_length
        elif op_verb == 'gt':
            prefix.seq[seq].gt = op_length
        elif op_verb == 'eq':
            prefix.seq[seq].eq = op_length

def device_config():
    with ncs.maapi.Maapi() as m:
        with ncs.maapi.Session(m, 'admin', 'python'):
            with m.start_write_trans() as t:
                root = ncs.maagic.get_root(t)
                device = root.devices.device['c0']
                # device.config.nx__banner.exec.start_marker = 'exec2'
                prefixes = device.config.nx__ip.prefix_list.prefixes
                create_prefix(prefixes, 'l111', 'd111', [0])
                t.apply()


if __name__ == '__main__':
    # parse_service()
    device_config()
    # ruiying()
