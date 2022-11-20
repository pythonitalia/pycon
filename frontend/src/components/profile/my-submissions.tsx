/** @jsxRuntime classic */

/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { Link } from "~/components/link";
import { Table } from "~/components/table";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useMySubmissionsQuery } from "~/types";

type Props = {
  className?: string;
};

export const MySubmissions = ({ className }: Props) => {
  const language = useCurrentLanguage();
  const { loading, error, data } = useMySubmissionsQuery({
    variables: {
      conference: process.env.conferenceCode,
      language,
    },
  });

  const titleHeader = useTranslatedMessage("cfp.title");
  const formatHeader = useTranslatedMessage("cfp.format");
  const viewSubmissionHeader = useTranslatedMessage("cfp.viewSubmission");

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
          my: 5,
        }}
      >
        <Heading mb={5} as="h2" sx={{ fontSize: 5 }}>
          <FormattedMessage id="profile.mySubmissionsHeader" />
        </Heading>

        {error && <Alert variant="alert">{error.message}</Alert>}

        {data && (
          <Table
            headers={[titleHeader, formatHeader, ""]}
            mobileHeaders={[titleHeader, formatHeader, ""]}
            data={data!.me.submissions}
            keyGetter={(item) => item.id}
            rowGetter={(item) => [
              item.title,
              item.type.name,
              <Link
                key="openSubmission"
                path={`/submission/${item.id}`}
                sx={{
                  textDecoration: "underline",
                }}
              >
                {viewSubmissionHeader}
              </Link>,
            ]}
          />
        )}
      </Box>
    </Box>
  );
};
