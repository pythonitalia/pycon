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
import { QuestionsSection } from "~/components/tickets-page/questions-section";
import { useCurrentUser } from "~/helpers/use-current-user";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import {
  AttendeeTicket,
  useUpdateTicketMutation,
  MyProfileDocument,
} from "~/types";

import { ProductState } from "../tickets-page/types";

type Props = {
  tickets: AttendeeTicket[];
};

export const MyTickets = ({ tickets = [] }: Props) => {
  const code = process.env.conferenceCode;

  const language = useCurrentLanguage();
  const { user } = useCurrentUser({ skip: false });
  const ticketHeader = useTranslatedMessage("profile.ticketFor");
  const nameHeader = useTranslatedMessage("orderReview.attendeeName");
  const emailHeader = useTranslatedMessage("orderReview.attendeeEmail");
  const [currentTicketId, setCurrentTicketId] = useState(null);
  const [error, setError] = useState(null);

  const headers = [ticketHeader, nameHeader, emailHeader, ""];

  const [selectedProducts, setSelectedProducts] = useState(
    tickets.reduce((accumulator, ticket) => {
      // if accumulator[ticket.id] is undefined assign empty list
      (accumulator[ticket.id] = accumulator[ticket.id] || []).push({
        id: ticket.id,
        attendeeName: ticket.name,
        attendeeEmail: ticket.email,
        answers: Object.fromEntries(
          ticket.item.questions.map((question) => [
            question.id,
            question.options.length > 0
              ? question.answer.options[0]
              : question.answer.answer,
          ]),
        ),
      } as ProductState);
      return accumulator;
    }, {}),
  );

  const [
    updateTicket,
    { data: updatedData, loading: updatingTicket, error: updatedError },
  ] = useUpdateTicketMutation({
    onCompleted(result) {
      if (
        ["AttendeeTicket", "TicketReassigned"].indexOf(
          result.updateAttendeeTicket.__typename,
        ) > -1
      ) {
        setCurrentTicketId(null);
      }
    },
    update(cache, { data }) {
      if (data.updateAttendeeTicket.__typename === "TicketReassigned") {
        setCurrentTicketId(null);
        const { me } = cache.readQuery({
          query: MyProfileDocument,
          variables: {
            conference: process.env.conferenceCode,
            language: language,
          },
        });
        cache.writeQuery({
          query: MyProfileDocument,
          data: {
            me: {
              ...me,
              tickets: me.tickets.filter(
                (ticket) => ticket.id !== data.updateAttendeeTicket.id,
              ),
            },
          },
          variables: {
            conference: process.env.conferenceCode,
            language: language,
          },
        });
      }
    },
    onError(err) {
      console.error(err);
      setError(err.message);
    },
  });

  const updateTicketCallback = useCallback(
    (id: string) => {
      return () => {
        const answers = tickets
          .filter((item) => item.id == id)[0]
          .item.questions.map((question) => {
            let answer;
            let option = null;
            if (question.options.length > 0) {
              option = question.options.filter(
                (option) =>
                  option.id == selectedProducts[id][0].answers[question.id],
              )[0];
              answer = option.name;
            } else {
              answer = selectedProducts[id][0].answers[question.id];
            }

            const data = {
              answer: answer,
              question: question.id,
            };
            if (option) {
              data["options"] = [option.id];
            }
            return data;
          });
        updateTicket({
          variables: {
            conferenceCode: code,
            input: {
              id,
              name: selectedProducts[id][0].attendeeName,
              email: selectedProducts[id][0].attendeeEmail,
              answers: answers,
            },
          },
        });
      };
    },
    [selectedProducts],
  );

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
              <Box sx={{ m: -2 }}>
                <Button
                  onClick={() => setCurrentTicketId(item.id)}
                  variant="small"
                >
                  <FormattedMessage id="profile.manageTicket" />
                </Button>
              </Box>,
            ]}
          />
        )}
        {["AttendeeTicket", "TicketReassigned"].indexOf(
          updatedData?.updateAttendeeTicket.__typename,
        ) > -1 && (
          <Alert variant="success">
            <FormattedMessage
              id={`profile.myTickets.update.${updatedData.updateAttendeeTicket.__typename}.message`}
              values={{ email: updatedData.updateAttendeeTicket.email }}
            />
          </Alert>
        )}

        {currentTicketId && (
          <Modal
            show={!!currentTicketId}
            onClose={() => setCurrentTicketId(null)}
          >
            <QuestionsSection
              tickets={[
                {
                  ...tickets.filter((item) => item.id == currentTicketId)[0]
                    .item,
                  id: currentTicketId,
                },
              ]}
              updateTicketInfo={({ id, index, key, value }) => {
                selectedProducts[id][index][key] = value;
                setSelectedProducts({ ...selectedProducts });
              }}
              updateQuestionAnswer={({ id, index, question, answer }) => {
                selectedProducts[id][index]["answers"][question] = answer;
                setSelectedProducts({ ...selectedProducts });
              }}
              selectedProducts={Object.assign(
                {},
                ...Object.entries(selectedProducts)
                  .filter(([k, v]) => k == currentTicketId)
                  .map(([k, v]) => ({ [k]: v })),
              )}
              showHeading={false}
              nextStepMessageId="buttons.save"
              onNextStep={updateTicketCallback(currentTicketId)}
              nextStepLoading={updatingTicket}
            />

            <Box sx={{ ml: 3 }}>
              {(updatedData?.updateAttendeeTicket.__typename ===
                "UpdateAttendeeTicketError" ||
                updatedError) && (
                <Alert variant="alert">
                  {error ? (
                    error
                  ) : (
                    <FormattedMessage id="global.somethingWentWrong" />
                  )}
                </Alert>
              )}
            </Box>
          </Modal>
        )}
      </Box>
    </Box>
  );
};
