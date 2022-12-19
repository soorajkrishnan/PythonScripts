# **Flask Project Initialization Script**

This script initializes a new Flask project with the following structure:
```
project_name
├── application.py
├── config.py
├── db.py
├── requirements.txt
├── templates
├── static
└── modules
```

The **`application.py`** file contains the base Flask application code, including the initialization of the Flask app, the configuration, the SQLAlchemy database, the CORS headers, and the Swagger documentation.

The **`config.py`** file contains the configuration for the Flask app, including the settings for the OpenAPI (Swagger) documentation, and the database credentials.

The **`db.py`** file is meant to be used to define the models for the database.

The **`requirements.txt`** file lists the required Python packages to run the Flask app.

The **`templates`** directory is meant to contain the HTML templates for the app.

The **`modules`** directory is meant to contain subdirectories for each module in the app.

## **Usage**

To use this script, run the following command:

```
usage: flask_setup.py [-h] [--init INIT] [--remove REMOVE] [--module MODULES [MODULES ...]] [--path PATH]

This script creates a scalable flask folder structure

optional arguments:
  -h, --help            show this help message and exit
  --init INIT, -i INIT  Initialize a directory with the given name
  --remove REMOVE, -r REMOVE
                        Remove the directory with the given name
  --module MODULES [MODULES ...], -m MODULES [MODULES ...]
                        Create sub-directories within the directory initialized with the given name
  --path PATH, -p PATH  Path of the directory

```

Replace **`project_name`** with the desired name for the project, and **`[module_1]`**, **`[module_2]`**, etc. with the names of the modules you want to include in the project. If no modules are specified, the script will create an empty project with just the base files.

## **Example**

To create a new Flask project with the name "my_project" and two modules, "users" and "products", run the following command:

```
python flask_setup.py -i my_project -m users products

```

This will create a new directory called "my_project" with the following structure:

```

my_project
├── application.py
├── config.py
├── db.py
├── requirements.txt
├── templates
├── static
└── modules
    ├── users
    │   └── users.py
    └── products
        └── products.py

```
