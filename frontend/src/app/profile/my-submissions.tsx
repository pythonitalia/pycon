/** @jsx jsx */

import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { Link } from "~/components/link";
import { useMySubmissionsQuery } from "~/types";

type Props = {
  className?: string;
};

export const MySubmissions: React.SFC<Props> = ({ className }) => {
  const { loading, error, data } = useMySubmissionsQuery({
    variables: {
      conference: process.env.conferenceCode,
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
            {data!.me.submissions.map((submission) => (
              <li key={submission.id}>
                <Link path={`/[lang]/submission/${submission.id}`}>
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
