import os
import decimal
from random import choice


def get_db_uri() -> str:
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


def get_app_settings() -> dict:
    setup = dict()
    try:
        setup['INIT_PLAYER_VALUE'] = decimal.Decimal(
            os.getenv('INIT_PLAYER_VALUE'))
        setup['INIT_TEAM_BUDGET'] = decimal.Decimal(
            os.getenv('INIT_TEAM_BUDGET'))
    except decimal.DecimalException:
        setup['INIT_PLAYER_VALUE'] = decimal.Decimal(1000000)
        setup['INIT_TEAM_BUDGET'] = decimal.Decimal(5000000)
    return setup


def get_firstname() -> list:
    firstnames = ['James', 'Jack', 'Harry', 'Jacob', 'Charles', 'Thomas', 'Peter', 'George', 'William', 'Joseph', 'Michael',
                  'Alexander', 'Jacques', 'Jean', 'Michel', 'Pierre', 'Jean-Baptiste', 'Antoine', 'Claude', 'Phillip', 'Frederic',
                  'Jean-Luc', 'Jean-Paul', 'Abimbola', 'Abdalla', 'Adebayo', 'Ahmed', 'Ayodele', 'Adetokunbo', 'Kgomotso'
                  'Kojo', 'Kwabena', 'Kwaku', 'Kofi', 'Kwame', 'Akwesi', 'Chiyembekezo', 'Fatsani', 'Kondwani', 'Kumbukani', 'Limbani ',
                  'Limbikani', 'Mayeso', 'Mphatso', 'Alinafe', 'Akuzike', 'Mayamiko', 'Takondwa', 'Yamikani', 'Pilirani']
    return choice(firstnames)


def get_lastname() -> str:
    lastnames = ['Martin', 'Duval', 'Leroy', 'Simon', 'Meyer', 'Muller', 'Schmitt', 'Schneider', 'Weber', 'Fischer', 'Weiss', 'Garcia'
                 'Martinez', 'Blanc', 'Fernandez', 'Lopez', 'Sanchez', 'Perez', 'Da Silva', 'Petit', 'Dos Santos', 'Ferreira', 'Rodrigues',
                 'Fernandes', 'Lambert', 'Dupont', 'Leclerc', 'Lejeune', 'Renard', 'Bouchard', 'Tremblay', 'Petit', 'Robert', 'Moreau',
                 'Silva', 'Santos', 'Sousa', 'Oliveira', 'Álvarez', 'Castro', 'Romero', 'Suárez', 'Núñez', 'Rossi', 'Méndez', 'Blanco', 'Pereyra'
                 'Medina', 'Herrera', 'Colombo', 'Peralta', 'Ledesma', 'Guzmán', 'Maldonado', 'Barbosa', 'Cardoso', 'Teixeira', 'Gonçalves',
                 'Banda', 'Phiri', 'Mwale', 'Mkandawire', 'Moyo', 'Kumwenda', 'Nyasulu', 'Ngwira', 'Msiska', 'Kachingwe', 'Chibwana', 'Milanzi', 'Sakala'
                 'Kapalamula', 'Kamwana', 'Mwenda', 'Mataka', 'Kasambala', 'Kapira', 'Kabaghe', 'Liwonde', 'Chikafa', 'Mkwanda', 'Diallo',
                 'Traore', 'Coulibaly', 'Moussa', 'Keita', 'Suleiman', 'Mwangi', 'Hamadou', 'Sene', 'Mba', 'Shaban', 'Ingabire', 'Muhumed', 'Mbatha',
                 'Mofokeng', 'Mido', 'Wang', 'Li', 'Zhang', 'Liu', 'Chen', 'Yang', 'Huang', 'Zhao', 'Wu', 'Zhou', 'Kim', 'Lee', 'Park', 'Jeong', 'Yang'
                 'Sato', 'Suzuki', 'Takahashi', 'Tanaka', 'Watanabe', 'Yamamoto', 'Nakamura', 'Ivanov', 'Kravtsov', 'Dimitrov', 'Svoboda', 'Popov',
                 'Dvořák', 'Kowalski', 'Kamiński']
    return choice(lastnames)


def get_teamsuffix() -> str:
    suffixes = ['United', 'Rovers', 'City', 'Galaxy', 'Stars', 'FC', 'CF', 'SC', 'SV', 'Eleven', 'Club', 'Lions',
                'Strikers', 'Eagles', 'Rhinos', 'Wolves', 'Bulldogs', 'Braves', 'Stallions', 'Warriors', 'Daredevils',
                'Wanderers', 'Bullets', 'Shapshooters', 'Blitz', 'Thunder', 'Crushers', 'Dragons', 'Kamikazes', 'Devils'
                'Hawks', 'Predators', 'Shockers', 'Spiders', 'Comets', 'Stingrays', 'Jets', 'Dynamo', 'Scorpions'
                'Dynamite', 'Raptors', 'Vikings', 'Knights', 'Sharks', 'Wizards', 'Pirates', 'Town', 'Aliens'
                ]
    return choice(suffixes)
