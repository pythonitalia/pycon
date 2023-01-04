import {
  BasicButton,
  Button,
  CardPart,
  Grid,
  GridColumn,
  Heading,
  MultiplePartsCard,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { GearIcon } from "@python-italia/pycon-styleguide/icons";
import React, { useState } from "react";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { MyProfileWithTicketsQuery, useUpdateTicketMutation } from "~/types";

import { Modal } from "../modal";
import { ProductQuestionnaire } from "../product-questionnaire";
import { ProductState } from "../tickets-page/types";

type Props = {
  ticket: MyProfileWithTicketsQuery["me"]["tickets"][0];
};

export const TicketCard = ({ ticket }: Props) => {
  const [showModal, openModal] = useState(false);
  const language = useCurrentLanguage();

  const [productUserInformation, setProductUserInformation] = useState({
    id: ticket.id,
    attendeeName: ticket.name,
    attendeeEmail: ticket.email,
    answers: ticket.item.questions.reduce((acc, question) => {
      acc[question.id] = question.answer?.answer;
      return acc;
    }, {}),
  });

  const [
    updateTicket,
    { data: updatedData, loading: updatingTicket, error: updatedError },
  ] = useUpdateTicketMutation();

  const taglineQuestion = ticket.item.questions.find(
    (question) => question.name.toLowerCase() === "tagline",
  );
  console.log("!!", productUserInformation);

  return (
    <>
      <MultiplePartsCard>
        <CardPart contentAlign="left">
          <Heading size={3}>{ticket.item.name}</Heading>
        </CardPart>
        <CardPart contentAlign="left" background="milk">
          <Grid cols={2}>
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
        <CardPart contentAlign="left">
          <Grid divide cols={4}>
            <GearIcon
              className="cursor-pointer"
              onClick={() => openModal(true)}
            />
          </Grid>
        </CardPart>
      </MultiplePartsCard>
      <Modal
        title="Customize your ticket"
        onClose={() => openModal(false)}
        show={showModal}
        actions={
          <div className="flex justify-end items-center">
            <BasicButton onClick={(_) => openModal(false)}>Cancel</BasicButton>
            <Spacer orientation="horizontal" size="large" />
            <Button size="small">
              <FormattedMessage id="profile.tickets.save" />
            </Button>
          </div>
        }
      >
        <ProductQuestionnaire
          product={ticket.item}
          index={0}
          productUserInformation={productUserInformation}
          updateTicketInfo={({ key, value }) => {
            setProductUserInformation({
              ...productUserInformation,
              [key]: value,
            });
          }}
          updateQuestionAnswer={({ id, index, question, answer }) => {
            setProductUserInformation({
              ...productUserInformation,
              answers: {
                ...productUserInformation.answers,
                [question]: answer,
              },
            });
          }}
        />
      </Modal>
    </>
  );
};

type ItemProps = {
  label: React.ReactNode;
  value: string;
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
