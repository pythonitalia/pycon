/** @jsx jsx */
import { Box, Heading, Input } from "@theme-ui/components";
import React, { useState } from "react";
import { jsx } from "theme-ui";

import { AllTracksEvent, CustomEvent, Submission } from "../events";

type ItemsPanelProp = {
  submissions: {
    title: string;
    id: string;
    duration: { duration: number } | null;
    type: { name: string };
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
        p: 4,
        borderLeft: "primary",
        background: "white",
        overflowX: "scroll",
      }}
    >
      <Heading sx={{ mb: 4 }}>Special items</Heading>

      <AllTracksEvent sx={{ mb: 4, width: "100%" }} />
      <CustomEvent sx={{ mb: 4, width: "100%" }} />

      <Heading sx={{ mb: 4 }}>Submissions</Heading>

      <Box>
        <Input
          type="search"
          placeholder="Filter submissions"
          value={query}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setQuery(e.target.value)
          }
          sx={{ mb: 4 }}
        />
        {filteredSubmissions.map(({ id, title, type, duration }) => (
          <Submission
            type={type.name}
            key={id}
            id={id}
            title={title}
            duration={duration!.duration}
            sx={{ mb: 3, width: "100%" }}
          />
        ))}
      </Box>
    </Box>
  );
};
