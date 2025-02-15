import React, { Fragment } from "react";
import {
  DynamicContentDisplaySectionSource,
  queryDynamicContentDisplaySectionProposals,
  queryKeynotesSection,
} from "~/types";
import { KeynotersContent } from "./keynoters-content";
import { ProposalsContent } from "./proposals-content";
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
      {source === DynamicContentDisplaySectionSource.Proposals && (
        <ProposalsContent />
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
        queryDynamicContentDisplaySectionProposals(client, {
          code: process.env.conferenceCode,
          language,
        }),
      ];
    }
    case DynamicContentDisplaySectionSource.Proposals: {
      return [
        queryDynamicContentDisplaySectionProposals(client, {
          code: process.env.conferenceCode,
          language,
        }),
      ];
    }
  }

  return [];
};
