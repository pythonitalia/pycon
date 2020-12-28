/** @jsxRuntime classic */
/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { Link } from "~/components/link";
import { Table } from "~/components/table";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useMySubmissionsQuery } from "~/types";

type Props = {
  className?: string;
};

export const MySubmissions: React.FC<Props> = ({ className }) => {
  const { loading, error, data } = useMySubmissionsQuery({
    variables: {
      conference: process.env.conferenceCode,
    },
  });

  const topicHeader = useTranslatedMessage("cfp.topicLabel");
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
          mt: 4,
        }}
      >
        <Heading mb={4} as="h2" sx={{ fontSize: 5 }}>
          <FormattedMessage id="profile.mySubmissionsHeader" />
        </Heading>

        {error && <Alert variant="alert">{error.message}</Alert>}

        {data && (
          <Table
            headers={[titleHeader, topicHeader, formatHeader, ""]}
            mobileHeaders={[titleHeader, topicHeader, formatHeader, ""]}
            data={data!.me.submissions}
            keyGetter={(item) => item.id}
            rowGetter={(item) => [
              item.title,
              item.topic.name,
              item.type.name,
              <Link key="openSubmission" path={`/[lang]/submission/${item.id}`}>
                {viewSubmissionHeader}
              </Link>,
            ]}
          />
        )}
      </Box>
    </Box>
  );
};
