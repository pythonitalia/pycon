# PyCon Italia backend

The backend is using Django and Strawberry to provide a GraphQL API. The
requirements are handled by [poetry](https://poetry.eustace.io). It will handle
the creation of the virtual environment for you.

### Install and run backend

To install the backend make you sure you have poetry installed, then run the
following command in the backend directory:

    poetry install

This will create the virtual environment and install all the dependencies
(including dev ones).

Create a `.env` file by copying the `.env.sample`, this will setup basic
environment variables for debugging.

To make sure everything went fine you can run the tests:

    poetry run pytest tests/

`poetry run` will run the command inside the virtual environment, without you
having to manually activate it.

To run the backend you can use the demodata we are providing, but first let's
run the migration so our db is created:

    poetry run python manage.py migrate

After that we can load the data:

    poetry run python manage.py loaddata demodata/*.json

This will add some dummy data that will allow you test the API and admin.

One last step before running the server, let's create a superuser so we can
access the admin:

    poetry run python manage.py createsuperuser

And follow the steps. Once that's done we can run the dev server by running:

    poetry run python manage.py runserver

To check if the API is up an running go to:

http://localhost:8000/graphql

and submitting the following query:

```gql
{
    conference(code: "pycon-demo") {
        name
    }
}
```

And for the admin go to:

http://localhost:8000/admin

You should be able to login with the user we create a few moments ago.
