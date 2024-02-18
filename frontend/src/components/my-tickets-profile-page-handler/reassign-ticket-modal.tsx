import {
  BasicButton,
  Button,
  Heading,
  Input,
  InputWrapper,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { useRef } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useTranslatedMessage } from "~/helpers/use-translated-message";

import { Modal } from "../modal";

type Form = {
  email: string;
  repeatEmail: string;
};

type Props = {
  open: boolean;
  openModal: (open: boolean) => void;
  onReassignTicket: (newEmail: string) => void;
  currentEmail: string;
};

export const ReassignTicketModal = ({
  open,
  openModal,
  onReassignTicket,
  currentEmail,
}: Props) => {
  const [formState, { email }] = useFormState<Form>();
  const formRef = useRef<HTMLFormElement>();
  const saveChanges = (e) => {
    e.preventDefault();

    if (formRef.current && !formRef.current.checkValidity()) {
      formRef.current.reportValidity();
      return;
    }

    if (Object.keys(formState.errors).length > 0) {
      return;
    }

    onReassignTicket(formState.values.email);
  };
  const emailDoNotMatchError = useTranslatedMessage(
    "orderQuestions.emailsDontMatch",
  );

  return (
    <Modal
      onClose={() => openModal(false)}
      title={<FormattedMessage id="profile.ticketsEdit.reassignTicket" />}
      show={open}
      actions={
        <div className="flex flex-col md:flex-row gap-6 justify-end items-center">
          <BasicButton onClick={() => openModal(false)}>
            <FormattedMessage id="profile.tickets.cancel" />
          </BasicButton>
          <Button
            disabled={
              formState.values.email === currentEmail || !formState.touched
            }
            size="small"
            onClick={saveChanges}
          >
            <FormattedMessage id="profile.tickets.save" />
          </Button>
        </div>
      }
    >
      <Heading size={3}>
        <FormattedMessage id="profile.ticketsEdit.reassignTicketHeading" />
      </Heading>
      <Spacer size="small" />
      <Text size={2}>
        <FormattedMessage id="profile.ticketsEdit.reassignTicketDescription" />
      </Text>
      <Spacer size="small" />

      <form onSubmit={saveChanges} ref={formRef}>
        <FormattedMessage id="orderQuestions.attendeeEmail">
          {(emailPlaceholder) => (
            <InputWrapper
              required={true}
              title={<FormattedMessage id="orderQuestions.attendeeEmail" />}
            >
              <Input
                {...email("email")}
                errors={[formState.errors.email]}
                placeholder={emailPlaceholder as unknown as string}
                required={true}
              />
            </InputWrapper>
          )}
        </FormattedMessage>
        <Spacer size="small" />

        <FormattedMessage id="orderQuestions.repeatAttendeeEmail">
          {(emailPlaceholder) => (
            <InputWrapper
              required={true}
              title={
                <FormattedMessage id="orderQuestions.repeatAttendeeEmail" />
              }
            >
              <Input
                {...email({
                  name: "repeatEmail",
                  validate(value, values) {
                    if (value !== values.email) {
                      return emailDoNotMatchError;
                    }
                  },
                  validateOnBlur: true,
                })}
                errors={[formState.errors.repeatEmail]}
                required={true}
                placeholder={emailPlaceholder as unknown as string}
              />
            </InputWrapper>
          )}
        </FormattedMessage>
      </form>
    </Modal>
  );
};
