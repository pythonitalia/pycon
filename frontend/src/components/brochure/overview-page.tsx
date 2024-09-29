import { Snake1 } from "@python-italia/pycon-styleguide/illustrations";
import { compile } from "~/helpers/markdown";

export function OverviewPage({
  conference,
  brochure,
}: {
  conference: {
    name: string;
  };
  brochure: {
    introduction: {
      text: string;
    };
    tags: { text: string };
    stats: {
      attendees: string;
      speakers: string;
      talks: string;
      uniqueOnlineVisitors: string;
      sponsorsAndPartners: string;
      grantsGiven: string;
      coffees: string;
    };
  };
}) {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm]">
      <h1 className="text-xl font-bold">Don’t miss {conference.name}!</h1>

      <div className="bg-yellow border-4 border-black px-[1cm] py-[0.5cm]">
        <div className="grid grid-cols-4 gap-4">
          <div>
            <p className="text-xl font-medium">{brochure.stats.attendees}</p>
            <p>attendees</p>
          </div>
          <div>
            <p className="text-xl font-medium">{brochure.stats.speakers}</p>
            <p>speakers</p>
          </div>
          <div>
            <p className="text-xl font-medium">{brochure.stats.talks}</p>
            <p>talks</p>
          </div>
          <div>
            <p className="text-xl font-medium">
              {brochure.stats.uniqueOnlineVisitors}
            </p>
            <p>unique online streaming visitors</p>
          </div>

          <div>
            <p className="text-xl font-medium">
              {brochure.stats.sponsorsAndPartners}
            </p>
            <p>sponsors & partners</p>
          </div>
          <div>
            <p className="text-xl font-medium">{brochure.stats.grantsGiven}</p>
            <p>grants given</p>
          </div>
          <div>
            <p className="text-xl font-medium">{brochure.stats.coffees}</p>
            <p>coffees</p>
          </div>
        </div>
      </div>

      <div className="bg-pink border-4 border-black px-[1cm] py-[0.5cm] space-y-[0.5cm]">
        {compile(brochure.introduction.text).tree}
      </div>

      <div className="grid grid-cols-[3fr,minmax(0,1fr)] gap-[0.5cm]">
        <div className="bg-green border-4 border-black px-[1cm] py-[0.5cm] space-y-[0.5cm]">
          <p className="font-bold">{brochure.tags.text}</p>
        </div>

        <Snake1 className="border-4 border-black aspect-square w-full h-full bg-purple" />
      </div>
    </div>
  );
}
