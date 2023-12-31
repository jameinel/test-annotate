#!venv/bin/python3
import asyncio
import argparse
import logging
import sys

from juju import jasyncio
import juju.model



async def get_annotations(model, args):
    logging.info('getting annotations')
    annotations = await model.get_annotations()
    if args.key is None:
        for key, value in annotations.items():
            print(f'{key}: {value!r}')
    else:
        value = annotations[args.key]
        print(value)


async def set_annotation(model, args):
    logging.info(f'setting annotation for {args.key!r}')
    await model.set_annotations({args.key: args.value})


async def get_model():
    logging.info('getting model')
    model = juju.model.Model()
    await model.connect()
    return model


async def run_func(args):
    model = await get_model()
    try:
        await args.func(model, args)
    finally:
        logging.info('disconnecting the model')
        if args.sleep_before_disconnect:
            jasyncio.sleep(args.sleep_before_disconnect)
        await model.disconnect()


def parse_args(args):
    p = argparse.ArgumentParser()
    p.add_argument('--debug', action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.WARNING)
    p.add_argument('--verbose', '-v', action="store_const", dest="loglevel", const=logging.INFO)
    p.add_argument('--quiet', action="store_const", dest="loglevel", const=logging.CRITICAL)
    p.add_argument('--sleep-before-disconnect', type=float, default=None, help='sleep briefly before disconnecting')
    sub = p.add_subparsers(required=True)
    getp = sub.add_parser('get')
    getp.set_defaults(func=get_annotations)
    getp.add_argument("key", help='the key to set', nargs='?')
    setp = sub.add_parser('set')
    setp.set_defaults(func=set_annotation)
    setp.add_argument("key", help='the key to set')
    setp.add_argument("value", help='set the value of key to this value, empty string removes the annotation')
    return p.parse_args(args)


def main():
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    args = parse_args(sys.argv[1:])
    rootLogger = logging.getLogger()
    rootLogger.setLevel(args.loglevel)
    jasyncio.run(run_func(args))


if __name__ == '__main__':
    main()

# vim: expandtab ts=4 sts=4 shiftwidth=4 autoindent:
