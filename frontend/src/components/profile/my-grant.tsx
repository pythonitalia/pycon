/** @jsxRuntime classic */

/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { Link } from "~/components/link";
import { useMyGrantQuery } from "~/types";

type Props = {
  className?: string;
};

export const MyGrant = ({ className }: Props) => {
  const { loading, error, data } = useMyGrantQuery({
    variables: {
      conference: process.env.conferenceCode,
    },
  });

  if (loading) {
    return null;
  }

  if (!error && data!.me!.grant === undefined) {
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
        {error && <Alert variant="alert">{error.message}</Alert>}

        {data && (
          <Alert varinat="alert">
            <FormattedMessage
              id="grants.alreadySubmitted"
              values={{
                linkGrant: (
                  <Link
                    path={`/grant/${data.me.grant.id}`}
                    sx={{
                      textDecoration: "underline",
                    }}
                  >
                    <FormattedMessage id="grants.alreadySubmitted.linkGrant.text" />
                  </Link>
                ),
              }}
            />
          </Alert>
        )}
      </Box>
    </Box>
  );
};
