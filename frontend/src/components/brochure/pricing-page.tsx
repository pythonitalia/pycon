import clsx from "clsx";

export type Benefit = {
  name: string;
  id: string;
  group: string;
};

export type Package = {
  name: string;
  price: number;
  availability: number | "unlimited";
  benefits: { id: string; value: number | string | boolean }[];
};

const getBackgroundColor = (index: number) => {
  return {
    0: "bg-purple",
    1: "bg-yellow",
    2: "bg-grey-100",
    3: "bg-pink",
    4: "bg-orange",
    5: "bg-blue",
    6: "bg-coral",
  }[index % 7];
};

const TableSection = ({
  title,
  totalPackages,
}: {
  title: string;
  totalPackages: number;
}) => {
  return (
    <tr>
      <td className="uppercase font-bold text-coral px-[0.5cm] pt-[0.5cm] bg-cream">
        {title}
      </td>
      {new Array(totalPackages).fill(null).map((_, i) => (
        <td className={clsx("border-l", getBackgroundColor(i))} />
      ))}
    </tr>
  );
};

function TableBenefit({
  title,
  values,
}: {
  title: string;
  values: Array<number | string | boolean>;
}) {
  return (
    <tr>
      <td className="px-[0.5cm] font-medium pb-[0.5cm] bg-cream">{title}</td>
      {values.map((value, i) => {
        return (
          <td
            className={clsx(
              "border-l text-center pb-[0.5cm] relative",
              getBackgroundColor(i),
            )}
          >
            {typeof value === "boolean" ? (value ? "✓" : "-") : value}
            {/* adding some divs here to prevent gaps when printing */}
            <span
              className={clsx(
                "absolute top-[-2px] left-0 right-0 h-[4px]",
                getBackgroundColor(i),
              )}
            />
            <span
              className={clsx(
                "absolute bottom-[-2px] left-0 right-0 h-[4px]",
                getBackgroundColor(i),
              )}
            />
          </td>
        );
      })}
    </tr>
  );
}

export function PricingPage({
  levels,
  benefits,
}: {
  levels: {
    name: string;
    price: string;
    slots?: number;
    benefits: { name: string; value: number | string | boolean }[];
  }[];
  benefits: { name: string; category: string }[];
}) {
  console.log(benefits);
  const benefitsByCategory = benefits.reduce(
    (acc, benefit) => {
      if (!acc[benefit.category]) {
        acc[benefit.category] = [];
      }

      acc[benefit.category].push(benefit);

      return acc;
    },
    {} as Record<string, { name: string; category: string }[]>,
  );

  const getBenefitForLevel = (
    benefit: { name: string },
    level: { benefits: { name: string; value: number | string | boolean }[] },
  ) => {
    return level.benefits.find((b) => b.name === benefit.name);
  };

  return (
    <div className="page bg-cream flex flex-col gap-[1cm] pt-[2cm] !h-auto">
      <div className="px-[2cm]">
        <h1 className="text-xl font-bold">Pricing</h1>
      </div>

      <table className="border-[4px]  border-black border-collapse table-fixed w-full text-[12px] border-spacing-0">
        <thead>
          <tr className="uppercase [&>th]:font-medium border-b">
            <th />

            {levels.map((p, i) => (
              <th
                className={clsx(
                  "py-[0.5cm] w-[2.1cm] text-center border-l",
                  getBackgroundColor(i),
                )}
                key={p.name}
              >
                {p.name}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          <TableSection title="Pricing" totalPackages={levels.length} />
          <TableBenefit
            title="Package price (VAT not included)"
            values={levels.map((p) => `${p.price.toLocaleString()}€`)}
          />

          <TableSection title="Availability" totalPackages={levels.length} />
          <TableBenefit
            title="Number of slots available"
            values={levels.map((p) => `${p.slots}`)}
          />

          {Object.entries(benefitsByCategory).map(([category, benefits]) => {
            return (
              <>
                <TableSection
                  title={category}
                  totalPackages={levels.length}
                  key={category}
                />
                {benefits.map((benefit) => (
                  <TableBenefit
                    title={benefit.name}
                    values={levels.map((p) => {
                      const levelBenefit = getBenefitForLevel(benefit, p);
                      return levelBenefit ? levelBenefit.value : "-";
                    })}
                    key={benefit.name}
                  />
                ))}
              </>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
