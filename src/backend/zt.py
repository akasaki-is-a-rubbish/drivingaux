import subprocess
import json
import sys
from time import sleep
from utils.logging import IconColor, IconMode, Logger

TEST_NETWORK_ID = '76cd197450623139'

logger = Logger('ZeroTier', ic=IconMode.star_filled, ic_color=IconColor.yellow)

def init():
    """
    Returns the IP in the network if success
    """
    logger.log('Checking ZT networks on ' + sys.platform + '...')
    try:
        ztcli = 'zerotier-cli.bat' if sys.platform in ['win32', 'cygwin'] else 'zerotier-cli'
        proc = subprocess.run([ztcli, '-j', 'listnetworks'], stdout=subprocess.PIPE)
        if proc.returncode != 0:
            logger.err('Failed to check ZT network.')
            return
        networks: list = json.loads(proc.stdout)
        networks = [x for x in networks if x['id'] == TEST_NETWORK_ID]
        if len(networks) == 0:
            logger.log("Joining the network...")
            proc = subprocess.run([ztcli, '-j', 'join', TEST_NETWORK_ID], stdout=subprocess.PIPE)
            if proc.returncode != 0:
                logger.err('Failed to join ZT network.')
                return
            networks = [json.loads(proc.stdout)]
            logger.log("Joined the network.")
        else:
            logger.log("Had already joined the network.")
        while (len(networks[0]['assignedAddresses']) == 0):
            sleep(3)
            proc = subprocess.run([ztcli, '-j', 'listnetworks'], stdout=subprocess.PIPE)
            if proc.returncode != 0:
                logger.err('Failed to check ZT network.')
                return
            networks: list = json.loads(proc.stdout)
            networks = [x for x in networks if x['id'] == TEST_NETWORK_ID]
        cidr: str = networks[0]['assignedAddresses'][0]
        ip = cidr[0:cidr.index('/')]
        logger.log('IP: ' + ip)
        return ip
    except Exception as e:
        logger.log('Error initializing ZT:')
        logger.err(str(e))
