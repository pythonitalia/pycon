import {
  BasicButton,
  Button,
  Heading,
  Input,
  InputWrapper,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { useRef, useState } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useTranslatedMessage } from "~/helpers/use-translated-message";

import { useCurrentLanguage } from "~/locale/context";
import {
  MyProfileWithTicketsDocument,
  MyProfileWithTicketsQuery,
  useUpdateTicketMutation,
} from "~/types";
import { snakeToCamel } from "../customize-ticket-modal";
import { Modal } from "../modal";

type Form = {
  email: string;
  repeatEmail: string;
};

type Props = {
  onClose: () => void;
};

export type ReassignTicketModalProps = {
  ticket: MyProfileWithTicketsQuery["me"]["tickets"][0];
};

export const ReassignTicketModal = ({
  onClose,
  ticket,
}: Props & ReassignTicketModalProps) => {
  const [formState, { email }] = useFormState<Form>();
  const [errors, setErrors] = useState({});
  const language = useCurrentLanguage();

  const [updateTicket, { loading: updatingTicket, error: updateTicketError }] =
    useUpdateTicketMutation({
      onCompleted(result) {
        if (
          result.updateAttendeeTicket.__typename ===
          "UpdateAttendeeTicketErrors"
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
          onClose();
        }
      },
    });

  const currentEmail = ticket.email;
  const formRef = useRef<HTMLFormElement>();
  const saveChanges = (e) => {
    e.preventDefault();

    if (!formRef.current?.checkValidity()) {
      formRef.current.reportValidity();
      return;
    }

    if (Object.keys(formState.errors).length > 0) {
      return;
    }

    updateTicket({
      variables: {
        conference: process.env.conferenceCode,
        language: language,
        input: {
          id: ticket.id,
          name: ticket.name,
          email: formState.values.email,
        },
      },
    });
  };

  const emailDoNotMatchError = useTranslatedMessage(
    "orderQuestions.emailsDontMatch",
  );

  return (
    <Modal
      onClose={onClose}
      title={<FormattedMessage id="profile.ticketsEdit.reassignTicket" />}
      show={true}
      actions={
        <div className="flex flex-col md:flex-row gap-6 justify-end items-center">
          <BasicButton onClick={onClose}>
            <FormattedMessage id="profile.tickets.cancel" />
          </BasicButton>
          <Button
            disabled={
              formState.values.email === currentEmail || !formState.touched
            }
            size="small"
            onClick={saveChanges}
            variant="secondary"
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
