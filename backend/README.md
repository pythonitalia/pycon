# PyCon Italia backend

The backend is using Django and Strawberry to provide a GraphQL API. The
requirements are handled by [poetry](https://poetry.eustace.io). It will handle
the creation of the virtual environment for you.

### Install and run backend

Launching invoke setup, you have installed poetry. 
Poetry create for you the virtual environment 
and install all the dependencies (including dev ones).

To make sure everything went fine you can run the tests, in the backend directory:

    poetry run pytest tests/

`poetry run` will run the command inside the virtual environment, without you
having to manually activate it.


We are using [docker](https://www.docker.com/) to install postgres DB, so install 
and execute it.

Then in your `backend` dir create a `.env` file by copying the `.env.sample`, this will setup basic
environment variables for database creation end for debugging 


To create your postgres DB with docker, execute this command from root directory:

    invoke setup-db
    
To create DB tables, execute this command from root directory:

    invoke migrate
     
To run the backend you can use the demodata we are providing, 
execute this command from root directory:

    invoke demo-data

This will add some dummy data that will allow you test the API and admin.

One last step before running the server, let's create a superuser so we can
access the admin:

    invoke createsuperuser

And follow the steps. Once that's done we can run the dev server by running:

    invoke run-backend

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
