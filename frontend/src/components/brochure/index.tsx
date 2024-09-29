import { CoverPage } from "./cover-page";
import { LocationPage } from "./location-page";
import { OptionsPage } from "./options-page";
import { OverviewPage } from "./overview-page";
import { Benefit, Package, PricingPage } from "./pricing-page";
import { TestimonialsPage } from "./testimonial-page";
import { BackCoverPage } from "./backcover-page";
import { CommunityPage } from "./community-page";
import { WhySponsorPage } from "./why-sponsor-page";

import { useGetBrochureDataQuery } from "~/types";

export type { Package, Benefit } from "./pricing-page";

export function Brochure({
  conference,
  packages,
  benefits,
  sponsorshipOptions,
  specialOptions,
  testimonials,
}: {
  conference: ReturnType<typeof useGetBrochureDataQuery>["data"]["conference"];
  packages: Package[];
  benefits: Benefit[];
  sponsorshipOptions: Array<{ name: string; description: string }>;
  specialOptions: Array<{ name: string; description: string; price: number }>;
  testimonials: Array<{ text: string; author: string }>;
}) {
  if (!conference.sponsorBrochure) {
    throw new Error("No sponsor brochure data found");
  }

  return (
    <div className="brochure-page">
      <CoverPage conference={conference} />

      <OverviewPage
        brochure={conference.sponsorBrochure}
        conference={conference}
      />
      <LocationPage location={conference.sponsorBrochure.location} />

      <CommunityPage community={conference.sponsorBrochure.community} />
      <WhySponsorPage whySponsor={conference.sponsorBrochure.whySponsor} />
      <PricingPage packages={packages} benefits={benefits} />
      <OptionsPage
        options={sponsorshipOptions}
        title="Options"
        background="bg-yellow"
      />
      <OptionsPage
        options={specialOptions}
        title="Special Options"
        background="bg-green"
      />
      <TestimonialsPage testimonials={testimonials} />
      <BackCoverPage />
    </div>
  );
}
