/** @jsx jsx */
import { Box, Heading } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { Link } from "../../components/link";
import { MyProfileQuery } from "../../generated/graphql-backend";

export const MySubmissions: React.SFC<{ profile: MyProfileQuery }> = ({
  profile: {
    me: { submissions },
  },
}) => (
  <Box
    sx={{
      borderTop: "primary",
    }}
  >
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        my: 4,
        px: 3,
      }}
    >
      <Heading mb={2} as="h2">
        <FormattedMessage id="profile.mySubmissionsHeader" />
      </Heading>

      <Box as="ul" sx={{ px: 3 }}>
        {submissions.map(submission => (
          <li sx={{ mt: 3 }} key={submission.id}>
            <Link href={`/:language/submission/${submission.id}`}>
              {submission.title}
            </Link>
          </li>
        ))}
      </Box>
    </Box>
  </Box>
);
