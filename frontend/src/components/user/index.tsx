import * as React from 'react';

import { Query } from 'react-apollo';

import USER from './query.graphql';

type User = {
  name: string;
};

type Props = {
  children: (user: User) => React.ReactNode;
};

export const User = (props: Props) => (
  <Query query={USER}>
    {({ loading, error, data }) => {
      if (loading) return 'Loading...';
      if (error) return `Error! ${error.message}`;

      return props.children(data.user);
    }}
  </Query>
);
