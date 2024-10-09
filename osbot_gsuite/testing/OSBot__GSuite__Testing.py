from osbot_utils.utils.Env import get_env, load_dotenv

from osbot_utils.base_classes.Type_Safe import Type_Safe

ENV_NAME__GDRIVE__TEMP_FOLDER = 'GDRIVE__TEMP_FOLDER'


class OSBot__GSuite__Testing(Type_Safe):

    def __init__(self):
        load_dotenv()
        super().__init__()

    def gdrive_temp_folder(self):
        value = get_env(ENV_NAME__GDRIVE__TEMP_FOLDER)
        if value:
            return value
        raise ValueError(f"[OSBot__GSuite__Testing] no value found for gdrive_temp_folder, looked in env var: {ENV_NAME__GDRIVE__TEMP_FOLDER}")


osbot_gsuite_testing = OSBot__GSuite__Testing()