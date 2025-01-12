import os
import subprocess
import time
from datetime import datetime

import pytz
import schedule

from core.logger import logger
from core.settings import settings


def create_dump():
    """Creating a database dump"""
    kyiv_tz = pytz.timezone('Europe/Kiev')
    dumps_folder = 'dumps'
    os.makedirs(dumps_folder, exist_ok=True)

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


def run_spider():
    """Launching Scrapy Spider"""
    logger.info('Starting the OLX spider...')
    try:
        subprocess.run(['scrapy', 'crawl', 'olx'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f'Error when starting spider: {e}')


def schedule_daily_dump():
    """Scheduling a task for daily dump"""
    schedule.every().day.at('12:00').do(create_dump)


def schedule_spider():
    schedule.every(1).minute.do(run_spider)


def run_jobs():
    schedule_daily_dump()
    schedule_spider()

    while True:
        schedule.run_pending()
        time.sleep(60)
