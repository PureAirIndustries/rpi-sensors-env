#!/usr/bin/env python3
"""
@Author: isaac12x/hunterx7
@Date:   2019-07-19T09:24:28+10:00
@Last modified by:   isaac12x/hunterx7
@Last modified time: 2019-07-11T13:26:28+10:00
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sync.timed_runner import TimedRunner

from scs_core.sys.signalled_exit import SignalledExit
from scs_core.sys.system_id import SystemID

from scs_dev.cmd.cmd_sampler import CmdSampler
from scs_dev.sampler.gases_sampler import GasesSampler

from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.bus.i2c import I2C
from scs_host.sync.schedule_runner import ScheduleRunner
from scs_host.sys.host import Host


class GasesSamplerWrapper:

    def start_sampling(self, frequency):
        cmd = CmdSampler()  # test what this does on a terminal

        with I2C.open(Host.I2C_SENSORS) as f:
            system_id = SystemID.load(Host)
            tag = None if system_id is None else system_id.message_tag()
            interface_conf = InterfaceConf.load(Host)
            interface = interface_conf.interface()
            gas_sensors = interface.gas_sensors(Host)
            ndir_monitor = None  # we don't use alphasenses for that.
            sht_conf = SHTConf.load(Host)
            sht = None if sht_conf is None else sht_conf.int_sht()

            runner = TimedRunner(cmd.interval, cmd.samples) if cmd.semaphore is None \
                else ScheduleRunner(cmd.semaphore, False)
            sampler = GasesSampler(runner, tag, ndir_monitor, sht, gas_sensors)
            sampler.start()

            for sample in sampler.samples():
                return JSONify.dumps(sample)

            sampler.stop()
