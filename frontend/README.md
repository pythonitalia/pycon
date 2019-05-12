# PyCon Frontend

## 1. Install the dependencies

Steps:
* Install the dependencies running `yarn install`

## 2. Download the schema

__WARNING__ - this is mandatory and must be executed in these cases:
* Setting up the project for the first time
* Every time the backend service's schema gets changed and it needs to be updated

Steps:
* Update the information about the endpoint for the schema inside the `apollo.config.js` file
* Make sure the backend server is reachable (or start it if using a local environment)
* Run the `yarn run graphql-schema` command to download the schema

## 3. Start the project

Steps:
* Run the `yarn start` command