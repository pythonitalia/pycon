import { CoverPage } from "./cover-page";
import { LocationPage } from "./location-page";
import { OptionsPage } from "./options-page";
import { OverviewPage } from "./overview-page";
import { Benefit, Package, PricingPage } from "./pricing-page";
import { TestimonialsPage } from "./testimonial-page";
import { BackCoverPage } from "./backcover-page";
import { CommunityPage } from "./community-page";
import { WhySponsorPage } from "./why-sponsor-page";

import type { useGetBrochureDataQuery } from "~/types";

export function Brochure({
  conference,
  testimonials,
  content,
}: {
  conference: ReturnType<typeof useGetBrochureDataQuery>["data"]["conference"];
  testimonials: Array<{ text: string; author: string }>;
  content: {
    stats: {
      attendees: string;
      speakers: string;
      talks: string;
      uniqueOnlineVisitors: string;
      sponsorsAndPartners: string;
      grantsGiven: string;
      coffees: string;
    };
    introduction: string;
    tags: string;
    location: {
      city: string;
      cityDescription: string;
      country: string;
      countryDescription: string;
      imageUrl: string;
    };
    community: string;
    whySponsor: { introduction: string; text: string };
  };
}) {
  return (
    <div className="brochure-page">
      <CoverPage conference={conference} content={content} />

      <OverviewPage content={content} conference={conference} />
      <LocationPage location={content.location} />

      <CommunityPage community={content.community} />
      <WhySponsorPage whySponsor={content.whySponsor} />
      <PricingPage
        levels={conference.sponsorLevels}
        benefits={conference.sponsorBenefits}
      />
      <OptionsPage
        options={conference.sponsorBenefits}
        title="Options"
        background="bg-yellow"
      />
      <OptionsPage
        options={conference.sponsorSpecialOptions}
        title="Special Options"
        background="bg-green"
      />
      <TestimonialsPage testimonials={testimonials} />
      <BackCoverPage />
    </div>
  );
}
