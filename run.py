#!/usr/bin/env python2.7
'''
Title
-----
run.py

Description
-----------
Run the flask app on 127.0.0.1:8090 by default.
Options can be changed by using --host and --port flags.

'''

from app import app
app.debug = True
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set the host and port')
    parser.add_argument('--host', default='127.0.0.1', type=str,
                        help='host')
    parser.add_argument('--port', type=int, default=8095,
                        help='port')
    args = parser.parse_args()
    host = args.host
    port = args.port
    app.run(host=host, port=port, threaded=True)