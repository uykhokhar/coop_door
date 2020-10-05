import logging

LOG_FILENAME = '/home/pi/coop_door/coop_door.log'
log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename=LOG_FILENAME)
