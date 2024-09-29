import { Snake1 } from "@python-italia/pycon-styleguide/illustrations";
import { Logo } from "../logo";

export function BackCoverPage() {
  return (
    <div className="page bg-yellow flex flex-col gap-[1cm] p-[2cm]">
      <div>
        <Snake1 className="size-[4cm] border-[2px] border-black bg-purple border-b-0" />
        <Logo className="w-[4cm]" />
      </div>

      <h1 className="text-xl font-bold">PyCon Italia</h1>

      <div className="flex flex-col gap-[0.2cm] text-md font-medium">
        <p>
          <span className="inline-block mr-2">📞</span> +39 3495577593
        </p>
        <p>
          <span className="inline-block mr-2">📧</span> info@pycon.it
        </p>
        <p>
          <span className="inline-block mr-2">🌐</span> https://pycon.it
        </p>
      </div>
    </div>
  );
}
