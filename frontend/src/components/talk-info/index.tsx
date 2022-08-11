/** @jsxRuntime classic */

/** @jsx jsx */
import { FormattedMessage, FormattedPlural } from "react-intl";
import FormattedDuration from "react-intl-formatted-duration";
import { Box, Flex, jsx, Text } from "theme-ui";

import { BlogPostIllustration } from "../illustrations/blog-post";

type Props = {
  talk: {
    speakers: { fullName: string }[];
    image?: string;
    audienceLevel?: string;
    topic?: string;
    duration?: number;
    language: {
      code: string;
    };
  };
};

const InfoLine = ({
  label,
  children,
  ...props
}: {
  label: React.ReactChild;
  children: React.ReactChild;
}) => {
  return (
    <Box sx={{ mb: 2 }}>
      <Text sx={{ fontWeight: "bold" }}>{label}</Text>

      <Text>{children}</Text>
    </Box>
  );
};

export const TalkInfo = ({ talk }: Props) => {
  return (
    <Flex
      sx={{
        position: "relative",
        justifyContent: "flex-end",
        alignItems: "flex-start",
        flexDirection: "column",
      }}
    >
      <BlogPostIllustration
        sx={{
          width: "80%",
          position: "relative",
          right: "-20%",
          display: ["none", "none", "block"],
        }}
      />

      <Box
        sx={{
          border: "primary",
          p: 4,
          backgroundColor: "cinderella",
          width: ["100%", "100%", "80%"],
          mt: [0, 0, -100],
          mb: [0, 0, -50],
          position: "relative",
        }}
      >
        {talk.speakers.length > 0 && (
          <InfoLine
            label={
              <FormattedMessage
                values={{
                  count: talk.speakers.length,
                }}
                id="talk.speaker"
              />
            }
          >
            {talk.speakers.map(({ fullName }) => fullName).join(" & ")}
          </InfoLine>
        )}

        {talk.topic ? (
          <InfoLine label={<FormattedMessage id="cfp.trackLabel" />}>
            {talk.topic}
          </InfoLine>
        ) : null}

        {talk.audienceLevel ? (
          <InfoLine label={<FormattedMessage id="cfp.audienceLevelLabel" />}>
            {talk.audienceLevel}
          </InfoLine>
        ) : null}

        <InfoLine label={<FormattedMessage id="talk.language" />}>
          <FormattedMessage id={`talk.language.${talk.language.code}`} />
        </InfoLine>

        {talk.duration ? (
          <InfoLine label={<FormattedMessage id="talk.duration" />}>
            <FormattedDuration seconds={talk.duration * 60} />
          </InfoLine>
        ) : null}
      </Box>
    </Flex>
  );
};
