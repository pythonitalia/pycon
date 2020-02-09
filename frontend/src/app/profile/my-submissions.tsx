/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { Box, Heading } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { Alert } from "../../components/alert";
import { Link } from "../../components/link";
import { useConference } from "../../context/conference";
import {
  MySubmissionsQuery,
  MySubmissionsQueryVariables,
} from "../../generated/graphql-backend";
import MY_SUBMISSIONS from "./my-submissions.graphql";

type Props = {
  className?: string;
};

export const MySubmissions: React.SFC<Props> = ({ className }) => {
  const { code } = useConference();
  const { loading, error, data } = useQuery<
    MySubmissionsQuery,
    MySubmissionsQueryVariables
  >(MY_SUBMISSIONS, {
    variables: {
      conference: code,
    },
  });

  if (loading) {
    return null;
  }

  if (!error && data!.me.submissions.length === 0) {
    return null;
  }

  return (
    <Box className={className}>
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          mt: 4,
        }}
      >
        <Heading mb={3} as="h2">
          <FormattedMessage id="profile.mySubmissionsHeader" />
        </Heading>

        {error && <Alert variant="alert">{error.message}</Alert>}

        {data && (
          <Box as="ul" sx={{ px: 3 }}>
            {data!.me.submissions.map(submission => (
              <li key={submission.id}>
                <Link href={`/:language/submission/${submission.id}`}>
                  {submission.title}
                </Link>
              </li>
            ))}
          </Box>
        )}
      </Box>
    </Box>
  );
};
