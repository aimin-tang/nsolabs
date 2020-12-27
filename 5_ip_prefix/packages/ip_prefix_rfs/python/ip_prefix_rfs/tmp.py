import ncs


def parse_service():
    with ncs.maapi.single_write_trans('admin', 'python') as t:
        root = ncs.maagic.get_root(t)
        service = root.ip_prefix_rfs__ip_prefix_rfs['l1']
        name = service.list_name
        desc = service.description
        device = service.device
        entries = service.prefix_entry

    return name, desc, device, entries


def device_config():
    with ncs.maapi.single_write_trans('admin', 'python') as t:
        root = ncs.maagic.get_root(t)
        device = root.devices.device['c0']
        prefixes = device.config.nx__ip.prefix_list.prefixes
        prefix = prefixes.create('l111')
        prefix.description = 'd111'
        seq = prefix.seq.create(5)
        print(dir(seq))


if __name__ == '__main__':
    parse_service()
    # device_config()
