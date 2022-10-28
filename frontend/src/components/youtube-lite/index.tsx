/** @jsxRuntime classic */

/** @jsx jsx */
import React, { useState } from "react";
import { Box, Flex, jsx } from "theme-ui";

import { ArrowIcon } from "../icons/arrow";

export const YouTubeLite = ({
  videoId,
  ...props
}: {
  videoId: string;
  sx?: any;
}) => {
  videoId = encodeURIComponent(videoId);
  const posterUrl = `https://i.ytimg.com/vi/${videoId}/maxresdefault.jpg`;

  const [playing, setPlaying] = useState(false);

  if (playing) {
    return (
      <iframe
        width="560"
        height="315"
        frameBorder="0"
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen={true}
        src={`https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&modestbranding=1&rel=0`}
        {...props}
      />
    );
  }

  // TODO: add connection warming on hover

  return (
    <Flex
      onClick={() => setPlaying(true)}
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
      <Box>
        <ArrowIcon
          direction="right"
          sx={{ fill: "violet", width: 60, strokeWidth: "6px" }}
          viewBox="6 6 54 65"
        />
      </Box>
    </Flex>
  );
};
