import { CoverLogo } from "./cover-logo";

export function BackCoverPage() {
  return (
    <div className="page bg-yellow flex flex-col gap-[1cm] p-[2cm]">
      <CoverLogo className="size-[4cm]" />

      <h1 className="text-xl font-bold">PyCon Italia</h1>

      <div className="flex flex-col gap-[0.2cm] text-md font-medium">
        <p>
          <span className="inline-block mr-2">📞</span> +39 3495577593
        </p>
        <p>
          <span className="inline-block mr-2">📧</span>{" "}
          <a className="font-medium" href="mailto:sponsor@pycon.it">
            sponsor@pycon.it
          </a>
        </p>
        <p>
          <span className="inline-block mr-2">🌐</span>{" "}
          <a className="font-medium" href="https://pycon.it">
            https://pycon.it
          </a>
        </p>
      </div>
    </div>
  );
}
