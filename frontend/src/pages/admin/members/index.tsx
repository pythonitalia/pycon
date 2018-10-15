import * as React from 'react';
import { RouteComponentProps } from '@reach/router';

import { Query } from 'react-apollo';

import { Card } from '~/components/card/index';
import { Table, ColumnHeader } from '~/components/table/index';
import { Pagination } from '~/components/pagination/index';

import { Users, Users_users_objects } from './types/Users';

import USERS from './query.graphql';

const USERS_PER_PAGE = 20;

const COLUMNS: Array<ColumnHeader<Users_users_objects>> = [
  { label: 'ID', accessor: 'id' },
  { label: 'Email', accessor: 'email' },
  {
    label: 'Data joined',
    accessor: (obj: Users_users_objects): string =>
      new Date(obj.dateJoined).toLocaleDateString(),
  },
];

export class Members extends React.Component<RouteComponentProps, {}> {
  constructor(props: RouteComponentProps) {
    super(props);

    this.onPageChange = this.onPageChange.bind(this);
    this.onUserClick = this.onUserClick.bind(this);
  }

  private onPageChange(nextPage: number) {
    this.props.navigate(`/admin/members/?page=${nextPage + 1}`);
  }

  private onUserClick(
    user: Users_users_objects,
    e: React.MouseEvent<HTMLTableRowElement>,
  ) {
    this.props.navigate(`/admin/members/${user.id}`);
  }

  private getCurrentPage() {
    const searchParams = new URLSearchParams(this.props.location.search);
    const page = parseInt(searchParams.get('page'), 10) || 1;
    return Math.max(page - 1, 0);
  }

  public render() {
    const currentPage = this.getCurrentPage();

    return (
      <Query<Users>
        query={USERS}
        variables={{
          offset: currentPage * USERS_PER_PAGE,
          limit: USERS_PER_PAGE,
        }}
      >
        {({ loading, error, data }) => {
          const title =
            !loading && !error
              ? `Members (${data.users.totalCount})`
              : 'Members';

          return (
            <Card title={title}>
              {error && `Something went wrong while loading the users`}
              {!loading &&
                !error && (
                  <>
                    <Table<Users_users_objects>
                      columns={COLUMNS}
                      data={data.users.objects}
                      onRowClick={this.onUserClick}
                    />
                    <Pagination
                      onPageChange={this.onPageChange}
                      currentPage={currentPage}
                      itemsPerPage={USERS_PER_PAGE}
                      totalItems={data.users.totalCount}
                    />
                  </>
                )}
            </Card>
          );
        }}
      </Query>
    );
  }
}
