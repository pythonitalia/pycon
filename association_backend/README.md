# PyCon Italia Association Microservice

The Association Microservice is using Django and Strawberry to provide a GraphQL API. The
requirements are handled by [pip-tools](https://github.com/jazzband/pip-tools).
N.B. You have to install virtualenv by your own!


### Install and run backend


To install make you sure you have poetry and invoke installed, elsewhere install it

    poetry install

    invoke install

This will update your virtual environment and install all the dependencies.

Then initialiaze .env file

    invoke init_env

and modify your .env file to customize configurations

To make sure everything went fine you can run the tests:

    invoke tests

`poetry run` will run the command inside the virtual environment, without you
having to manually activate it.

To run the backend you can use the demodata we are providing, but first let's
run the migration so our db is created:

    invoke migrate

One last step before running the server, let's create a superuser so we can
access the admin:

    invoke createsuperuser

And follow the steps. Once that's done we can run the dev server by running:

    invoke server

To check if the server is up:

http://localhost:8000/

And for the admin go to:

http://localhost:8000/admin

You should be able to login with the user we create a few moments ago.
