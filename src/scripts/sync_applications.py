import xmlrpc.client
import logging
from typing import NoReturn

import src.scripts.odoo as odoo
import src.scripts.cabinet as cabinet
import src.config as config


def sync_applications() -> NoReturn:
    """
    Adds new applications in Odoo if they exist
    :return: NoReturn
    """

    models = xmlrpc.client.ServerProxy(f'{config.SYSTEM_PARAMS["url"]}/xmlrpc/2/object')

    if len(config.PROJECT_NUMBERS) == 0:
        config.PROJECT_NUMBERS = cabinet.get_all_project_numbers()

    for project_number in config.PROJECT_NUMBERS:
        project_id = cabinet.get_project_id_by_number(project_number)

        odoo_recruiter_id = odoo.get_odoo_recruiter_id(
            models,
            cabinet.get_recruiter_email(project_id)
        )

        odoo_project_id = odoo.get_odoo_project_id(models, project_number)

        for role_name, email, name, comment in cabinet.get_applications(project_id):
            if len(name.split()) == 3:
                name = ' '.join(name.split()[:-1])

            odoo.create_odoo_application(
                models,
                {'name': name, 'email': email,
                 'role_name': role_name,
                 'odoo_job': config.SYSTEM_PARAMS["odoo_job"],
                 'odoo_recruiter_id': odoo_recruiter_id,
                 'comment': comment,
                 'odoo_project_id': odoo_project_id
                 }
            )

    logging.info('Application fetch done')
