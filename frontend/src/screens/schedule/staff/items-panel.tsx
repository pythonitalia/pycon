/** @jsx jsx */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Flex, Heading, Input } from "@theme-ui/components";
import React, { useCallback, useLayoutEffect, useState } from "react";
import { jsx } from "theme-ui";

import { AllTracksEvent, Submission } from "../events";

type ItemsPanelProp = {
  submissions: {
    title: string;
    id: string;
    duration: { duration: number } | null;
  }[];
};

export const ItemsPanel: React.SFC<ItemsPanelProp> = ({ submissions }) => {
  const [query, setQuery] = useState("");

  // TODO: https://fusejs.io/
  const filteredSubmissions = submissions.filter(submission =>
    submission.title.toLowerCase().includes(query),
  );

  return (
    <Box
      sx={{
        position: "fixed",
        bottom: 0,
        top: 0,
        right: 0,
        zIndex: 100,
        width: 300,
        borderLeft: "primary",
        background: "white",
        overflowX: "scroll",
      }}
    >
      <Heading sx={{ pt: 4, px: 4 }}>Submissions</Heading>

      <Box sx={{ p: 4 }}>
        <Input
          type="search"
          placeholder="Filter submissions"
          value={query}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setQuery(e.target.value)
          }
          sx={{ mb: 4 }}
        />
        {filteredSubmissions.map(({ id, title, duration }) => (
          <Submission
            key={id}
            id={id}
            title={title}
            duration={duration!.duration}
            sx={{ mb: 3 }}
          />
        ))}

        <AllTracksEvent />
      </Box>
    </Box>
  );
};
