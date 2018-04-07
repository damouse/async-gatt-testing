import array
import time

import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

from gi.repository import GObject
import advertising
import gatt_server
import argparse

import asyncio


async def async_main():
    print(f"Starting bluetooth loop with loop: ", asyncio.get_event_loop())

    await asyncio.get_event_loop().run_in_executor(None, loop_feed, asyncio.get_event_loop())
    # await asyncio.get_event_loop().run_in_executor(None, main, asyncio.get_event_loop())


async def async_cb(a):
    print('Async callback: ', a)


def loop_feed(loop):
    print('Starting with loop: ', loop)

    for i in range(10):
        time.sleep(2)
        print('About to feed')
        loop.create_task(async_cb(i))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--adapter-name', type=str, help='Adapter name', default='')
    args = parser.parse_args()
    adapter_name = args.adapter_name

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    mainloop = GObject.MainLoop()

    advertising.advertising_main(mainloop, bus, adapter_name)
    gatt_server.gatt_server_main(mainloop, bus, adapter_name)
    mainloop.run()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(async_main())
