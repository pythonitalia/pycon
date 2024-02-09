import { useState } from "react";

import { useCurrentConference } from "../../utils/conference";
import { KeynotePreview } from "./keynote-preview";
import { ProposalPreview } from "./proposal-preview";
import { useSearchEventsQuery } from "./search-events.generated";

export const SearchEvent = () => {
  const conferenceId = useCurrentConference();
  const [searchQuery, setSearchQuery] = useState("");
  const { data, loading } = useSearchEventsQuery({
    variables: { conferenceId, query: searchQuery },
    skip: !searchQuery,
    returnPartialData: true,
  });
  const changeSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };
  return (
    <>
      <div className="mb-2">
        <strong>Search proposal / keynote</strong>
      </div>
      <div>
        <input
          onChange={changeSearch}
          className="w-full p-3 border"
          type="text"
          placeholder="Search"
          value={searchQuery}
        />
      </div>
      <div>
        {loading && <span>Searching events</span>}
        {!loading && data?.searchEvents.length === 0 && (
          <span>No events found</span>
        )}
        {data?.searchEvents.length > 0 && (
          <ul>
            {data.searchEvents.map((event) => {
              if (event.__typename === "Proposal") {
                return <ProposalPreview key={event.id} proposal={event} />;
              }

              if (event.__typename === "Keynote") {
                return <KeynotePreview key={event.id} keynote={event} />;
              }
            })}
          </ul>
        )}
      </div>
    </>
  );
};
