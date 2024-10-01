import { HeroIllustrationBologna } from "@python-italia/pycon-styleguide";
import { format, parseISO } from "date-fns";
import { Logo } from "~/components/logo";
import { CoverLogo } from "./cover-logo";

export function CoverPage({
  conference,
  content,
}: {
  conference: {
    name: string;
    start: string;
    end: string;
  };
  content: {
    location: {
      city: string;
      country: string;
    };
  };
}) {
  const start = parseISO(conference.start);
  const end = parseISO(conference.end);

  // TODO: add support for dates that start in a month and end in another
  if (start.getMonth() !== end.getMonth()) {
    throw new Error("Unsupported date range, see TODO");
  }

  // we want to show Start Day(th) - End Day(th) Month Year
  // e.g. 2nd - 5th June 2022
  const formattedStart = format(start, "do");
  const formattedEnd = format(end, "do");
  const formattedMonth = format(start, "MMMM yyyy");

  const date = `${formattedStart} - ${formattedEnd} ${formattedMonth}`;

  return (
    <div className="page bg-purple flex flex-col gap-[2cm]">
      <div className="grid grid-cols-[1fr,2fr] gap-[1cm] px-[2cm]">
        <CoverLogo className="size-[5cm]" />
        <h1 className="text-2xl font-medium relative top-[-0.5cm]">
          Sponsorship Opportunities
        </h1>
      </div>

      <div className="w-full aspect-[8/5] border-[4px] border-b-[4px] [&>div>div]:scale-50 [&>div>div]:translate-y-[4px] [&>div>div]:-translate-x-16 [&>div>div]:origin-bottom relative">
        <HeroIllustrationBologna cycle="day" />
        <Logo className="absolute bottom-[-0.8cm] left-[2cm] w-[5cm] h-auto" />
      </div>

      <div className="text-right px-[2cm] font-medium">
        <p>{date}</p>
        {/* TODO: add location */}
        <p>
          {content.location.city}, {content.location.country}
        </p>
        <p>
          <a href="https://pycon.it" className="no-underline font-medium">
            https://pycon.it
          </a>
        </p>
      </div>
    </div>
  );
}
