import { SnakeDNA } from "@python-italia/pycon-styleguide/illustrations";

export function WhySponsorPage() {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm] relative h-screen">
      <h1 className="text-xl font-bold">Why sponsor PyCon Italia?</h1>

      <p className="bg-purple border-4 border-black px-[1cm] py-[0.5cm] absolute w-[45%] top-[5cm] left-[1cm]">
        The very first reason is to help the community around this environment
        to grow. Sponsors are what make this conference possible. From low
        ticket prices to financial aid, to video recording, the organizations
        who step forward to support PyCon Italia, in turn, support the entire
        Python community.
      </p>

      <SnakeDNA className="size-[4cm] absolute border-black border-4 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />

      <p className="bg-pink border-4 border-black px-[0.5cm] py-[0.5cm] absolute w-[40%] bottom-[3cm] right-[1cm]">
        Advertising your brand in a very targeted audience like this gives back
        a high increase of its awareness.
        <br />
        <br />
        Moreover, many of our sponsoring services have turned towards the
        increased recruiting requests we got in the last years, that’s why you
        can find several ways of engage potential candidates for the position
        you are looking for in our event.
      </p>
    </div>
  );
}
