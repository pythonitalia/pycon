import clsx from "clsx";
import { compile } from "~/helpers/markdown";
import { humanizeText } from "./utils";

export const OptionsPage = ({
  title,
  options,
  background,
}: {
  title: string;
  options: Array<{ name: string; description: string; price?: string }>;
  background?: string;
}) => {
  return (
    <div className="page bg-cream flex flex-col gap-[1cm] p-[2cm] !pb-0 !h-auto">
      <h1 className="text-xl font-bold">{title}</h1>

      <dl className={clsx("border-4 border-black p-[1cm]", background)}>
        {options.map((option) => (
          <div key={option.name}>
            <dt className="font-bold break-after-avoid pt-[0.3cm]">
              {humanizeText(option.name)}
              {option.price && (
                <span className="text-sm font-normal"> - {option.price}€</span>
              )}
            </dt>
            <dd>{compile(option.description).tree}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
};
