import { Button, Page, VerticalStack } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import type { GetServerSideProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { createHref } from "~/components/link";
import { ScheduleEventDetail } from "~/components/schedule-event-detail";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import NotFoundPage from "~/pages/404";
import { getType } from "~/pages/event/[slug]";
import {
  queryIsVotingClosed,
  querySubmission,
  useSubmissionQuery,
} from "~/types";

export const SubmissionPage = () => {
  const router = useRouter();

  const id = router.query.id as string;

  const {
    data: { submission },
  } = useSubmissionQuery({
    errorPolicy: "all",
    variables: {
      id,
    },
  });

  if (!submission) {
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
        language={submission.languages[0].code}
        audienceLevel={submission?.audienceLevel.name}
        startTime={null}
        endTime={null}
        speakers={submission?.speaker ? [submission.speaker] : null}
        bookable={false}
        spacesLeft={0}
        materials={submission?.materials}
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
                })}
              >
                <FormattedMessage id="profile.myProposals.edit" />
              </Button>
            ) : null}
          </VerticalStack>
        }
      />
    </Page>
  );
};

export const getServerSideProps: GetServerSideProps = async ({
  req,
  params,
}) => {
  const client = getApolloClient(null, req.cookies);

  const [_, __, submission] = await Promise.all([
    prefetchSharedQueries(client),
    queryIsVotingClosed(client, {
      conference: process.env.conferenceCode,
    }),
    querySubmission(client, {
      id: params.id as string,
    }),
  ]);

  if (!submission) {
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
