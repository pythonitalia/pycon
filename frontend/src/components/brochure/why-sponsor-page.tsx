import { SnakeDNA } from "@python-italia/pycon-styleguide/illustrations";
import { compile } from "~/helpers/markdown";

export function WhySponsorPage({
  whySponsor,
}: {
  whySponsor: { introduction: { text: string }; text: string };
}) {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm] relative h-screen">
      <h1 className="text-xl font-bold">Why sponsor PyCon Italia?</h1>

      <p className="bg-purple border-4 border-black px-[1cm] py-[0.5cm] absolute w-[45%] top-[5cm] left-[1cm]">
        {compile(whySponsor.introduction.text).tree}
      </p>

      <SnakeDNA className="size-[4cm] absolute border-black border-4 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />

      <p className="bg-pink border-4 border-black px-[0.5cm] py-[0.5cm] absolute w-[40%] bottom-[3cm] right-[1cm]">
        {compile(whySponsor.text).tree}
      </p>
    </div>
  );
}
