import {
  Button,
  Page,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { GetServerSideProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { createHref } from "~/components/link";
import { ScheduleEventDetail } from "~/components/schedule-event-detail";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import NotFoundPage from "~/pages/404";
import { getType } from "~/pages/event/[slug]";
import {
  queryIsVotingClosed,
  querySubmission,
  useSubmissionQuery,
} from "~/types";

export const SubmissionPage = () => {
  const router = useRouter();
  const language = useCurrentLanguage();

  const id = router.query.id as string;

  const {
    data: { submission: englishSubmission },
  } = useSubmissionQuery({
    errorPolicy: "all",
    variables: {
      id,
      language: "en",
    },
  });

  const {
    data: { submission: italianSubmission },
  } = useSubmissionQuery({
    errorPolicy: "all",
    variables: {
      id,
      language: "it",
    },
  });

  const [viewInLanguage, setViewInLanguage] = React.useState<string>(language);
  const submission =
    viewInLanguage === "it" ? italianSubmission : englishSubmission;

  const otherLanguage = viewInLanguage === "it" ? "en" : "it";

  if (!italianSubmission && !englishSubmission) {
    return <NotFoundPage />;
  }

  return (
    <Page endSeparator={false}>
      <ScheduleEventDetail
        id={submission.id}
        type={getType(submission.type.name)}
        eventTitle={submission.title}
        elevatorPitch={submission.elevatorPitch}
        abstract={submission.abstract}
        tags={submission?.tags.map((tag) => tag.name)}
        language={
          submission.languages.length > 1
            ? viewInLanguage
            : submission.languages[0].code
        }
        audienceLevel={submission?.audienceLevel.name}
        startTime={null}
        endTime={null}
        speakers={[]}
        bookable={false}
        spacesLeft={0}
        sidebarExtras={
          <VerticalStack alignItems="start" gap="small">
            {submission.canEdit ? (
              <Button
                size="small"
                variant="primary"
                href={createHref({
                  path: "/submission/[id]/edit",
                  params: {
                    id: submission.id,
                  },
                  locale: language,
                })}
              >
                <FormattedMessage id="profile.myProposals.edit" />
              </Button>
            ) : null}

            {submission.languages.length > 1 && (
              <>
                <Text as="p" size="label3">
                  <FormattedMessage
                    id="submission.languageSwitch"
                    values={{
                      language: (
                        <FormattedMessage
                          id={`talk.language.${otherLanguage}`}
                        />
                      ),
                    }}
                  />
                </Text>
                <Button
                  size="small"
                  variant="secondary"
                  onClick={(_) => {
                    setViewInLanguage(otherLanguage);
                  }}
                >
                  <FormattedMessage
                    id="profile.myProposals.viewIn"
                    values={{
                      language: (
                        <FormattedMessage
                          id={`talk.language.${otherLanguage}`}
                        />
                      ),
                    }}
                  />
                </Button>
              </>
            )}
          </VerticalStack>
        }
      />
    </Page>
  );
};

export const getServerSideProps: GetServerSideProps = async ({
  req,
  locale,
  params,
}) => {
  const client = getApolloClient(null, req.cookies);

  const [_, englishSubmission, italianSubmission] = await Promise.all([
    prefetchSharedQueries(client, locale),
    queryIsVotingClosed(client, {
      conference: process.env.conferenceCode,
    }),
    querySubmission(client, {
      id: params.id as string,
      language: "en",
    }),
    querySubmission(client, {
      id: params.id as string,
      language: "it",
    }),
  ]);

  if (!englishSubmission && !italianSubmission) {
    return {
      notFound: true,
    };
  }

  return addApolloState(
    client,
    {
      props: {},
    },
    null,
  );
};

export default SubmissionPage;
