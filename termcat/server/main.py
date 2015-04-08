#!/usr/bin/env python

import argparse
import asyncio

from utils import *

@asyncio.coroutine
def handle_client(reader, writer, remote_addr):
    """Handles a client connection to create a new paste."""

    # Read data and meta from client
    raw_data = yield from reader.readline()
    decoded_data = raw_data.decode()

    # Pass the data off to create a new paste and encode the response
    paste = handle_new_paste(decoded_data, remote_addr[0])
    r = paste.get_absolute_url() + '\n'
    encoded_response = r.encode()

    # Try to write the response back to the client. If there is a connection
    # error, delete the paste as the client will never see the URL.
    try:
        # Write the response and close
        writer.write(encoded_response)
        yield from writer.drain()
        writer.close()
    except ConnectionResetError:
        delete_paste(paste)

@asyncio.coroutine
def client_worker(reader, writer):
    """The worker thread to handle a client connection. Passes the work
    off to handle_client() and wraps any exceptions.
    """

    remote_addr = writer.get_extra_info('peername')
    try:
        yield from handle_client(reader, writer, remote_addr)
    except Exception as e:
        print_exception(remote_addr, e)
        writer.write('500 Internal Server Error\n'.encode())
        writer.write('Sorry! We are aware of the problem and will try to fix it soon.\n'.encode())
        writer.write(message)
        yield from writer.drain()
        writer.close()

def do_event_loop(host, port):
    """The main event loop to handle connections from clients."""

    loop = asyncio.get_event_loop()
    work = asyncio.start_server(client_worker, host, port, loop=loop)
    server = loop.run_until_complete(work)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

def handle_args():
    parser = argparse.ArgumentParser(description='Server for accepting new pastes')
    parser.add_argument('--host', default='0.0.0.0',
            help='IP address to listen on. Defaults to all available addresses.')
    parser.add_argument('--port', default=9999, type=int,
            help='Port to listen on. Defaults to 9999.')
    return parser.parse_args()


if __name__ == '__main__':
    args = handle_args()
    do_event_loop(args.host, args.port)
