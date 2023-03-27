import {
  Button,
  Spacer,
  Text,
  Input,
  InputWrapper,
  BasicButton,
} from "@python-italia/pycon-styleguide";
import React, { useCallback, useRef, useState } from "react";
import { FormattedMessage } from "react-intl";

import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { NewsletterSubscriptionResult, useSubscribeMutation } from "~/types";

import { Modal } from "../modal";

export const NewsletterModal = ({ openModal, show }) => {
  const formRef = useRef<HTMLFormElement>();
  const [email, setEmail] = useState("");
  const [subscribe, { loading, error, data }] = useSubscribeMutation();
  const subscribeToNewsletter = data?.subscribeToNewsletter;

  const hasFormErrors =
    subscribeToNewsletter?.__typename === "SubscribeToNewsletterErrors";
  const hasCompletedSubscription =
    subscribeToNewsletter?.__typename === "NewsletterSubscribeResult";
  const isUnableToSubscribe =
    hasCompletedSubscription &&
    subscribeToNewsletter?.status ===
      NewsletterSubscriptionResult.UnableToSubscribe;

  const canSubmit = email.trim() !== "" && !loading;
  const onSubmit = useCallback(
    async (e) => {
      e.preventDefault();

      if (
        loading ||
        hasCompletedSubscription ||
        !formRef.current.reportValidity()
      ) {
        return;
      }

      subscribe({
        variables: {
          email,
        },
      });
    },
    [email, hasCompletedSubscription, loading],
  );

  const errorMessage = useTranslatedMessage("newsletter.error");

  const getErrors = (key: "validationEmail" | "nonFieldErrors") =>
    (hasFormErrors && data.subscribeToNewsletter[key]) || [];

  const success =
    hasCompletedSubscription &&
    subscribeToNewsletter.status == NewsletterSubscriptionResult.Subscribed;

  return (
    <Modal
      title={<FormattedMessage id="footer.stayTuned" />}
      onClose={() => openModal(false)}
      show={show}
      actions={
        <div className="flex flex-col md:flex-row gap-6 justify-end items-center">
          <BasicButton onClick={() => openModal(false)}>
            <FormattedMessage id="profile.tickets.cancel" />
          </BasicButton>
          <Button role="secondary" onClick={onSubmit} disabled={!canSubmit}>
            <FormattedMessage id="newsletter.button" />
          </Button>
        </div>
      }
    >
      <form onSubmit={onSubmit} ref={formRef}>
        <Text size={2}>
          <FormattedMessage id="newsletter.text" />
        </Text>
        <Spacer size="small" />

        <InputWrapper title={<FormattedMessage id="signup.email" />}>
          <Input
            placeholder="guido@python.org"
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setEmail(e.target.value)
            }
            value={email}
            required={true}
            type="email"
            errors={[
              ...getErrors("validationEmail"),
              error || isUnableToSubscribe ? errorMessage : "",
            ]}
          />
        </InputWrapper>

        {hasCompletedSubscription && !isUnableToSubscribe && (
          <Text size={2}>
            <FormattedMessage
              id={success ? "newsletter.success" : "newsletter.confirmViaEmail"}
            />
          </Text>
        )}
      </form>
    </Modal>
  );
};
