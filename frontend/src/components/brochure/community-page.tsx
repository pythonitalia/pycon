import { Snake4 } from "@python-italia/pycon-styleguide/illustrations";
import { compile } from "~/helpers/markdown";

export function CommunityPage({ community }: { community: { text: string } }) {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm] relative h-screen">
      <h1 className="text-xl font-bold">Community</h1>

      <img
        className="w-full border-4 border-black aspect-[9/12] object-cover"
        src="https://live.staticflickr.com/65535/53774457009_168efb54ef_h.jpg"
      />

      <p className="bg-blue border-4 border-black px-[1cm] py-[0.5cm] absolute w-[65%] top-[4cm] left-[1cm]">
        {compile(community.text).tree}
      </p>

      <Snake4 className="size-[4cm] absolute right-[1cm] bottom-[2cm] border-black border-4" />
    </div>
  );
}
