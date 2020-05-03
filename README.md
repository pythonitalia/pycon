<p align="center">
    <img src="https://avatars1.githubusercontent.com/u/3573467?s=96" alt="Python Italia Logo" />
</p>

# PyCon Italia website

> The monorepo for the new PyCon Italia website, based on Django, Strawberry,
> Gatsby and React.

## How to setup

We are using [pyinvoke](http://docs.pyinvoke.org/en/1.3/) to run tasks (it is an
alternative to make files) 
To install it we recommend to use [pipx](https://github.com/pipxproject/pipx)
    
    pipx install invoke


This project is composed of two services, a backend and a frontend.

Follow the [README in the backend service](./backend/README.md) to setup and run the
backend.

Note:  
    
   

Currently in order to run the frontend you also need the backend up and running,
we will, in future, provide a staging environment that can be used for
development, without you having to setup the backend as well.

Follow the [README in the frontend service](./frontend/README.md) to setup and run the
frontend.



Run the following command:

    invoke --list
    
to know all the command you can run