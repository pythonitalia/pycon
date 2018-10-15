import * as React from 'react';
import { RouteComponentProps } from '@reach/router';
import { Query } from 'react-apollo';

import { UserDetail } from './types/UserDetail';

import USER_DETAIL from './query.graphql';

import { Card } from '~/components/card/index';

type Props = RouteComponentProps & {
  id: number;
};

export class Member extends React.Component<Props, {}> {
  public render() {
    return (
      <Query<UserDetail>
        query={USER_DETAIL}
        variables={{
          id: this.props.id,
        }}
      >
        {({ loading, error, data }) => {
          if (loading) {
            return <Card>Please wait</Card>;
          }

          if (error) {
            return (
              <Card>
                Unable to fetch user ID {this.props.id}: {error.message}
              </Card>
            );
          }

          return (
            <Card title={`User ${data.user.email}`}>
              <ul>
                <li>
                  <strong>ID</strong>: {data.user.id}
                </li>
                <li>
                  <strong>Email</strong>: {data.user.email}
                </li>
              </ul>
            </Card>
          );
        }}
      </Query>
    );
  }
}
