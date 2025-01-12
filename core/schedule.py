import os
import subprocess
import time
from datetime import datetime

import pytz
import schedule

from core.logger import logger
from core.settings import settings


kyiv_tz = pytz.timezone('Europe/Kiev')
dumps_folder = 'dumps'

os.makedirs(dumps_folder, exist_ok=True)


def create_dump():
    current_time = datetime.now(kyiv_tz).strftime('%Y-%m-%d_%H-%M-%S')
    dump_filename = f'{dumps_folder}/db_dump_{current_time}.sql'

    logger.info(f'Starting to create dump: {dump_filename}')
    command = (
        f'PGPASSWORD={settings.postgres_password} '
        f'pg_dump -U {settings.postgres_user} '
        f'-h {settings.postgres_host} '
        f'-d {settings.postgres_db} '
        f'-F c -b -v '
        f'-f {dump_filename}'
    )
    try:
        subprocess.run(command, shell=True, check=True)
        logger.info(f'Successfully created dump: {dump_filename}')
    except subprocess.CalledProcessError as e:
        logger.error(f'Error creating dump: {e}', exc_info=True)


# We plan the task for 12:00 every day Kyiv
schedule.every().day.at('12:00').do(create_dump)


while True:
    schedule.run_pending()
    time.sleep(60)
