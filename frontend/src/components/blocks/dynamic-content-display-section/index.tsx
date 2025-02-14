import React, { Fragment } from "react";
import {
  DynamicContentDisplaySectionSource,
  queryAcceptedProposals,
  queryKeynotesSection,
} from "~/types";
import { AcceptedProposalsContent } from "./accepted-proposals-content";
import { KeynotersContent } from "./keynoters-content";
import { SpeakersContent } from "./speakers-content";

export const DynamicContentDisplaySection = ({
  source,
}: {
  source: string;
}) => {
  return (
    <Fragment>
      {source === DynamicContentDisplaySectionSource.Keynoters && (
        <KeynotersContent />
      )}
      {source === DynamicContentDisplaySectionSource.Speakers && (
        <SpeakersContent />
      )}
      {source === DynamicContentDisplaySectionSource.AcceptedProposals && (
        <AcceptedProposalsContent />
      )}
    </Fragment>
  );
};

DynamicContentDisplaySection.dataFetching = (client, language, block) => {
  const source = block.source;

  switch (source) {
    case DynamicContentDisplaySectionSource.Keynoters: {
      return [
        queryKeynotesSection(client, {
          code: process.env.conferenceCode,
          language,
        }),
      ];
    }
    case DynamicContentDisplaySectionSource.Speakers: {
      return [
        queryAcceptedProposals(client, {
          code: process.env.conferenceCode,
          language,
        }),
      ];
    }
    case DynamicContentDisplaySectionSource.AcceptedProposals: {
      return [
        queryAcceptedProposals(client, {
          code: process.env.conferenceCode,
          language,
        }),
      ];
    }
  }

  return [];
};
