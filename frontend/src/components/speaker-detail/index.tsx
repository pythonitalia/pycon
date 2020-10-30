/** @jsx jsx */

import { Fragment } from "react";
import { Box, Grid, jsx } from "theme-ui";

import { AvatarPlaceholder } from "~/components/icons/avatar-placeholder";

const SpeakerInfoRow: React.SFC<{
  title: string | React.ReactElement;
  value: string;
}> = ({ title, value }) => (
  <Fragment>
    <dt
      sx={{ color: "violet", textTransform: "uppercase", fontWeight: "bold" }}
    >
      {title}:
    </dt>
    <dd>{value}</dd>

    <Box
      sx={{
        borderBottom: "primary",
        borderColor: "violet",
        gridColumnStart: 1,
        gridColumnEnd: -1,
      }}
    />
  </Fragment>
);

export const SpeakerDetail: React.SFC<{ speaker: { fullName: string } }> = ({
  speaker,
}) => {
  const Avatar = AvatarPlaceholder; // TODO: check speaker image

  return (
    <Fragment key={speaker.fullName}>
      <Box
        sx={{
          width: "100%",
          position: "relative",
          mb: 3,
          border: "primary",
          overflow: "hidden",
          "&::after": {
            content: "''",
            display: "inline-block",
            width: "100%",
            paddingTop: "100%",
          },
        }}
      >
        <Avatar
          style={{
            width: "auto",
            height: "100%",
            position: "absolute",
            top: 0,
            left: 0,
          }}
        />
      </Box>

      <Box>
        <Grid
          as="dl"
          sx={{
            gridTemplateColumns: "1fr 2fr",
          }}
        >
          <SpeakerInfoRow title={"Speaker name"} value={speaker.fullName} />
        </Grid>
      </Box>
    </Fragment>
  );
};
