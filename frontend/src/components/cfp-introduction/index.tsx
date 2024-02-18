/** @jsxRuntime classic */

/** @jsx jsx */
import { Link } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";
import { Box, Grid, Heading, Text, jsx } from "theme-ui";

import { CFPIllustration } from "~/components/illustrations/cfp";
import { formatDeadlineDateTime } from "~/helpers/deadlines";
import { useCurrentLanguage } from "~/locale/context";

import { createHref } from "../link";

export const Introduction = ({ deadline }: { deadline?: string }) => {
  const language = useCurrentLanguage();
  return (
    <Box
      sx={{
        borderTop: "primary",
        borderBottom: "primary",
      }}
    >
      <Grid
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
          my: 5,
          gridTemplateColumns: [null, null, "9fr 3fr 8fr"],
        }}
      >
        <Box>
          <Heading as="h1">
            <FormattedMessage id="cfp.introductionHeading" />
          </Heading>
          <Text
            as="p"
            sx={{
              color: "orange",
              mt: 4,
              fontSize: 2,
            }}
          >
            <FormattedMessage id="cfp.introductionSubtitle" />
          </Text>
          <Text
            sx={{
              mt: 4,
              fontSize: 2,
            }}
            as="p"
          >
            <FormattedMessage id="cfp.introductionCopy" />
          </Text>

          {deadline && (
            <Text
              sx={{
                fontSize: 2,
              }}
              as="p"
            >
              <FormattedMessage
                id="cfp.introductionDeadline"
                values={{
                  deadline: (
                    <Text as="span" sx={{ fontWeight: "bold" }}>
                      {formatDeadlineDateTime(deadline, language)}
                    </Text>
                  ),
                }}
              />
            </Text>
          )}

          <Link
            href={createHref({
              path: "/call-for-proposals",
              locale: language,
            })}
            className="mt-[4px]"
          >
            <FormattedMessage id="global.learnMore" />
          </Link>
        </Box>
        <Box
          sx={{
            gridColumnStart: [0, 0, 3],
          }}
        >
          <Box
            sx={{
              display: ["none", null, "block"],
              border: "primary",
              gridColumnStart: [0, 0, 3],
              backgroundColor: "#C4C4C4",
              position: "relative",
            }}
          >
            <Box sx={{ display: "inline-block", pt: "100%", width: "100%" }} />
            <CFPIllustration
              sx={{
                position: "absolute",
                top: 0,
                left: "-4px",
                width: "100%",
                height: "100%",
              }}
            />
          </Box>
        </Box>
      </Grid>
    </Box>
  );
};
