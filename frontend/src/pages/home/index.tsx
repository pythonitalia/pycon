import * as React from 'react';
import { RouteComponentProps } from '@reach/router';

import { Query } from 'react-apollo';

import { Home as HomeType, HomeVariables } from './types/Home';

import HOME from './query.graphql';

export const Home = (props: RouteComponentProps) => {
  return (
    <Query<HomeType, HomeVariables> query={HOME} variables={{ conf: 'pp18' }}>
      {({ loading, error, data }) => {
        if (loading) {
          return <div>Loading</div>;
        }

        if (error) {
          return <div>Unable to fetch the data: {error}</div>;
        }

        return (
          <div>
            <h1>{data.conference.name}</h1>
            Begins at {data.conference.start} and ends at {data.conference.end}
            <h2>Tickets</h2>
            <ul>
              {data.conference.tickets.map(ticket => (
                <li key={ticket.name}>
                  {ticket.name} - {ticket.price}
                </li>
              ))}
            </ul>
          </div>
        );
      }}
    </Query>
  );
};
