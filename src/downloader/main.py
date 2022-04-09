import argparse
import logging

from api_caller import APICaller
from db_saver import DBSaver


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mask',
                        type=str,
                        default='https://api.hh.ru/vacancies',
                        help='API URL')
    parser.add_argument('--per_page',
                        type=int,
                        default=100,
                        help='number of items per page')
    parser.add_argument('--area',
                        type=int,
                        default=2,
                        help='id of the area - default Saint-Petersburg')

    args = parser.parse_args()

    caller_params = {
        'per_page': args.per_page,
        'area': args.area
    }

    caller = APICaller(args.mask, **caller_params)
    saver = DBSaver()

    logger.info('Downloader started')

    while True:
        vacancies = caller.get_batch()
        saver.save_batch(vacancies)
