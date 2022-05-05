/** @jsxRuntime classic */

/** @jsx jsx */
import { useState, useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

import { useRouter } from "next/router";

import { Alert } from "~/components/alert";
import { Button } from "~/components/button/button";
import { Modal } from "~/components/modal";
import { Table } from "~/components/table";
import { QuestionsSection } from "~/components/tickets-page/questions-section";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { AttendeeTicket, useUpdateTicketMutation } from "~/types";

import { ProductState } from "../tickets-page/types";

type Props = {
  tickets: AttendeeTicket[];
};

export const MyTickets: React.FC<Props> = ({ tickets }) => {
  const code = process.env.conferenceCode;
  const ticketHeader = useTranslatedMessage("profile.ticketFor");
  const nameHeader = useTranslatedMessage("orderReview.attendeeName");
  const emailHeader = useTranslatedMessage("orderReview.attendeeEmail");
  const [currentTicket, setCurrentTicket] = useState({ id: null, show: false });

  const headers = [ticketHeader, nameHeader, emailHeader, ""];

  const [selectedProducts, setSelectedProducts] = useState(
    tickets.reduce((acc, ticket) => {
      (acc[ticket.id] = acc[ticket.id] || []).push({
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
      return acc;
    }, {}),
  );

  const [
    updateTicket,
    { data: updatedData, loading: updatingTicket, error: updatedError },
  ] = useUpdateTicketMutation({
    onCompleted(result) {
      if (result.updateAttendeeTicket.__typename === "AttendeeTicket") {
        setCurrentTicket({ id: null, show: false });
      }
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
            conference: code,
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
                onClick={() => setCurrentTicket({ id: item.id, show: true })}
                variant="small"
              >
                <FormattedMessage id="profile.manageTicket" />
              </Button>
            </Box>,
          ]}
        />
        {["AttendeeTicket", "OperationSuccess"].indexOf(
          updatedData?.updateAttendeeTicket.__typename,
        ) >= 0 && (
          <Alert variant="success">
            <FormattedMessage id="profile.myTickets.update.succeed.message" />
          </Alert>
        )}

        {currentTicket.id && (
          <Modal
            show={currentTicket.show}
            onClose={() => setCurrentTicket({ id: null, show: false })}
          >
            <QuestionsSection
              tickets={[
                {
                  ...tickets.filter((item) => item.id == currentTicket.id)[0]
                    .item,
                  id: currentTicket.id,
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
              selectedProducts={selectedProducts}
              showHeading={false}
              nextStepMessageId="buttons.save"
              onNextStep={updateTicketCallback(currentTicket.id)}
              nextStepLoading={updatingTicket}
            />

            <Box sx={{ ml: 3 }}>
              {(updatedData?.updateAttendeeTicket.__typename ===
                "UpdateAttendeeTicketError" ||
                updatedError) && (
                <Alert variant="alert">
                  <FormattedMessage id="global.somethingWentWrong" />
                </Alert>
              )}
            </Box>
          </Modal>
        )}
      </Box>
    </Box>
  );
};
