import { Snake1 } from "@python-italia/pycon-styleguide/illustrations";

export function OverviewPage({
  conference,
  attendees,
  speakers,
  talks,
  onlineVisitors,
  sponsors,
  grants,
  coffees,
}: {
  conference: {
    name: string;
  };
  attendees: number;
  speakers: number;
  talks: number;
  onlineVisitors: number;
  sponsors: number;
  grants: number;
  coffees: number;
}) {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm]">
      <h1 className="text-xl font-bold">Don’t miss {conference.name}!</h1>

      <div className="bg-yellow border-4 border-black px-[1cm] py-[0.5cm]">
        <div className="grid grid-cols-4 gap-4">
          <div>
            <p className="text-xl font-medium">{attendees}+</p>
            <p>attendees</p>
          </div>
          <div>
            <p className="text-xl font-medium">{speakers}+</p>
            <p>speakers</p>
          </div>
          <div>
            <p className="text-xl font-medium">{talks}+</p>
            <p>talks</p>
          </div>
          <div>
            <p className="text-xl font-medium">{onlineVisitors}+</p>
            <p>unique online streaming visitors</p>
          </div>

          <div>
            <p className="text-xl font-medium">{sponsors}+</p>
            <p>sponsors & partners</p>
          </div>
          <div>
            <p className="text-xl font-medium">{grants}+</p>
            <p>grants given</p>
          </div>
          <div>
            <p className="text-xl font-medium">{coffees}+</p>
            <p>coffees</p>
          </div>
        </div>
      </div>

      <div className="bg-pink border-4 border-black px-[1cm] py-[0.5cm] space-y-[0.5cm]">
        <p>
          <strong>PyCon Italia</strong> is the official Italian event about
          Python but nowadays it's one of the most important pythonic events in
          all Europe. More than 800 people gather from all over the world to
          attend, learn, code, speak, support and meet other fellow pythonistas
          in Florence.
        </p>
        <p>
          Our care for the quality of every aspect of PyCon Italia results in a
          wonderful gathering for growing together.
        </p>
        <p>
          This year, PyCon Italia is at its 14th edition and we'll try to make
          it an unforgettable and even more great experience for everyone.
        </p>
      </div>

      <div className="grid grid-cols-[3fr,minmax(0,1fr)] gap-[0.5cm]">
        <div className="bg-green border-4 border-black px-[1cm] py-[0.5cm] space-y-[0.5cm]">
          <p className="font-bold">
            BEGINNERS’ & DJANGOGIRLS — WORKSHOPS NETWORKING — RECRUITING SESSION
            SOCIAL DINNER & EVENTS SPEAKERS & ATTENDEES FROM ALL OVER THE WORLD
            CARE FOR DIVERSITY AND INCLUSION PRIZES AND CHALLENGES SPRINTS —
            CHILDCARE — GREEN
          </p>
        </div>

        <Snake1 className="border-4 border-black aspect-square w-full h-full bg-purple" />
      </div>
    </div>
  );
}
