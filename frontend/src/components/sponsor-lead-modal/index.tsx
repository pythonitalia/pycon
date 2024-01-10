import {
  Button,
  Spacer,
  Text,
  Input,
  InputWrapper,
  BasicButton,
  Link,
} from "@python-italia/pycon-styleguide";
import React, { useCallback, useRef, useState } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { NewsletterSubscriptionResult, useSubscribeMutation } from "~/types";

import { Modal } from "../modal";

type SponsorLeadForm = {
  email: string;
  fullname: string;
  company: string;
};
export const SponsorLeadModal = ({ onClose }) => {
  const [formValues, { email, text }] = useFormState<SponsorLeadForm>({
    email: "",
    fullname: "",
    company: "",
  });

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
          <Button role="secondary">
            <FormattedMessage id="sponsorLeadModal.submit" />
          </Button>
        </div>
      }
    >
      <Text size={2}>
        <FormattedMessage id="sponsorLeadModal.body" />
      </Text>
      <Spacer size="medium" />
      <form>
        <InputWrapper title={<FormattedMessage id="signup.email" />}>
          <Input placeholder="Jane Doe" required={true} {...text("fullname")} />
        </InputWrapper>
        <Spacer size="small" />
        <InputWrapper title={<FormattedMessage id="signup.company" />}>
          <Input
            placeholder="Save the world with Python TLD"
            required={true}
            {...text("company")}
          />
        </InputWrapper>
        <Spacer size="small" />
        <InputWrapper title={<FormattedMessage id="signup.email" />}>
          <Input
            placeholder="my-name@my-amazing-company.com"
            required={true}
            {...email("email")}
          />
        </InputWrapper>
      </form>
    </Modal>
  );
};
