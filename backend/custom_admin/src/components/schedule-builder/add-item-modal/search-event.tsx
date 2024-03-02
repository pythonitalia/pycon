import { useEffect, useRef, useState } from "react";

import { useCurrentConference } from "../../utils/conference";
import { useDebounce } from "../../utils/use-debounce";
import { KeynotePreview } from "./keynote-preview";
import { ProposalPreview } from "./proposal-preview";
import { useSearchEventsLazyQuery } from "./search-events.generated";

export const SearchEvent = () => {
  const searchInputRef = useRef<HTMLInputElement>(null);
  const { conferenceId } = useCurrentConference();

  const [searchQuery, setSearchQuery] = useState("");
  const debouncedSearch = useDebounce(searchQuery, 300);
  const [runSearch, { data, loading }] = useSearchEventsLazyQuery({
    returnPartialData: true,
  });

  const changeSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  useEffect(() => {
    if (!searchInputRef.current) {
      return;
    }
    searchInputRef.current.focus();
  }, []);

  useEffect(() => {
    if (debouncedSearch) {
      console.log("running search", debouncedSearch);

      runSearch({
        variables: {
          conferenceId,
          query: debouncedSearch,
        },
      });
    } else {
    }
  }, [debouncedSearch]);

  return (
    <>
      <div className="mb-2">
        <strong>Search proposal / keynote</strong>
      </div>
      <div>
        <input
          ref={searchInputRef}
          onChange={changeSearch}
          className="w-full p-3 border"
          type="text"
          placeholder="Search"
          value={searchQuery}
        />
      </div>
      <div>
        {loading && <span>Searching events</span>}
        {!loading && data?.searchEvents.results.length === 0 && (
          <span>No events found</span>
        )}
        {debouncedSearch && data?.searchEvents.results.length > 0 && (
          <ul>
            {data.searchEvents.results.map((event) => {
              if (event.__typename === "Submission") {
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
