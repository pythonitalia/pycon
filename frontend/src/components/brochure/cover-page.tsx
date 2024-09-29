import { HeroIllustrationBologna } from "@python-italia/pycon-styleguide";
import { format, parseISO } from "date-fns";
import { Logo } from "~/components/logo";

export function CoverPage({
  conference,
}: {
  conference: {
    name: string;
    start: string;
    end: string;
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
      <div className="grid grid-cols-[1fr,2fr] gap-4 px-[2cm]">
        <Logo />
        <h1 className="text-2xl font-medium relative top-[-0.5cm]">
          Sponsorship Opportunities
        </h1>
      </div>

      <div className="w-full aspect-[8/5] border-[4px] [&>div>div]:scale-50 [&>div>div]:-translate-x-16 [&>div>div]:origin-bottom">
        {/* TODO: this should be based on location */}
        <HeroIllustrationBologna cycle="day" />
      </div>

      <div className="text-right px-[2cm] font-medium">
        <p>{date}</p>
        {/* TODO: add location */}
        <p>Bologna, Italy</p>
        <p>
          <a href="https://pycon.it" className="no-underline font-medium">
            https://pycon.it
          </a>
        </p>
      </div>
    </div>
  );
}
