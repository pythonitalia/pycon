import * as React from 'react';
import { Query } from 'react-apollo';
import { RouteComponentProps } from '@reach/router';
import { MyTickets as MyTicketsQuery, MyTickets_me_tickets } from './Types/MyTickets';

import MY_TICKETS from './query.graphql';

import * as styles from './style.css';

export const MyTickets = (props: RouteComponentProps) => {
  return <Query<MyTicketsQuery> query={MY_TICKETS}>
    {({ loading, error, data }) => {
      console.log('loading', loading, error, data)
      if (loading) {
        return <div>Hang on</div>;
      }

      if (error) {
        return <div>Something went wrong: {error}</div>
      }

      return <div className={styles.container}>
        {data.me.tickets.map(ticket => <Ticket {...ticket} />)}
      </div>;
    }}
  </Query>;
}

const Ticket = (props: MyTickets_me_tickets) => {
  return <div className={styles.ticket}>
    {props.ticketFare.name}
    <p>Paid on #{props.order.id}</p>
  </div>
}
