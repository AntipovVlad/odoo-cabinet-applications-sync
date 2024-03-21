from src import consts
import requests

import src.config as config


def get_all_project_numbers() -> list:
    """
    Gets all open project numbers
    :return: list of project numbers
    """

    response = requests.get(config.CABINET_BASE_URL + consts.CABINET_ALL_PROJECTS,
                            timeout=consts.TIMEOUT).json()

    return [int(record["number"]) for record in response["data"]]


def get_project_id_by_number(project_number: int) -> int:
    """
    Gets project id by its number
    :param project_number:
    :return: project id in cabinet
    """

    response = requests.get(config.CABINET_BASE_URL + consts.CABINET_PROJECT_IDS_URL + str(project_number),
                            timeout=consts.TIMEOUT).json()

    return response['data']['id']


def get_applications(project_id: int) -> tuple:
    """
    Gathers info about users' applications
    :param project_id: id of project
    :return: role, email, name, comment
    """

    response = requests.get(config.CABINET_BASE_URL + consts.CABINET_APPLICATIONS_URL + str(project_id),
                            timeout=consts.TIMEOUT).json()

    for record in response["data"]:
        if record['leader_confirm'] + record['student_confirm'] == 0:
            yield record['role'], record['email'][0], record['name'], record['studentComment']


def get_recruiter_email(project_id: int) -> str:
    """
    Returns email of recruiter
    :param project_id: id of project
    :return: recruiter's email
    """

    response = requests.get(config.CABINET_BASE_URL + consts.CABINET_PROJECT_PARTICIPANTS_URL + str(project_id),
                            timeout=consts.TIMEOUT).json()
    if response.get('data'):
        user_email = list(filter(lambda x: not x['initiator'],
                                 response['data']['leaders']))[0]['email']
        for email in user_email:
            if 'miem' not in email:
                user_email = email
                break
    else:
        user_email = ''

    return user_email
