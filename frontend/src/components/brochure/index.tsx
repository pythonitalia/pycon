import { CoverPage } from "./cover-page";
import { LocationPage } from "./location-page";
import { OptionsPage } from "./options-page";
import { OverviewPage } from "./overview-page";
import { Benefit, Package, PricingPage } from "./pricing-page";
import { TestimonialsPage } from "./testimonial-page";
import { BackCoverPage } from "./backcover-page";
import { CommunityPage } from "./community-page";
import { WhySponsorPage } from "./why-sponsor-page";

export type { Package, Benefit } from "./pricing-page";

export function Brochure({
  conference,
  packages,
  benefits,
  sponsorshipOptions,
  specialOptions,
  testimonials,
}: {
  conference: {
    name: string;
    start: string;
    end: string;
  };
  packages: Package[];
  benefits: Benefit[];
  sponsorshipOptions: Array<{ name: string; description: string }>;
  specialOptions: Array<{ name: string; description: string; price: number }>;
  testimonials: Array<{ text: string; author: string }>;
}) {
  return (
    <div className="brochure-page">
      <CoverPage conference={conference} />

      <OverviewPage
        conference={conference}
        attendees={1000}
        speakers={100}
        talks={200}
        onlineVisitors={5000}
        sponsors={50}
        grants={10}
        coffees={1000}
      />
      <LocationPage />
      <CommunityPage />
      <WhySponsorPage />
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
