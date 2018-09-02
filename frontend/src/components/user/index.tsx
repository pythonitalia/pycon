import * as React from 'react';

import { Query } from 'react-apollo';

import { User as UserQuery, User_me } from './types/User';

import USER from './query.graphql';

type Props = {
  children: (user: User_me) => React.ReactNode;
};

export const User = (props: Props) => (
  <Query<UserQuery> query={USER}>
    {({ loading, error, data }) => {
      if (loading) return 'Loading...';
      if (error) return `Error! ${error.message}`;

      return props.children(data.me!);
    }}
  </Query>
);
