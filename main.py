import logging

import src.config
import src.logger

from src.scripts.odoo_auth import auth
from src.scripts.sync_applications import sync_applications


def main() -> None:
    """
    Main function
    :return: None
    """

    logging.info('==== Start ====')

    src.config.init_config_settings()
    user_id = auth()

    if user_id:
        try:
            sync_applications()
        except Exception as e:
            logging.error(e)

    logging.info('==== Finish ====\n')


if __name__ == '__main__':
    main()
