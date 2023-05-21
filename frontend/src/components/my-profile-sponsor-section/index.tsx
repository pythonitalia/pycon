import {
  Button,
  Heading,
  Page,
  Section,
  Spacer,
} from "@python-italia/pycon-styleguide";
import { format, parseISO } from "date-fns";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useBadgeScansQuery } from "~/types";

import { MetaTags } from "../meta-tags";
import { Table } from "../table";
import { ExportBadgeScansButton } from "./export-button";

export const MyProfileSponsorSection = () => {
  const [currentPage, setCurrentPage] = React.useState(1);

  const { data, loading, fetchMore } = useBadgeScansQuery({
    variables: {
      conferenceCode: process.env.conferenceCode,
      page: 1,
      pageSize: 20,
    },
    notifyOnNetworkStatusChange: true,
  });

  const hasMore = data?.badgeScans.pageInfo.totalPages > currentPage;

  const handleFetchMore = async () => {
    await fetchMore({
      variables: {
        page: currentPage + 1,
      },
      updateQuery: (prev, { fetchMoreResult }) => {
        if (!fetchMoreResult) return prev;

        return {
          badgeScans: {
            ...fetchMoreResult.badgeScans,
            items: [
              ...prev.badgeScans.items,
              ...fetchMoreResult.badgeScans.items,
            ],
          },
        };
      },
    });
    setCurrentPage(currentPage + 1);
  };

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="profile.sponsorSection.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>

      <Section background="purple">
        <Heading size="display2">
          <FormattedMessage id="profile.sponsorSection" />
        </Heading>
      </Section>

      <Section>
        <Heading size="display2">
          <FormattedMessage id="profile.sponsorSection.badgeScans" />
        </Heading>

        <Spacer size="small" />

        {data?.badgeScans.items.length > 0 && (
          <>
            <ExportBadgeScansButton />
            <Spacer size="small" />

            <Table
              data={data.badgeScans.items}
              rowGetter={(item) => [
                format(parseISO(item.created), "dd MMM yyyy '@' HH:mm"),
                item.attendee.fullName,
                item.attendee.email,
                item.notes || "No notes",
              ]}
              keyGetter={(item) => item.id}
              cols={4}
            ></Table>
          </>
        )}
        {data?.badgeScans.items.length === 0 && !loading && (
          <p>
            <FormattedMessage id="profile.sponsorSection.noScan" />
          </p>
        )}

        {!data && loading && (
          <p>
            <FormattedMessage id="profile.sponsorSection.loading" />
          </p>
        )}

        <Spacer size="large" />

        <div>
          {hasMore && (
            <Button onClick={handleFetchMore} disabled={loading}>
              {loading ? (
                <FormattedMessage id="profile.sponsorSection.loading" />
              ) : (
                <FormattedMessage id="profile.sponsorSection.loadMore" />
              )}
            </Button>
          )}
        </div>
      </Section>
    </Page>
  );
};
