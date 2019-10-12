import React from "react";
import styled from "styled-components";

import { TicketFare } from "../../generated/graphql-backend";
import { Cart } from "./index";

type Props = {
  cart: Cart;
  updateCart: (cart: Cart) => void;
  tickets: ({ __typename?: "TicketFare" } & Pick<
    TicketFare,
    "name" | "code" | "price" | "id"
  >)[];
};

const TicketCard = styled.div`
  width: 14rem;
  height: 6rem;

  display: inline-flex;
  flex-direction: column;

  margin: 0.5rem;
  padding: 1rem;

  border-radius: 0.5rem;

  background: #fff;

  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);

  p {
    margin: 0;
  }
`;

const BottomWrapper = styled.div`
  display: flex;
  align-items: center;

  margin: auto 0 0 0;

  select {
    min-width: 5rem;
    margin-left: 1rem;
  }
`;

const Container = styled.div`
  display: flex;
  flex-wrap: wrap;

  margin: 0 -0.5rem;
`;

export const Tickets: React.SFC<Props> = ({ tickets, updateCart, cart }) => {
  const total = Object.entries(cart).reduce(
    (p, [id, quantity]) =>
      p + parseFloat(tickets.find(t => t.id === id)!.price) * quantity,
    0,
  );
  return (
    <Container>
      {tickets.map(ticket => (
        <TicketCard key={ticket.code}>
          <p>{ticket.name}</p>
          <BottomWrapper>
            <p>{ticket.price}€ x</p>
            <select
              value={cart[ticket.id]}
              onChange={e => {
                const newCart = { ...cart };
                newCart[ticket.id] = parseInt(
                  e.target.selectedOptions[0].value,
                  10,
                );
                updateCart(newCart);
              }}
            >
              <option value="0">0</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
          </BottomWrapper>
        </TicketCard>
      ))}
    </Container>
  );
};
