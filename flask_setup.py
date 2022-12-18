import argparse
import os
import shutil
import subprocess
import pkg_resources


APP_BASE = """
import os
from flask import Flask
from config import get_config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)

app.config.from_object(get_config(os.getenv('ENV')))

CORS(app)
db = SQLAlchemy(app)
swagger = Swagger(app)

if __name__ == "__main__":
    app.run()
"""

CONTENT = ''


CONFIG_BASE = r"""import os

class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-is-a-secret'

    # OpenAPI (Swagger) configuration
    SWAGGER = {
        'title': '',
        'description': '',
        'uiversion': 3
    }
    
    # Retrieve database credentials from environment variables
    username = os.getenv('DB_USERNAME', 'default_username')
    password = os.getenv('DB_PASSWORD', 'default_password')
    hostname = os.getenv('DB_HOSTNAME', 'localhost')
    database_name = os.getenv('DB_NAME', 'database_name')

    # Construct SQLAlchemy URL with placeholders
    SQLALCHEMY_DATABASE_URI = 'postgresql://{username}:{password}@{hostname}/{database_name}'.format(
        username=username,
        password=password,
        hostname=hostname,
        database_name=database_name
    )

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config_by_name = dict(
    local=DevelopmentConfig,
    dev=DevelopmentConfig,
    qa=StagingConfig,
    prod=ProductionConfig,
    test=TestingConfig
)

def get_config(env):
    return config_by_name[env]



"""

REQ_BASE="""
psycopg2
flask
Flask-Cors
Flask-SQLAlchemy  
flasgger 
"""


def init_project(project_name, modules=[]):
    # Create project root directory
    root_dir = f"{project_name}"
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
        print(f"Created {project_name} folder")

    # Create application.py file
    application_file = f"{root_dir}/application.py"
    if not os.path.exists(application_file):
        with open(application_file, "w") as f:
            f.write(APP_BASE)
        print(f"Created application.py file")
    # Create db.py file
    db_file = f"{root_dir}/db.py"
    if not os.path.exists(db_file):
        with open(db_file, "w") as f:
            f.write("# Flask project database file")

    # Create config.py file
    config_file = f"{root_dir}/config.py"
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            f.write(CONFIG_BASE)
        print(f"Created config.py file")

    # Create templates directory
    template_dir = f"{root_dir}/templates"
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
        print(f"Created templates folder")

    # Create modules directory inside templates

    # Create modules directory
    modules_dir = f"{root_dir}/modules"
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)
        print(f"Created modules folder")

    # Iterate over the modules and create them in the given directory
    for module in modules:
        module_dir = f"{modules_dir}/{module}"
        if not os.path.exists(module_dir):
            os.makedirs(module_dir)
            with open(f'{module_dir}/{module}.py','w') as f:
                f.write("from flask import Blueprint")
                f.write('\n')
                f.write(f"{module}_bp = Blueprint('{module}', __name__,url_prefix='{module}')")
            
            print(f"Created {module} folder")

        template_dirs = f"{template_dir}/{module}"
        if not os.path.exists(template_dirs):
            os.makedirs(template_dirs)

    # Create static directory
    static_dir = f"{root_dir}/static"
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        print(f"Created static folder")

    # Add blueprints to application.py
    with open(application_file, "r") as f:
        # Read the file into a list of lines
        lines = f.readlines()

    # Check if the lines are not already present in the file
    lines_present = all(any(line.strip() == f"from modules.{module} import {module}_bp" for line in lines) and
                        any(line.strip() == f"app.register_blueprint({module}_bp)" for line in lines)
                        for module in modules)

    # If the lines are not present, add them to the file
    if not lines_present:
        with open(application_file, "a") as f:
            f.write("\n")
            for module in modules:
                f.write(f"from modules.{module} import {module}_bp\n")
                f.write(f"app.register_blueprint({module}_bp)\n")
                print(f"Added {module} blueprint to application.py file")



def remove_project(directory):
    """
    Remove a directory and all its contents.

    Parameters:
        directory (str): The path of the directory to be removed.

    Returns:
        None
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        raise ValueError(f"Error: directory {directory} does not exist")
    else:
        # Confirm with the user before deleting the directory
        confirm = input(
            f"Are you sure you want to delete the directory {directory} and all its contents? [y/N] "
        )
        if confirm.lower() == "y" or confirm.lower() == "yes":
            shutil.rmtree(directory)
            print(f"Directory {directory} successfully deleted")
        else:
            print(f"Directory {directory} was not deleted")


def create_utility_files(project_name):
    # Create project root directory
    util_file = f"{project_name}/.gitignore"
    req_file = f"{project_name}/requirements.txt"
    with open(util_file, 'w') as f:
        f.write(CONTENT)
        f.write(f"{project_name}")

    with open(req_file, 'w') as f:
        f.write(REQ_BASE)


def main():
    try:
        
        # Create an ArgumentParser object
        parser = argparse.ArgumentParser(
            description="This script creates a scalable flask folder structure")
        # Add the init, remove, and module arguments
        parser.add_argument(
            "--init", "-i", dest="init", help="Initialize a directory with the given name"
        )
        parser.add_argument(
            "--remove", "-r", dest="remove", help="Remove the directory with the given name"
        )
        parser.add_argument(
            "--module",
            "-m",
            dest="modules",
            nargs="+",
            help="Create sub-directories within the directory initialized with the given name",
        )
        parser.add_argument(
            "--path", "-p", default="./", dest="path", help="Path of the directory"
        )

        # Parse the arguments
        args = parser.parse_args()
        # Check if the init argument is present
        project_path=''
        if args.init:
            # Call the initialize_directory function with the given directory name
            project_path = os.path.join(args.path, args.init)
            init_project(project_path)
            create_utility_files(project_path)

        # Check if the remove argument is present
        if args.remove:
            # Call the remove_project function with the given directory name
            if args.modules is not None:
                for i in args.modules:  
                    module_path=os.path.join(args.remove,'modules',i)                  
                    remove_project(module_path)
            else:
                remove_project(args.remove)

        # Check if the module argument is present
        if args.modules:
            # Get the directory name from the init argument
            directory = args.init

            # Check if the directory exists
            if not os.path.exists(directory):
                print(f"Error: directory {directory} does not exist")
            else:
                init_project(args.init, args.modules)
        try:
            pkg_resources.get_distribution('black')
        except pkg_resources.DistributionNotFound as error:
            subprocess.run(['pip','install', 'black'], stdout=subprocess.DEVNULL)
        if project_path!='':
            subprocess.run(['python','-m', 'black',f'{project_path}'], stdout=subprocess.DEVNULL)
         
    except Exception as error:
        print(error)
        exit(0)


if __name__ == "__main__":
    main()