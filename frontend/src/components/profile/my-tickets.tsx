/** @jsxRuntime classic */

/** @jsx jsx */
import { useRouter } from "next/router";
import { useState, useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

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
  const router = useRouter();
  const code = process.env.conferenceCode;
  const ticketHeader = useTranslatedMessage("profile.ticketFor");
  const nameHeader = useTranslatedMessage("orderReview.attendeeName");
  const emailHeader = useTranslatedMessage("orderReview.attendeeEmail");

  const headers = [
    ticketHeader,
    nameHeader,
    emailHeader,
    ...tickets[0].item.questions.map((question) => question.name),
    "",
  ];

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
  const [showModals, setShowModals] = useState(
    Object.fromEntries(tickets.map((item) => [item.id, false])),
  );
  const toggleModal = (ticketId?: string) => {
    return () => {
      console.log("toggleModal", ticketId);
      if (ticketId) {
        console.log("toggleModal ", ticketId, " to ", !showModals[ticketId]);
        showModals[ticketId] = !showModals[ticketId];
      } else {
        console.log("setting false");
        Object.keys(showModals).forEach((item) => (showModals[item] = false));
      }
      console.log("showModals: ", showModals);
      setShowModals({ ...showModals });
    };
  };

  const [
    updateTicket,
    { data: ticketData, loading: updatingTicket },
  ] = useUpdateTicketMutation({
    onCompleted(result) {
      console.log(result);
      if (result.updateAttendeeTicket.__typename === "OperationResult") {
        console.log("push!");
        toggleModal()();
        router.push("/profile");
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
        console.log("Updating the ticket!!");
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
            ...item.item.questions.map((question) => question.answer.answer),
            <Box>
              <Button onClick={toggleModal(item.id)} variant="small">
                <FormattedMessage id="profile.manageTicket" />
              </Button>
              {showModals[item.id] && (
                <Modal
                  show={showModals[item.id]}
                  onClose={toggleModal(item.id)}
                >
                  <QuestionsSection
                    tickets={[
                      {
                        ...item.item,
                        id: item.id,
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
                    onNextStep={updateTicketCallback(item.id)}
                    nextStepLoading={updatingTicket}
                  />
                </Modal>
              )}
            </Box>,
          ]}
        />
      </Box>
    </Box>
  );
};
