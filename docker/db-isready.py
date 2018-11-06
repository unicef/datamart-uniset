#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib.parse
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()

    parser.add_argument(
        '--db', default=os.environ.get('DATABASE_URL'),
        dest='connection_url',
        action="store",
        help='database url',
    )

    parser.add_argument(
        '--redis', default=os.environ.get('REDIS_URL'),
        dest='connection_url',
        action="store",
        help='database url',
    )

    parser.add_argument(
        '--sleep', default=1,
        action="store",
        type=int,
        help='sleep time between attempt',
    )
    # parser.add_argument(
    #     '--wait', default=False,
    #     action="store_true",
    #     help='wait until database is available',
    # )
    parser.add_argument(
        '--debug', default=False,
        action="store_true",
        help='debug mode. WARNING can dump passwords',
    )
    parser.add_argument(
        '--timeout', default=30,
        type=int,
        help='timeout in sec before OperationalError',
    )

    parser.add_argument(
        '--connection', default='default',
        help='timeout in sec before OperationalError',
    )
    args = parser.parse_args()
    url = urllib.parse.urlparse(args.connection_url)
    elapsed = 0
    retcode = 1
    if url.scheme == 'postgres':
        import psycopg2
    else:
        raise Exception("Database not supported")
    try:
        sys.stdout.write(f"Checking connnection {url.hostname}:{url.port}...\n")

        while True:
            try:
                conn = psycopg2.connect(host=url.hostname,
                                    port=url.port,
                                    user=url.username,
                                    password=url.password,
                                    database=url.path[1:])
                conn = conn.cursor()
            except Exception as e:
                if elapsed < args.timeout:
                    sys.stdout.write("." * elapsed)
                    sys.stdout.flush()
                    time.sleep(args.sleep)
                    elapsed += 1
                else:
                    sys.stderr.write(f"\nDatabase on {url.hostname}:{url.port} "
                                     f"is not available after {elapsed} secs\n")
                    if args.debug:
                        sys.stderr.write(f"Error is: {e}\n")
                    retcode = 1
                    break
            else:
                sys.stdout.write(f"Connection {url.hostname}:{url.port} successful\n")
                retcode = 0
                break
    except KeyboardInterrupt:  # pragma: no-cover
        sys.stdout.write('Interrupted')
    sys.exit(retcode)


if __name__ == "__main__":
    main()
