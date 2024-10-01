import {
  Checkbox,
  HorizontalStack,
  Text,
} from "@python-italia/pycon-styleguide";
import Link from "next/link";
import { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { useCurrentLanguage } from "~/locale/context";
import { createHref } from "../link";
import { useCart } from "../tickets-page/use-cart";

export const PrivacyPolicy = () => {
  const {
    state: { acceptedPrivacyPolicy },
    updateAcceptedPrivacyPolicy,
  } = useCart();

  const [formState, { checkbox }] = useFormState<{
    acceptedPrivacyPolicy: boolean;
  }>({
    acceptedPrivacyPolicy,
  });

  useEffect(() => {
    updateAcceptedPrivacyPolicy(formState.values.acceptedPrivacyPolicy);
  }, [formState.values]);

  const language = useCurrentLanguage();
  return (
    <div>
      <label htmlFor="acceptedPrivacyPolicy">
        <HorizontalStack gap="small" alignItems="center">
          <Checkbox
            {...checkbox("acceptedPrivacyPolicy")}
            checked={formState.values.acceptedPrivacyPolicy}
            required
            id="acceptedPrivacyPolicy"
          />
          <Text size={2} weight="strong" hoverColor="none">
            <FormattedMessage
              id="global.acceptPrivacyPolicy"
              values={{
                link: (
                  <Link
                    className="underline"
                    target="_blank"
                    href={createHref({
                      path: "/privacy-policy",
                      locale: language,
                    })}
                  >
                    <Text
                      size="inherit"
                      weight="strong"
                      decoration="underline"
                      hoverColor="green"
                    >
                      <FormattedMessage id="signup.privacyPolicy" />
                    </Text>
                  </Link>
                ),
              }}
            />
          </Text>
        </HorizontalStack>
      </label>
    </div>
  );
};
