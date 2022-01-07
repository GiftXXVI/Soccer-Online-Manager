import os
import decimal


def get_db_uri():
    if os.getenv('APP_MODE') == 'LIVE':
        db_conf_name = os.getenv('LIVEDB_NAME')
        db_conf_user = os.getenv('LIVEDB_USER')
        db_conf_pass = os.getenv('LIVEDB_PASS')
        db_conf_host = os.getenv('LIVEDB_HOST')
        db_conf_port = os.getenv('LIVEDB_PORT')
        db_credentials = f'{db_conf_user}:{db_conf_pass}'
        db_socket = f'{db_conf_host}:{db_conf_port}'
        db_url = f'postgresql://{db_credentials}@{db_socket}/{db_conf_name}'
        return db_url
    else:
        test_conf_name = os.getenv('TESTDB_NAME')
        test_conf_user = os.getenv('TESTDB_USER')
        test_conf_pass = os.getenv('TESTDB_PASS')
        test_conf_host = os.getenv('TESTDB_HOST')
        test_conf_port = os.getenv('TESTDB_PORT')
        test_credentials = f'{test_conf_user}:{test_conf_pass}'
        test_socket = f'{test_conf_host}:{test_conf_port}'
        test_url = f'postgresql://{test_credentials}@{test_socket}/{test_conf_name}'
        return test_url


def get_app_settings():
    setup = dict()
    try:
        setup['INIT_PLAYER_VALUE'] = decimal.Decimal(os.getenv('INIT_PLAYER_VALUE'))
        setup['INIT_TEAM_BUDGET'] = decimal.Decimal(os.getenv('INIT_TEAM_BUDGET'))
    except decimal.DecimalException:
        setup['INIT_PLAYER_VALUE'] = decimal.Decimal(1000000)
        setup['INIT_TEAM_BUDGET'] = decimal.Decimal(5000000)
    return setup
