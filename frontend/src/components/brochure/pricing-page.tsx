import clsx from "clsx";
import { useMoneyFormatter } from "~/helpers/formatters";
import { humanizeText } from "./utils";

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
    4: "bg-cream",
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
    <>
      <div className="uppercase font-bold text-coral px-[0.5cm] pt-[0.5cm] bg-cream">
        {humanizeText(title)}
      </div>
      {new Array(totalPackages).fill(null).map((_, i) => (
        <div className={clsx("border-l", getBackgroundColor(i))} />
      ))}
    </>
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
    <>
      <div className="px-[0.5cm] font-medium pb-[0.5cm] bg-cream">{title}</div>
      {values.map((value, i) => {
        return (
          <div
            className={clsx(
              "border-l text-center pb-[0.5cm] relative",
              getBackgroundColor(i),
            )}
          >
            {typeof value === "boolean" ? (value ? "✓" : "-") : value}
          </div>
        );
      })}
    </>
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
  const filteredLevels = levels.filter(
    (level) => Number.parseFloat(level.price) > 0,
  );
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
  const moneyFormatter = useMoneyFormatter({ fractionDigits: 0 });

  const sectionHeaderSize = 37;
  const itemSize = 55;
  let currentPageSize = 0;
  let currentContent = {};
  const pagesToRender: Record<string, { name: string; category: string }[]>[] =
    [];

  Object.entries(benefitsByCategory).map(([category, benefits], index) => {
    currentPageSize += sectionHeaderSize;
    const maxPageSize = index === 0 ? 550 : 756;
    benefits.forEach((benefit) => {
      console.log({ currentPageSize, benefit });
      if (currentPageSize + itemSize > maxPageSize) {
        currentPageSize = sectionHeaderSize;
        pagesToRender.push(currentContent);
        currentContent = {};
      }

      if (!currentContent[category]) {
        currentContent[category] = [];
      }

      currentContent[category].push(benefit);
      currentPageSize += itemSize;
    });
  });

  pagesToRender.push(currentContent);

  return (
    <div>
      {pagesToRender.map((page, i) => (
        <div
          key={i}
          className="page pricing-page-table flex flex-col gap-[1cm] bg-cream pt-[2cm]"
        >
          <div className="px-[2cm]">
            <h1 className="text-xl font-bold">Pricing</h1>
          </div>

          <div
            className="border-[4px] grid gap-0 border-black w-full text-[12px]"
            style={{
              gridTemplateColumns: `auto repeat(${filteredLevels.length}, 2.1cm)`,
            }}
          >
            <div className="border-b-[4px] bg-cream" />
            {filteredLevels.map((p, i) => (
              <th
                className={clsx(
                  "py-[0.5cm] w-[2.1cm] text-center border-l uppercase border-b-[4px]",
                  getBackgroundColor(i),
                )}
                key={p.name}
              >
                {p.name}
              </th>
            ))}
            {i === 0 && (
              <>
                <TableSection
                  title="Pricing"
                  totalPackages={filteredLevels.length}
                />
                <TableBenefit
                  title="Package price (VAT not included)"
                  values={filteredLevels.map(
                    (p) =>
                      `${moneyFormatter.format(Number.parseFloat(p.price))}`,
                  )}
                />

                <TableSection
                  title="Availability"
                  totalPackages={filteredLevels.length}
                />
                <TableBenefit
                  title="Number of slots available"
                  values={filteredLevels.map(
                    (p) => `${p.slots === 0 ? "Unlimited" : p.slots}`,
                  )}
                />
              </>
            )}

            {Object.entries(page).map(([category, benefits]) => {
              return (
                <>
                  <TableSection
                    title={category}
                    totalPackages={filteredLevels.length}
                    key={category}
                  />
                  {benefits.map((benefit) => (
                    <TableBenefit
                      title={benefit.name}
                      values={filteredLevels.map((p) => {
                        const levelBenefit = getBenefitForLevel(benefit, p);
                        return levelBenefit ? levelBenefit.value : "-";
                      })}
                      key={benefit.name}
                    />
                  ))}
                </>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
