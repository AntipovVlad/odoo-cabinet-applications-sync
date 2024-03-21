import logging
import xmlrpc.client

import src.config
import src.logger


def auth() -> int | None:
    try:
        common = xmlrpc.client.ServerProxy(f'{src.config.SYSTEM_PARAMS["url"]}xmlrpc/2/common')
        user_id = common.authenticate(src.config.SYSTEM_PARAMS["odoo_db"],
                                      src.config.SYSTEM_PARAMS["odoo_username"],
                                      src.config.SYSTEM_PARAMS["odoo_password"],
                                      {})
        src.config.SYSTEM_PARAMS['user_id'] = user_id
    except xmlrpc.client.Fault:
        logging.error('Incorrect config.conf')

        return None

    return user_id
