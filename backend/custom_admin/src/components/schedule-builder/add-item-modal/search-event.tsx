import { Flex, Heading, Text, TextField } from "@radix-ui/themes";
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
      runSearch({
        variables: {
          conferenceId,
          query: debouncedSearch,
        },
      });
    }
  }, [debouncedSearch]);

  return (
    <Flex direction="column" gap="2">
      <Heading size="3">Search proposal / keynote</Heading>
      <TextField.Root
        ref={searchInputRef}
        onChange={changeSearch}
        placeholder="Search"
        value={searchQuery}
      />
      {loading && <Text color="gray">Searching events</Text>}
      {!loading &&
        debouncedSearch &&
        data?.searchEvents.results.length === 0 && (
          <Text color="gray">No events found</Text>
        )}
      {debouncedSearch && data?.searchEvents.results.length > 0 && (
        <Flex direction="column" gap="2">
          {data.searchEvents.results.map((event) => {
            if (event.__typename === "Submission") {
              return <ProposalPreview key={event.id} proposal={event} />;
            }

            if (event.__typename === "Keynote") {
              return <KeynotePreview key={event.id} keynote={event} />;
            }

            return null;
          })}
        </Flex>
      )}
    </Flex>
  );
};
