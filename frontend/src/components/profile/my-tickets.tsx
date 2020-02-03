/** @jsxRuntime classic */
/** @jsx jsx */
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Grid, Heading, jsx } from "theme-ui";

import { MyProfileQuery } from "~/types";

import { Link } from "../link";

type Props = {
  className?: string;
  tickets: MyProfileQuery["me"]["tickets"];
};

const Head: React.FC<{ className?: string }> = ({ children, className }) => (
  <Box
    className={className}
    sx={{
      fontWeight: "bold",
      color: "orange",
      textTransform: "uppercase",
      pb: 3,
    }}
  >
    {children}
  </Box>
);

const Content: React.SFC = ({ children }) => (
  <Box
    sx={{
      py: 3,
      borderTop: "primary",
    }}
  >
    {children}
  </Box>
);

export const MyTickets: React.SFC<Props> = ({ className, tickets }) => (
  <Box className={className}>
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
      }}
    >
      <Heading mb={4} as="h2" sx={{ fontSize: 5 }}>
        <FormattedMessage id="profile.myTicketsHeader" />
      </Heading>

      <Grid
        sx={{
          gridTemplateColumns: "1fr 1fr 1fr",
          gridColumnGap: 0,
          gridRowGap: 0,
        }}
      >
        <Head>Ticket</Head>
        <Head
          sx={{
            gridColumn: "2/4",
          }}
        >
          Attendee name
        </Head>

        {tickets.map((ticket) => (
          <Fragment key={ticket.id}>
            <Content>{ticket.ticketName}</Content>
            <Content>{ticket.attendeeName}</Content>
            <Content>
              <Link
                path={`/[lang]/profile/ticket/[ticketId]/`}
                params={{
                  ticketId: ticket.id,
                }}
              >
                <FormattedMessage id="profile.manageTicket" />
              </Link>
            </Content>
          </Fragment>
        ))}
      </Grid>
    </Box>
  </Box>
);
