import {
  Button,
  Spacer,
  Text,
  Input,
  InputWrapper,
  BasicButton,
} from "@python-italia/pycon-styleguide";
import React, { useRef } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useSendSponsorLeadMutation } from "~/types";

import { Modal } from "../modal";

type SponsorLeadForm = {
  email: string;
  fullname: string;
  company: string;
};
export const SponsorLeadModal = ({ onClose }) => {
  const formRef = useRef<HTMLFormElement>();

  const [sendSponsorLeadMutation, { loading, data, error }] =
    useSendSponsorLeadMutation();
  const [formState, { email, text }] = useFormState<SponsorLeadForm>({
    email: "",
    fullname: "",
    company: "",
  });

  const onSubmit = (e) => {
    e.preventDefault();
    if (!formRef.current.reportValidity()) {
      return;
    }

    sendSponsorLeadMutation({
      variables: {
        input: {
          fullname: formState.values.fullname,
          company: formState.values.company,
          email: formState.values.email,
          conferenceCode: process.env.conferenceCode,
        },
      },
    });
  };

  const submitComplete =
    data?.sendSponsorLead?.__typename === "OperationResult" &&
    data?.sendSponsorLead?.ok;

  return (
    <Modal
      title={<FormattedMessage id="sponsorLeadModal.title" />}
      onClose={onClose}
      show={true}
      actions={
        <div className="flex flex-col-reverse md:flex-row gap-6 justify-end items-center">
          <BasicButton onClick={onClose}>
            <FormattedMessage id="modal.cancel" />
          </BasicButton>
          <Button
            role="secondary"
            disabled={loading || submitComplete}
            onClick={onSubmit}
          >
            <FormattedMessage id="sponsorLeadModal.submit" />
          </Button>
        </div>
      }
    >
      <Text size={2}>
        <FormattedMessage id="sponsorLeadModal.body" />
      </Text>
      <Spacer size="medium" />
      {!submitComplete && (
        <form onSubmit={onSubmit} ref={formRef}>
          <InputWrapper
            title={<FormattedMessage id="signup.email" />}
            required={true}
          >
            <Input
              placeholder="Jane Doe"
              required={true}
              {...text("fullname")}
            />
          </InputWrapper>
          <Spacer size="small" />
          <InputWrapper
            title={<FormattedMessage id="sponsorLeadModal.company" />}
            required={true}
          >
            <Input
              placeholder="Save the world with Python TLD"
              required={true}
              {...text("company")}
            />
          </InputWrapper>
          <Spacer size="small" />
          <InputWrapper
            title={<FormattedMessage id="signup.email" />}
            required={true}
          >
            <Input
              placeholder="my-name@my-amazing-company.com"
              required={true}
              {...email("email")}
            />
          </InputWrapper>
          {error && (
            <Text size={1} color="red">
              {error.message}
            </Text>
          )}
        </form>
      )}
      {submitComplete && (
        <Text size={1}>
          <FormattedMessage id="sponsorLeadModal.completed" />
        </Text>
      )}
    </Modal>
  );
};
