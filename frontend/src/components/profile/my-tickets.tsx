/** @jsxRuntime classic */

/** @jsx jsx */
import { useState } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

import { Button } from "~/components/button/button";
import { Modal } from "~/components/modal";
import { Table } from "~/components/table";
import { QuestionsSection } from "~/components/tickets-page/questions-section";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { PretixOrderPosition } from "~/types";

type Props = {
  tickets: PretixOrderPosition[];
};

export const MyTickets: React.FC<Props> = ({ tickets }) => {
  const [showModal, setShowModal] = useState(false);
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

  const [questions, setQuestions] = useState([]);

  // console.log(ticket);
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
              <Button onClick={() => setShowModal(!showModal)} variant="small">
                <FormattedMessage id="profile.manageTicket" />
              </Button>

              <Modal show={showModal} onClose={() => setShowModal(false)}>
                <QuestionsSection
                  tickets={[
                    {
                      // attendeeName: item.name,
                      // attendeeEmail: item.email,
                      ...item.item,
                    },
                  ]}
                  // updateTicketInfo={updateTicketInfo}
                  updateTicketInfo={({ id, index, key, value }) => {
                    console.log(id, index, key, value);
                  }}
                  updateQuestionAnswer={({ id, index, question, answer }) => {
                    console.log(id, index, question, answer);
                  }}
                  selectedProducts={{
                    [item.id]: [
                      {
                        answers: item.item.questions.map((question) => {
                          console.log("question.id", question.id.toString());
                          return {
                            [String(question.id)]: question.answer.answer,
                          };
                        }),
                        ...item.item,
                        attendeeName: item.name,
                        attendeeEmail: item.email,
                      },
                    ],
                  }}
                  onNextStep={() => {
                    return;
                  }}
                  showHeading={false}
                />
              </Modal>
            </Box>,
          ]}
        />
      </Box>
    </Box>
  );
};
