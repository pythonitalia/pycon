/** @jsx jsx */
import React, { useState } from "react";
import { Box, Heading, Input, jsx } from "theme-ui";

import { AllTracksEvent, CustomEvent, Submission } from "../events";
import { Submission as SubmissionType } from "../types";

type ItemsPanelProp = {
  submissions: SubmissionType[];
};

export const ItemsPanel: React.SFC<ItemsPanelProp> = ({ submissions }) => {
  const [query, setQuery] = useState("");

  // TODO: https://fusejs.io/
  const filteredSubmissions = submissions.filter((submission) =>
    submission.title.toLowerCase().includes(query),
  );

  return (
    <Box
      sx={
        {
          position: "fixed",
          bottom: 0,
          top: 0,
          right: 0,
          zIndex: "scheduleItemPanel",
          width: 300,
          p: 4,
          borderLeft: "primary",
          background: "white",
          overflowX: "scroll",
        } as any
      }
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
        {filteredSubmissions.map((submission) => (
          <Submission
            submission={submission}
            key={submission.id}
            sx={{ mb: 3, width: "100%" }}
          />
        ))}
      </Box>
    </Box>
  );
};
