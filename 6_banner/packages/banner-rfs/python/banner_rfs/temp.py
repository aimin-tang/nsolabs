import ncs


def f1():
    with ncs.maapi.Maapi() as m:
        with ncs.maapi.Session(m, 'admin', 'python'):
            with m.start_write_trans() as t:
                root = ncs.maagic.get_root(t)
                device_name = 'c0'
                device = root.ncs__devices.device[device_name]
                device.config.nx__banner.exec.start_marker = 'b1'
                t.apply()

f1()