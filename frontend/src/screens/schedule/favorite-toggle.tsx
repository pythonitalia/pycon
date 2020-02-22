/** @jsx jsx */
import { Box, Button, Text } from "@theme-ui/components";
import React, { useCallback, useState } from "react";
import { jsx } from "theme-ui";

type Props = {
  itemId: string;
  myInterested: boolean;
};

export const FavoriteToggle: React.SFC<Props> = ({
  myInterested,
  ...props
}) => {
  const [favorited, setFavorited] = useState(myInterested);

  const toggleMyInterest = useCallback(
    e => {
      e.stopPropagation();
      console.log("click!");
      setFavorited(!favorited);
    },
    [favorited],
  );

  return (
    <Box>
      {favorited ? (
        <Button onClick={toggleMyInterest}>❤️</Button>
      ) : (
        <Button onClick={toggleMyInterest}>🖤</Button>
      )}
    </Box>
  );
};
