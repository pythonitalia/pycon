/** @jsxRuntime classic */

/** @jsx jsx */
import { useState, useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { Button } from "~/components/button/button";
import { Link } from "~/components/link";
import { Modal } from "~/components/modal";
import { Table } from "~/components/table";
import { useCurrentUser } from "~/helpers/use-current-user";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import {
  AttendeeTicket,
  useUpdateTicketMutation,
  MyProfileDocument,
} from "~/types";

import { ProductState } from "../tickets-page/types";
import { QuestionsSection } from "./questions-section";

type Props = {
  tickets: AttendeeTicket[];
};

const snakeToCamel = (str: string) => {
  return str.replace(/[^a-zA-Z0-9]+(.)/g, (m, chr) => chr.toUpperCase());
};

export const MyTickets = ({ tickets = [] }: Props) => {
  const code = process.env.conferenceCode;

  const language = useCurrentLanguage();
  const { user } = useCurrentUser({ skip: false });
  const ticketHeader = useTranslatedMessage("profile.ticketFor");
  const nameHeader = useTranslatedMessage("orderReview.attendeeName");
  const emailHeader = useTranslatedMessage("orderReview.attendeeEmail");
  const [currentTicketId, setCurrentTicketId] = useState(null);

  const headers = [ticketHeader, nameHeader, emailHeader, ""];

  return (
    <Box
      sx={{
        borderTop: "primary",
      }}
    >
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          my: 5,
          px: 3,
        }}
      >
        <Heading mb={5} as="h2" sx={{ fontSize: 5 }}>
          <FormattedMessage id="profile.myTickets" />
        </Heading>
        {tickets.length === 0 && (
          <FormattedMessage
            id="profile.myTickets.notickets"
            values={{
              email: user?.email,
              linkTicket: (
                <Link path="/tickets">
                  <FormattedMessage id="global.here" />
                </Link>
              ),
              br: <br />,
            }}
          />
        )}
        {tickets.length > 0 && (
          <Table
            headers={headers}
            mobileHeaders={headers}
            data={tickets}
            keyGetter={(item) => item.id}
            rowGetter={(item) => [
              item.item.name,
              item.name,
              item.email,
              <Box>
                <Button
                  onClick={() => setCurrentTicketId(item.id)}
                  variant="primary"
                >
                  <FormattedMessage id="profile.manageTicket" />
                </Button>
              </Box>,
            ]}
          />
        )}
        {(updatedData?.updateAttendeeTicket.__typename === "AttendeeTicket" ||
          updatedData?.updateAttendeeTicket.__typename ===
            "TicketReassigned") && (
          <Alert variant="success">
            <FormattedMessage
              id={`profile.myTickets.update.${updatedData.updateAttendeeTicket.__typename}.message`}
              values={{ email: updatedData.updateAttendeeTicket.email }}
            />
          </Alert>
        )}
      </Box>
    </Box>
  );
};
