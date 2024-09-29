import { Snake4 } from "@python-italia/pycon-styleguide/illustrations";

export function CommunityPage() {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm] relative h-screen">
      <h1 className="text-xl font-bold">Community</h1>

      <img
        className="w-full border-4 border-black aspect-[9/12] object-cover"
        src="https://live.staticflickr.com/65535/53774457009_168efb54ef_h.jpg"
      />

      <p className="bg-blue border-4 border-black px-[1cm] py-[0.5cm] absolute w-[65%] top-[4cm] left-[1cm]">
        PyCon Italia is aimed at everyone in the Python community, of all skill
        levels, both users and programmers. It is a great meeting event: ~800
        attendees are expected from all over the world. Professionals, companies
        and students will meet for learning, collaborate and grow together. The
        delegates are a mix of Python users and developers (~60%), students
        (~20%), PMs (~8%), researchers (~7%), CTOs (~5%) as well as individuals
        whose businesses rely on the use of Python.
      </p>

      <Snake4 className="size-[4cm] absolute right-[1cm] bottom-[2cm] border-black border-4" />
    </div>
  );
}
