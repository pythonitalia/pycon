import {
  CardPart,
  Grid,
  GridColumn,
  Heading,
  MultiplePartsCard,
  Text,
} from "@python-italia/pycon-styleguide";
import { GearIcon, TicketsIcon } from "@python-italia/pycon-styleguide/icons";
import type React from "react";
import { FormattedMessage } from "react-intl";
import QRCode from "react-qr-code";
import type { MyProfileWithTicketsQuery } from "~/types";

import { useSetCurrentModal } from "../modal/context";

type Props = {
  ticket: MyProfileWithTicketsQuery["me"]["tickets"][0];
  userEmail: string;
};

export const TicketCard = ({ ticket, userEmail }: Props) => {
  const setCurrentModal = useSetCurrentModal();

  const taglineQuestion = ticket.item.questions.find(
    (question) => question.name.toLowerCase() === "tagline",
  );

  const isAdmissionTicket = ticket.item.admission;
  const emptyDetails =
    !isAdmissionTicket &&
    !ticket.variation &&
    ticket.item.questions.length === 0;

  const ticketReassigned = isAdmissionTicket && ticket.email !== userEmail;

  const openQRCodeModal = () => {
    setCurrentModal("ticket-qr-code", {
      qrCodeValue: ticket.secret,
    });
  };

  const openEditTicketModal = () => {
    setCurrentModal("customize-ticket", {
      ticket,
    });
  };

  const openReassignTicketModal = () => {
    setCurrentModal("reassign-ticket", {
      ticket,
    });
  };

  return (
    <>
      <MultiplePartsCard>
        <CardPart contentAlign="left" shrink={false}>
          <Heading size={3}>{ticket.item.name}</Heading>
        </CardPart>
        <CardPart contentAlign="left" background="milk" fullHeight>
          <Grid cols={2} mdCols={2}>
            {ticketReassigned && (
              <GridColumn colSpan={2} className="break-words">
                <Text size={3}>
                  <FormattedMessage
                    id="profile.tickets.ticketReassigned"
                    values={{
                      to: (
                        <Text weight="strong" size={3}>
                          {ticket.email}
                        </Text>
                      ),
                    }}
                  />
                </Text>
              </GridColumn>
            )}
            {!ticketReassigned && (
              <>
                {isAdmissionTicket && (
                  <Item
                    label={
                      <FormattedMessage id="profile.tickets.attendeeName" />
                    }
                    value={ticket.name}
                  />
                )}
                {ticket.variation && (
                  <Item
                    label={<FormattedMessage id="profile.tickets.size" />}
                    value={
                      ticket.item.variations.find(
                        (variation) => variation.id === ticket.variation,
                      ).value
                    }
                  />
                )}
                {ticket.item.questions
                  .filter((question) => question.id !== taglineQuestion?.id)
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
                {taglineQuestion && (
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
                )}
                {emptyDetails && (
                  <Heading color="black" size={5}>
                    <FormattedMessage id="profile.tickets.noDetails" />
                  </Heading>
                )}
              </>
            )}
          </Grid>
        </CardPart>
        {!ticketReassigned && (
          <CardPart size="none" contentAlign="left" shrink={false}>
            <div className="flex justify-between">
              <div className="flex divide-x">
                {isAdmissionTicket && !ticketReassigned && (
                  <div
                    className="p-5 flex flex-col items-center justify-center cursor-pointer"
                    onClick={openEditTicketModal}
                  >
                    <GearIcon className="w-10 h-10 shrink-0" />
                  </div>
                )}
                {isAdmissionTicket && !ticketReassigned && (
                  <div
                    onClick={openReassignTicketModal}
                    className="p-5 flex items-center justify-center cursor-pointer"
                  >
                    <TicketsIcon className="w-10 h-10 shrink-0" />
                  </div>
                )}
              </div>
              {!ticketReassigned && (
                <div
                  className="p-2 shrink-0 cursor-pointer"
                  onClick={openQRCodeModal}
                >
                  <QRCode
                    className="w-full h-full"
                    bgColor="none"
                    size={64}
                    value={ticket.secret}
                  />
                </div>
              )}
            </div>
          </CardPart>
        )}
      </MultiplePartsCard>
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
