<div align="center">

<img src="https://raw.githubusercontent.com/jakebrehm/manymiles/master/img/banner.png" alt="ManyMiles Banner" style="width: 400px;"/>

<br>

<h1>Keep track of your mileage.</h1>

<br>

<a href="https://github.com/jakebrehm/manymiles"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/jakebrehm/manymiles?color=blue&logo=Git&logoColor=white&style=for-the-badge"></a>
<a href="https://raw.githubusercontent.com/jakebrehm/manymiles/master/license.txt"><img alt="GitHub license" src="https://img.shields.io/github/license/jakebrehm/manymiles?color=blue&style=for-the-badge"></a>
<a href="https://railway.app/"><img src="https://img.shields.io/badge/Hosted%20on-Railway-blue?style=for-the-badge&logo=Railway&logoColor=white" alt="Hosted on Railway"></img></a>

<br>
</div>

<p align="center">
    <a href="https://manymiles.app/"><strong>ManyMiles</strong></a> is a minimalistic website that teaches you about your driving habits.
</p>

<img src="https://raw.githubusercontent.com/jakebrehm/manymiles/master/img/divider.png" alt="ManyMiles Section Divider" style="width: 100%;"/>

## Table of contents

* [Main features](#main-features)
* [Getting set up](#getting-set-up)
* [API documentation](#api-documentation)
* [Future improvements](#future-improvements)
* [Contributors](#contributors)
* [Acknowledgements](#acknowledgements)

<img src="https://raw.githubusercontent.com/jakebrehm/manymiles/master/img/divider.png" alt="ManyMiles Section Divider" style="width: 100%;"/>

<img src="https://raw.githubusercontent.com/jakebrehm/manymiles/master/img/demo-border.gif" alt="ManyMiles Demo GIF" style="width: 100%;"/>

## Main features

- Create secure user accounts, with the ability to delete them as well
- Track their driving habits using a sleek, responsive interface
- Download their records to a csv file for storage and analysis
- Learn about their driving habits via metrics and visualizations
- Interact with their data from anywhere using an API

## Getting set up

The source code can be viewed on Github [here](https://github.com/jakebrehm/manymiles). Keep in mind that **ManyMiles** was not built with the intention of being run locally, so there are a few hoops to jump through if you want to do so.

Before you start, you're going to need to have a local instance of MySQL installed on your machine. I recommend using [MySQL Workbench](https://dev.mysql.com/downloads/workbench/), although I won't be going into too much detail about how to work with it here.

### Cloning the repository

The first step to setting up a local version of **ManyMiles** is to clone this repository. To do this, open a command line instance and change your working directory to the directory you'd like to clone the repository to.

```bash
cd path/to/clone/repository/to
```

Then, use the following command to clone the repository.

```
git clone https://github.com/jakebrehm/manymiles.git
```

Once that's done, change your working directory to the directory you just cloned.

```bash
cd manymiles
```

### Creating the virtual environment

Optionally, create a virtual environment to run the project in.

```
python3 -m venv env
```

If you chose to create the virtual environment, you need to activate it using `source env/bin/activate` (Unix) or `.\env\Scripts\activate` (Windows). You can deactivate the environment using `deactivate` whenever you'd like.

### Installing dependencies

Now you can install all of the dependencies required to properly get **ManyMiles** up and running.

```
pip3 install -r requirements.txt
```

### Creating the database

Next, you'll need to actually create a database in MySQL, which is relatively simple if you run this query in MySQL Workbench. We can call the database `manymiles`.

```sql
CREATE DATABASE `manymiles`;
```

Then, you'll need to grab the host, port, username, and password in order to create the connection string, which should have the following format for our purposes. Replace the values in brackets with the appropriate values (get rid of the brackets too).

```
mysql+pymysql://{username}:{password}@{host}:{port}/{database}
```

You'll add this connection string to the configuration file in the following steps.


### Write the configuration file

There is a file in the `cfg` directory named `.env.example` that is intended to be a template for your configuration file. Create a copy of this file, rename it to `.env`, and open it in a text editor.

Two of the configuration variables are already filled in for you. You *do not* need to change these unless you have a good reason to do so.
- `MM_FLASK_DEBUG` tells the application whether or not to run in debug mode (`True`/`False`).
- `PORT` is an environmental variable used by Flask to determine what port to host the application on.

The other two variables, however, you *do* need to change.
- `MM_FLASK_SECRET` is the value that Flask uses to protect the user session. This should ideally be a lengthy and completely random string.
- `MM_DATABASE_URI` is the connection string that you constructed in [Creating the database](#creating-the-database).


### Initialize the database

```bash
python3 create.py
```


### Run the application

Now you should finally be able to use the following command to run **ManyMiles** locally.

```
python3 app.py
```

## API documentation

**ManyMiles** features an API that allows users to perform operations such as add a new record or delete their most recent record. The main documentation lives [here](https://docs.manymiles.app), but you can also view the [Swagger UI](https://manymiles.app/api/docs) version as well.

### Siri shortcuts

A few Siri Shortcuts are available for iOS and MacOS devices to make recording your mileage and interacting with your data as painless as possible. Once you've set up the shortcuts in your Shortcuts app, you should be able to use the following voice commands with Siri:
- ["Let's record my mileage"](https://www.icloud.com/shortcuts/b931a703983349c18b90ab9bf52cd695)
- ["What was my last record?"](https://www.icloud.com/shortcuts/d59656250b4847b9af0cb4dd9de11858)
- ["Delete my last record"](https://www.icloud.com/shortcuts/c3129bd6cad64d8780a7cca88606a7a4)

## Database schema

For anyone curious, an entity relationship diagram for the database is included below.

<img src="https://raw.githubusercontent.com/jakebrehm/manymiles/master/img/er-diagram.png" alt="ManyMiles ER Diagram" style="width: 100%;"/>

## Future improvements

- Create a demo for prospective users
- Allow users to reset their password via email
- Provide more metrics and visualizations
- Set up an admin dashboard
- Incorporate extensive unit testing

<img src="https://raw.githubusercontent.com/jakebrehm/manymiles/master/img/divider.png" alt="ManyMiles Section Divider" style="width: 100%;"/>

## Contributors

- **Jake Brehm** - *main developer* - [Email](mailto:mail@jakebrehm.com) | [Github](http://github.com/jakebrehm) | [LinkedIn](http://linkedin.com/in/jacobbrehm)

## Acknowledgements

Thank you to [Muhammad Haroon](https://www.fiverr.com/haroonnaeem) for designing the **ManyMiles** logo.