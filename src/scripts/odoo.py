import logging

from typing import NoReturn

import src.config as config


def get_odoo_project_id(models: object, project_number: int) -> int:
    """
    Gets project id in Odoo by its number
    :param models:
    :param project_number:
    :return: project id in odoo
    """
    return models.execute_kw(
        config.SYSTEM_PARAMS["odoo_db"], config.SYSTEM_PARAMS["user_id"], config.SYSTEM_PARAMS["odoo_password"],
        'project.project', 'search_read', [[['x_project_number', '=', project_number]]],
        {'fields': ['id'], 'limit': 1}
    )[0]['id']


def get_odoo_recruiter_id(models: object, recruiter_email: str) -> int:
    """
    Gets recruiter id in Odoo by its name
    :param models:
    :param recruiter_email:
    :return: recruiter id in Odoo
    """
    alt_email = recruiter_email.split('@')[0] + '@' + {'miem.hse.ru': 'edu.hse.ru',
                                                 'edu.hse.ru': 'miem.hse.ru'}[recruiter_email.split('@')[1]]
    return models.execute_kw(
        config.SYSTEM_PARAMS["odoo_db"], config.SYSTEM_PARAMS["user_id"], config.SYSTEM_PARAMS["odoo_password"],
        'res.users', 'search_read', [['|', ['login', '=', recruiter_email], ['login', '=', alt_email]]],
        {'fields': ['id'], 'limit': 1}
    )[0]['id']


def get_odoo_role_id(models: object, role_name: str) -> int:
    """
    Gets role id Odoo by its name
    :param models:
    :param role_name:
    :return: role id in Odoo
    """
    if len(role := models.execute_kw(
            config.SYSTEM_PARAMS["odoo_db"], config.SYSTEM_PARAMS["user_id"], config.SYSTEM_PARAMS["odoo_password"],
            'project.role', 'search_read', [[['name', '=', role_name]]],
            {'fields': ['id'], 'limit': 1}
    )) == 0:
        logging.info(f'Created vacancy {role_name}')

        return models.execute_kw(
            config.SYSTEM_PARAMS["odoo_db"], config.SYSTEM_PARAMS["user_id"], config.SYSTEM_PARAMS["odoo_password"],
            'project.role', 'create', [{'company_id': 1, 'name': role_name}]
        )
    else:
        return role[0]['id']


def get_odoo_job_id(models: object, job_name: str) -> int:
    """
    Gets job id in Odoo by its name
    :param models:
    :param job_name:
    :return: job id in Odoo
    """
    return models.execute_kw(
        config.SYSTEM_PARAMS["odoo_db"], config.SYSTEM_PARAMS["user_id"], config.SYSTEM_PARAMS["odoo_password"],
        'hr.job', 'search_read', [[['name', '=', job_name]]],
        {'fields': ['id'], 'limit': 1}
    )[0]['id']


def create_odoo_application(models: object, user_data: dict) -> NoReturn:
    """
    Creates application if it does not exist yet
    :param models:
    :param user_data:
    :return: NoReturn
    """
    if len(models.execute_kw(
            config.SYSTEM_PARAMS["odoo_db"], config.SYSTEM_PARAMS["user_id"], config.SYSTEM_PARAMS["odoo_password"],
            'hr.applicant', 'search_read',
            [['&', ['email_from', '=', user_data["email"]],
              ['x_specialization', 'in', [user_data["role_name"], False]],
              ['job_id', '=', get_odoo_job_id(models, user_data["odoo_job"])],
              ['x_project', 'in', [user_data["odoo_project_id"], False]]]],
            {'fields': ['id'], 'limit': 1}
    )) == 0:
        models.execute_kw(
            config.SYSTEM_PARAMS["odoo_db"], config.SYSTEM_PARAMS["user_id"], config.SYSTEM_PARAMS["odoo_password"],
            'hr.applicant', 'create', [{'name': user_data["name"], 'email_from': user_data["email"],
                                        'x_specialization': user_data["role_name"],
                                        'job_id': get_odoo_job_id(models, user_data["odoo_job"]),
                                        'user_id': user_data["odoo_recruiter_id"],
                                        'description': user_data["comment"],
                                        'x_project': user_data["odoo_project_id"]
                                        }]
        )

        logging.info(f'Added user {user_data["email"]} for vacancy {user_data["role_name"]}')
