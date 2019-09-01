# PyCon Italia frontend

The frontend is using Gatsby, React and TypeScript, the site will be partially static,
all the conference information eg, schedule, talks and speakers will be fetched
at build time, other information, such as current user profile will be loaded via
javascript on the client side.

## Install and run frontend

To install the frontend dependencies make you sure you have yarn installed, then run the
following commands in the frontend directory:

    yarn install

This will install all the dependencies (including dev ones).

Currenly you need to have the backend running to start the frontend, we will change
this in future, but for now make sure you follow the [backend README](../backend/README.md) to set it up.

To run the development command use:

    yarn start

This will start the Gatsby server and fetch the data from the backend,
when the data fetching is done you should be able to go to

http://localhost:4000

And see the frontend.

## Codegen

We are using TypeScript and also making use of the GraphQL schema to
generate types from the GraphQL queries we are running. The generated types
are not stored on git, they are always generated when needed. To run the
code generation run the following command:

    yarn codegen

This will create the types based on the queries done on the frontend.
