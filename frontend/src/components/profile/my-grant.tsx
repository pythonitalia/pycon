import { Text, Section, Link, Heading } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { Alert } from "~/components/alert";
import { useCurrentLanguage } from "~/locale/context";
import { useMyGrantQuery } from "~/types";

import { createHref } from "../link";

export const MyGrant = () => {
  const code = process.env.conferenceCode;
  const language = useCurrentLanguage();
  const { loading, error, data } = useMyGrantQuery({
    errorPolicy: "all",
    variables: {
      conference: code,
    },
    skip: typeof window === "undefined",
  });

  if (loading) {
    return null;
  }

  if (!error && data!.me!.grant === undefined) {
    return null;
  }

  return (
    <>
      <Section>
        <Heading size="display2">
          <FormattedMessage id="grants.form.title" />
        </Heading>
      </Section>
      <Section>
        {error && <Alert variant="alert">{error.message}</Alert>}

        {data && (
          <Text>
            <FormattedMessage
              id="grants.alreadySubmitted"
              values={{
                linkGrant: (
                  <Link
                    href={createHref({
                      path: "/grants/edit",
                      locale: language,
                    })}
                  >
                    <Text color="none" weight="strong" decoration="underline">
                      <FormattedMessage id="grants.form.sent.linkGrant.text" />
                    </Text>
                  </Link>
                ),
              }}
            />
          </Text>
        )}
      </Section>
    </>
  );
};
