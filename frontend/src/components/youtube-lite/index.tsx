/** @jsx jsx */
import { Box, Flex } from "@theme-ui/components";
import React, { useState } from "react";
import { jsx } from "theme-ui";

import { ArrowIcon } from "../icons/arrow";

export const YouTubeLite: React.SFC<{ videoId: string }> = ({
  videoId,
  ...props
}) => {
  videoId = encodeURIComponent(videoId);
  const posterUrl = `https://i.ytimg.com/vi/${videoId}/maxresdefault.jpg`;

  const [playing, setPlaying] = useState(true);

  if (playing) {
    return (
      <iframe
        width="560"
        height="315"
        frameBorder="0"
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen={true}
        src={`https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1`}
        {...props}
      />
    );
  }

  // TODO: add connection warming on hover

  return (
    <Flex
      sx={{
        background: `black url(${posterUrl})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        justifyContent: "center",
        alignItems: "center",
        cursor: "pointer",
      }}
      {...props}
    >
      <Box onClick={() => setPlaying(true)}>
        <ArrowIcon
          direction="right"
          sx={{ fill: "violet", width: 60, strokeWidth: "6px" }}
          viewBox="6 6 54 65"
        />
      </Box>
    </Flex>
  );
};
