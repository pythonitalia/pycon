import { BasicButton, Spacer, Button } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { MyProfileWithTicketsQuery } from "~/types";

import { Modal } from "../modal";
import { ProductQuestionnaire } from "../product-questionnaire";

type Props = {
  open: boolean;
  openModal: (open: boolean) => void;
  ticket: MyProfileWithTicketsQuery["me"]["tickets"][0];
  productUserInformation: any;
  updatingTicket: boolean;
  saveChanges: (updatedProductUserInformation: any) => void;
  errors: { [key: string]: string };
};

type Form = {
  id: string;
  attendeeName: string;
  attendeeEmail: string;
  answers: { [key: string]: string };
};

export const CustomizeTicketModal = ({
  open,
  openModal,
  ticket,
  updatingTicket,
  saveChanges,
  productUserInformation,
  errors,
}: Props) => {
  const [formState] = useFormState<Form>({
    id: productUserInformation.id,
    attendeeName: productUserInformation.attendeeName,
    attendeeEmail: productUserInformation.attendeeEmail,
    answers: ticket.item.questions.reduce((acc, question) => {
      acc[question.id] =
        question.options.length > 0
          ? question.options[0].id
          : question.answer?.answer;
      return acc;
    }, {}),
  });

  return (
    <Modal
      title={<FormattedMessage id="profile.ticketsEdit.modalTitle" />}
      onClose={() => openModal(false)}
      show={open}
      actions={
        <div className="flex flex-col md:flex-row gap-6 justify-end items-center">
          <BasicButton onClick={() => openModal(false)}>
            <FormattedMessage id="profile.tickets.cancel" />
          </BasicButton>
          <Button
            disabled={updatingTicket}
            size="small"
            role="secondary"
            onClick={() => saveChanges(formState.values)}
          >
            <FormattedMessage id="profile.tickets.save" />
          </Button>
        </div>
      }
    >
      <ProductQuestionnaire
        product={ticket.item}
        index={0}
        hideAttendeeEmail={true}
        productUserInformation={{
          ...formState.values,
          errors,
        }}
        updateTicketInfo={({ key, value }) => {
          formState.setField(key, value);
        }}
        updateQuestionAnswer={({ question, answer }) => {
          formState.setField("answers", {
            ...formState.values.answers,
            [question]: answer,
          });
        }}
      />
    </Modal>
  );
};
