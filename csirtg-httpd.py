import logging
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import textwrap
import os
from flask import Flask, redirect, render_template, request
import json
from pprint import pprint
import sys
import arrow

from csirtgsdk.indicator import Indicator

USER = os.getenv('CSIRTG_USER', '')
FEED = os.getenv('CSIRTG_FEED', '')
TOKEN = os.getenv('CSIRTG_TOKEN', '')
PORT = os.getenv('PORT', 8080)
PORT = int(PORT)

TRACE = os.getenv('TRACE', False)

# logging configuration
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'
logger = logging.getLogger(__name__)

if TRACE == '1':
    logger.setLevel(logging.DEBUG)

app = Flask(__name__)

context = set()
day = None


def _log_indicator(indicator, content):
    global context
    global day

    today = arrow.utcnow().format('YYYY-MM-DD')
    if today != day:
        context = set()
        day = today

    if indicator in context:
        return

    context.add(indicator)

    i = {
        "user": USER,
        "feed": FEED,
        "indicator": indicator,
        "tags": ['httpd', 'bruteforce', 'scanner'],
        "description": 'unauthorized probe',
        "portlist": "80",
        "content": content,
    }

    logger.debug(json.dumps(i, indent=4))

    if TOKEN != '':
        try:
            ret = Indicator(i).submit()
            logger.debug(ret)
        except Exception as e:
            logger.error(e)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    _log_indicator(ip, dict(request.headers))

    return redirect('wp-login.php')

def main():
    p = ArgumentParser(
        description=textwrap.dedent('''\
                example usage:
                    $ csirtg-httpd -d
                    $ csirtg-httpd
                '''),
        formatter_class=RawDescriptionHelpFormatter,
    )

    p.add_argument('-d', '--debug', action='store_true')
    p.add_argument('--log')

    args = p.parse_args()

    loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    console.setLevel(loglevel)
    logger.addHandler(console)
    # logging.propagate = False


    if TOKEN != '':
        if USER == '':
            raise SystemError('Missing envvar: CSIRTG_USER')
        if FEED == '':
            raise SystemError('Missing envvar: CSIRTG_FEED')

        logger.info(f"Logging indicators to {USER}/{FEED}")

    app.run(debug=True, host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
