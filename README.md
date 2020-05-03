<p align="center">
    <img src="https://avatars1.githubusercontent.com/u/3573467?s=96" alt="Python Italia Logo" />
</p>

# PyCon Italia website

> The monorepo for the new PyCon Italia website, based on Django, Strawberry,
> Gatsby and React.

## How to setup - quick

We are using [pyinvoke](http://docs.pyinvoke.org/en/1.3/) to run tasks (it is an
alternative to make files). Top install it we recommend to use
[pipx](https://github.com/pipxproject/pipx), with this command

    pipx install invoke

this will install globally invoke (in a separate environment, but you can use pip if you don't want to use pipx). 
To run the setup, run the following command:

    invoke setup

## How to setup - extended

This project is composed of two services, a backend and a frontend.

Follow the [README in the backend service](./backend/README.md) to setup the
backend.

Note:

Currently in order to run the frontend you also need the backend up and running,
we will, in future, provide a staging environment that can be used for
development, without you having to setup the backend as well.

Follow the [README in the frontend service](./frontend/README.md) to setup the
frontend.
