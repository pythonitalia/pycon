import {
  CardPart,
  Grid,
  GridColumn,
  Heading,
  MultiplePartsCard,
  Text,
} from "@python-italia/pycon-styleguide";
import { GearIcon, TicketsIcon } from "@python-italia/pycon-styleguide/icons";
import React, { useState } from "react";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import {
  MyProfileWithTicketsDocument,
  MyProfileWithTicketsQuery,
  useUpdateTicketMutation,
} from "~/types";

import { CustomizeTicketModal } from "./customize-ticket-modal";
import { ReassignTicketModal } from "./reassign-ticket-modal";

type Props = {
  ticket: MyProfileWithTicketsQuery["me"]["tickets"][0];
};

const snakeToCamel = (str: string) => {
  return str.replace(/[^a-zA-Z0-9]+(.)/g, (m, chr) => chr.toUpperCase());
};

export const TicketCard = ({ ticket }: Props) => {
  const [showEditTicketModal, openEditTicketModal] = useState(false);
  const [showReassignTicketModal, openReassignTicketModal] = useState(false);
  const language = useCurrentLanguage();

  const [productUserInformation, setProductUserInformation] = useState({
    id: ticket.id,
    attendeeName: ticket.name,
    attendeeEmail: ticket.email,
    errors: {},
    answers: ticket.item.questions.reduce((acc, question) => {
      acc[question.id] =
        question.options.length > 0
          ? question.options[0].id
          : question.answer?.answer;
      return acc;
    }, {}),
  });
  const [errors, setErrors] = useState({});

  const [
    updateTicket,
    { data: updatedData, loading: updatingTicket, error: updatedError },
  ] = useUpdateTicketMutation({
    onCompleted(result) {
      if (
        result.updateAttendeeTicket.__typename === "UpdateAttendeeTicketErrors"
      ) {
        setErrors(
          Object.fromEntries(
            result.updateAttendeeTicket.errors.map((error) => [
              snakeToCamel(error.field),
              error.message,
            ]),
          ),
        );
        return;
      }
    },

    update(cache, { data }) {
      if (data.updateAttendeeTicket.__typename === "TicketReassigned") {
        const { me } = cache.readQuery<MyProfileWithTicketsQuery>({
          query: MyProfileWithTicketsDocument,
          variables: {
            conference: process.env.conferenceCode,
            language: language,
          },
        });
        cache.writeQuery({
          query: MyProfileWithTicketsDocument,
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
  });

  const saveTicketChanges = (updatedProductUserInformation: any) => {
    console.log("updatedProductUserInformation", updatedProductUserInformation);
    setProductUserInformation(updatedProductUserInformation);
    callUpdateUserTicket(updatedProductUserInformation);
  };

  const onReassignTicket = (newEmail: string) => {
    const updatedProductUserInformation = {
      ...productUserInformation,
      attendeeEmail: newEmail,
      errors: {},
    };
    setProductUserInformation(updatedProductUserInformation);
    callUpdateUserTicket(updatedProductUserInformation);
  };

  const callUpdateUserTicket = (updatedProductUserInformation) => {
    const answers = ticket.item.questions
      .map((question) => {
        let answer;
        let option = null;

        if (question.options.length > 0) {
          option = question.options.filter(
            (option) =>
              option.id == updatedProductUserInformation.answers[question.id],
          )[0];
          answer = option.name;
        } else {
          answer = updatedProductUserInformation.answers[question.id] || "";
        }

        const data = {
          answer,
          question: question.id,
        };

        if (option) {
          data["options"] = [option.id];
        }
        return data;
      })
      .filter((item) => item.answer !== "");

    updateTicket({
      variables: {
        conference: process.env.conferenceCode,
        language: language,
        input: {
          id: updatedProductUserInformation.id,
          name: updatedProductUserInformation.attendeeName,
          email: updatedProductUserInformation.attendeeEmail,
          answers,
        },
      },
    });
  };

  const taglineQuestion = ticket.item.questions.find(
    (question) => question.name.toLowerCase() === "tagline",
  );

  return (
    <>
      <MultiplePartsCard>
        <CardPart contentAlign="left">
          <Heading size={3}>{ticket.item.name}</Heading>
        </CardPart>
        <CardPart contentAlign="left" background="milk">
          <Grid cols={2} mdCols={2}>
            <Item
              label={<FormattedMessage id="profile.tickets.attendeeName" />}
              value={ticket.name}
            />
            {ticket.item.questions
              .filter((question) => question.id !== taglineQuestion.id)
              .map((question) => (
                <Item
                  key={question.id}
                  label={question.name}
                  value={
                    question.answer?.answer ?? (
                      <FormattedMessage id="profile.tickets.noAnswer" />
                    )
                  }
                />
              ))}
            <GridColumn colSpan={2}>
              <Item
                label={taglineQuestion.name}
                value={
                  taglineQuestion.answer?.answer ?? (
                    <FormattedMessage id="profile.tickets.noAnswer" />
                  )
                }
              />
            </GridColumn>
          </Grid>
        </CardPart>
        <CardPart size="none" contentAlign="left">
          <div className="flex divide-x">
            <div
              className="p-5 flex flex-col items-center justify-center cursor-pointer"
              onClick={() => openEditTicketModal(true)}
            >
              <GearIcon className="w-10 h-10 shrink-0" />
            </div>
            <div
              onClick={() => openReassignTicketModal(true)}
              className="p-5 flex items-center justify-center cursor-pointer"
            >
              <TicketsIcon className="w-10 h-10 shrink-0" />
            </div>
          </div>
        </CardPart>
      </MultiplePartsCard>
      <CustomizeTicketModal
        ticket={ticket}
        saveChanges={saveTicketChanges}
        productUserInformation={productUserInformation}
        updatingTicket={updatingTicket}
        open={showEditTicketModal}
        openModal={openEditTicketModal}
        errors={errors}
      />
      <ReassignTicketModal
        open={showReassignTicketModal}
        openModal={openReassignTicketModal}
        onReassignTicket={onReassignTicket}
        currentEmail={productUserInformation.attendeeEmail}
      />
    </>
  );
};

type ItemProps = {
  label: React.ReactNode;
  value: string | React.ReactNode;
};
const Item = ({ label, value }: ItemProps) => {
  return (
    <div>
      <Heading color="grey-500" size={5}>
        {label}
      </Heading>
      <Text size={3}>{value}</Text>
    </div>
  );
};
