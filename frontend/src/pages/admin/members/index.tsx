import * as React from 'react';
import { RouteComponentProps } from '@reach/router';

import { Query } from 'react-apollo';

import { Card } from '../../../components/card/index';
import { Table, ColumnHeader } from '../../../components/table/index';
import { Pagination } from '../../../components/pagination/index';

import { Users } from './types/Users';

import USERS from './query.graphql';

const USERS_PER_PAGE = 20;

const COLUMNS: ColumnHeader[] = [
  { label: 'ID', accessor: 'id' },
  { label: 'Email', accessor: 'email' },
  {
    label: 'Data joined',
    accessor: obj => new Date(obj.dateJoined).toLocaleDateString(),
  },
];

type Props = RouteComponentProps & {
  page?: number;
};

export class Members extends React.Component<Props, {}> {
  constructor(props: RouteComponentProps) {
    super(props);

    this.onPageChange = this.onPageChange.bind(this);
  }

  private onPageChange(nextPage: number) {
    this.props.navigate(`/admin/members/${nextPage + 1}`);
  }

  private getCurrentPage() {
    if (!this.props.page) {
      return 0;
    }

    return Math.max(this.props.page - 1, 0);
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
                    <Table columns={COLUMNS} data={data.users.objects} />
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
