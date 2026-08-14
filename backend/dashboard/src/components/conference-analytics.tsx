import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  ReferenceLine,
  XAxis,
  YAxis,
} from "recharts";

export type AnalyticsWeekData = {
  label: string;
  value: number;
};

export type AnalyticsBreakdownData = {
  count: number;
  id: string;
  label: string;
  share: number;
};

export type AnalyticsDetailData = {
  label: string;
  value: string;
};

export type AnalyticsProductData = {
  id: string;
  name: string;
  price: string;
  tier: string;
};

export type AnalyticsAnnotationData = {
  date: string;
  id: string;
  label: string;
  x: number | string;
};

export type AnalyticsChartData = {
  allocatedTotal: number | null;
  annotations: AnalyticsAnnotationData[];
  breakdown: AnalyticsBreakdownData[];
  comparisonAnnotations: AnalyticsAnnotationData[];
  comparisonBreakdown: AnalyticsBreakdownData[];
  comparisonLabel: string;
  comparisonValues: AnalyticsWeekData[];
  currentLabel: string;
  details: AnalyticsDetailData[];
  id: string;
  period: string;
  products: AnalyticsProductData[];
  summary: string;
  title: string;
  total: number | null;
  values: AnalyticsWeekData[];
};

export type AnalyticsConferenceData = {
  analytics: AnalyticsChartData[];
  code: string;
  name: string;
  year: number | null;
};

type AnalyticsChartSeries = {
  chart: AnalyticsChartData;
  conference: AnalyticsConferenceData;
};

function cumulativeValues(values: AnalyticsWeekData[]) {
  let total = 0;

  return values.map((week) => {
    total += week.value;
    return { ...week, value: total };
  });
}

function CumulativeLineChart({ series }: { series: AnalyticsChartSeries[] }) {
  const primary = series[0];
  const hasExplicitComparisons = series.length > 1;
  const implicitComparisonValues = cumulativeValues(
    primary.chart.comparisonValues,
  );
  const displayedSeries = hasExplicitComparisons
    ? series.map(({ chart, conference }, index) => ({
        annotationLabel: String(conference.year ?? conference.name),
        annotations: chart.annotations,
        color: `var(--chart-${(index % 5) + 1})`,
        dashed: false,
        key: `conference${index}`,
        label: conference.name,
        values: cumulativeValues(chart.values),
      }))
    : [
        {
          annotationLabel: "",
          annotations: primary.chart.annotations,
          color: "var(--chart-1)",
          dashed: false,
          key: "conference0",
          label: primary.chart.currentLabel,
          values: cumulativeValues(primary.chart.values),
        },
        ...(implicitComparisonValues.length
          ? [
              {
                annotationLabel: "",
                annotations: primary.chart.comparisonAnnotations,
                color: "var(--chart-2)",
                dashed: true,
                key: "conference1",
                label: primary.chart.comparisonLabel,
                values: implicitComparisonValues,
              },
            ]
          : []),
      ];
  const values = Array.from(
    {
      length: Math.max(
        ...displayedSeries.map((chartSeries) => chartSeries.values.length),
      ),
    },
    (_, index) => {
      const value: Record<string, number | string | undefined> = {
        label:
          displayedSeries[0].values[index]?.label ??
          displayedSeries.find((chartSeries) => chartSeries.values[index])
            ?.values[index]?.label ??
          "",
        position: index,
      };

      for (const chartSeries of displayedSeries) {
        value[chartSeries.key] = chartSeries.values[index]?.value;
      }

      return value;
    },
  );
  const annotationPosition = (x: number | string) => {
    if (typeof x === "number") {
      return x;
    }

    const position = values.findIndex((value) => value.label === x);
    return position >= 0 ? position : 0;
  };
  const annotationRows = displayedSeries.filter(
    (chartSeries) => chartSeries.annotations.length,
  ).length;
  const chartConfig = Object.fromEntries(
    displayedSeries.map((chartSeries) => [
      chartSeries.key,
      {
        color: chartSeries.color,
        label: chartSeries.label,
      },
    ]),
  ) satisfies ChartConfig;
  const unavailable = series.every(({ chart }) => chart.total === null);

  return (
    <figure
      className="min-w-0"
      aria-label={`${primary.chart.title} by checkpoint`}
    >
      {unavailable ? null : (
        <ul className="flex list-none flex-wrap items-center gap-x-5 gap-y-2 pb-3 text-base text-muted-foreground sm:text-sm">
          {displayedSeries.map((chartSeries) => (
            <li className="flex items-center gap-2" key={chartSeries.key}>
              <span
                aria-hidden="true"
                className="w-5 border-t-2"
                style={{
                  borderColor: chartSeries.color,
                  borderStyle: chartSeries.dashed ? "dashed" : "solid",
                }}
              />
              {chartSeries.label}
            </li>
          ))}
          {annotationRows ? (
            <li className="flex items-center gap-2">
              <span
                aria-hidden="true"
                className="h-4 border-l-2 border-muted-foreground"
              />
              Deadline markers
            </li>
          ) : null}
        </ul>
      )}
      <div className="overflow-x-auto">
        <div className="relative min-w-xl">
          <ChartContainer
            className="h-60 w-full aspect-auto"
            config={chartConfig}
          >
            <AreaChart
              accessibilityLayer
              data={values}
              margin={{
                left: 4,
                right: 4,
                top: annotationRows ? 36 + (annotationRows - 1) * 18 : 8,
              }}
            >
              <CartesianGrid vertical={false} />
              <XAxis
                allowDecimals={false}
                axisLine={false}
                dataKey="position"
                domain={[0, Math.max(values.length - 1, 0)]}
                minTickGap={24}
                tickFormatter={(position: number) =>
                  String(values[Math.round(position)]?.label ?? "")
                }
                tickLine={false}
                tickMargin={10}
                ticks={values.map((value) => Number(value.position))}
                type="number"
              />
              <YAxis domain={[0, "auto"]} hide />
              {unavailable ? null : (
                <>
                  <ChartTooltip
                    content={
                      <ChartTooltipContent
                        indicator="line"
                        labelFormatter={(_value, payload) =>
                          payload?.[0]?.payload?.label
                        }
                      />
                    }
                    cursor={false}
                    isAnimationActive={false}
                  />
                  {displayedSeries.flatMap((chartSeries, seriesIndex) =>
                    chartSeries.annotations.map((annotation, index) => (
                      <ReferenceLine
                        key={`${chartSeries.key}-${annotation.id}`}
                        label={{
                          dy: seriesIndex * 18,
                          fill: `var(--color-${chartSeries.key})`,
                          fontSize: 12,
                          position:
                            index === chartSeries.annotations.length - 1
                              ? "insideTopLeft"
                              : "insideTopRight",
                          value: hasExplicitComparisons
                            ? `${chartSeries.annotationLabel} · ${annotation.label} · ${annotation.date}`
                            : `${annotation.label} · ${annotation.date}`,
                        }}
                        stroke={`var(--color-${chartSeries.key})`}
                        strokeDasharray={chartSeries.dashed ? "5 5" : undefined}
                        strokeWidth={1.5}
                        x={annotationPosition(annotation.x)}
                      />
                    )),
                  )}
                  {hasExplicitComparisons ? (
                    displayedSeries.map((chartSeries, index) => (
                      <Line
                        activeDot={{ r: 5 }}
                        dataKey={chartSeries.key}
                        dot={
                          index === 0
                            ? {
                                fill: `var(--color-${chartSeries.key})`,
                                r: 3,
                              }
                            : false
                        }
                        isAnimationActive={false}
                        key={chartSeries.key}
                        stroke={`var(--color-${chartSeries.key})`}
                        strokeWidth={index === 0 ? 2.5 : 2}
                        type="monotone"
                      />
                    ))
                  ) : (
                    <>
                      {displayedSeries[1] ? (
                        <Line
                          dataKey={displayedSeries[1].key}
                          dot={false}
                          isAnimationActive={false}
                          stroke={`var(--color-${displayedSeries[1].key})`}
                          strokeWidth={2}
                          type="monotone"
                        />
                      ) : null}
                      <Area
                        activeDot={{ r: 5 }}
                        dataKey={displayedSeries[0].key}
                        dot={{
                          fill: `var(--color-${displayedSeries[0].key})`,
                          r: 3,
                        }}
                        fill={`var(--color-${displayedSeries[0].key})`}
                        fillOpacity={0.12}
                        isAnimationActive={false}
                        stroke={`var(--color-${displayedSeries[0].key})`}
                        strokeWidth={2}
                        type="monotone"
                      />
                    </>
                  )}
                </>
              )}
            </AreaChart>
          </ChartContainer>
          {unavailable ? (
            <p className="absolute inset-0 flex items-center justify-center text-base text-muted-foreground sm:text-sm">
              Connect Pretix to populate this chart
            </p>
          ) : null}
        </div>
      </div>
      <figcaption className="sr-only">
        {unavailable
          ? `${primary.chart.title} data is unavailable.`
          : `${primary.chart.title} cumulative totals for the selected conferences.`}
      </figcaption>
    </figure>
  );
}

function trendLabel(current: number | null, comparison: number | null) {
  if (current === null || comparison === null || comparison === 0) {
    return null;
  }

  const change = ((current - comparison) / comparison) * 100;
  const formatted = new Intl.NumberFormat("en", {
    maximumFractionDigits: 1,
    signDisplay: "always",
  }).format(change);

  return `${formatted}%`;
}

function MetricHeading({ series }: { series: AnalyticsChartSeries[] }) {
  const chart = series[0].chart;

  return (
    <div className="space-y-5">
      <div className="flex min-w-0 items-center justify-between gap-4">
        <h3 className="truncate text-base font-medium">{chart.title}</h3>
        <p className="shrink-0 text-base text-muted-foreground sm:text-sm">
          {chart.period}
        </p>
      </div>
      <div className="flex min-w-0 items-baseline gap-3">
        <p className="shrink-0 text-4xl font-semibold tracking-tight tabular-nums">
          {chart.total?.toLocaleString() ?? "—"}
        </p>
        <p className="truncate text-base text-muted-foreground sm:text-sm">
          {chart.summary}
        </p>
      </div>
      {series.length > 1 ? (
        <ul className="flex list-none flex-wrap gap-x-4 gap-y-2 text-base text-muted-foreground sm:text-sm">
          {series
            .slice(1)
            .map(({ chart: comparisonChart, conference }, index) => {
              const trend = trendLabel(chart.total, comparisonChart.total);

              return (
                <li
                  className="inline-flex items-center gap-1.5"
                  key={conference.code}
                >
                  <span
                    aria-hidden="true"
                    className="size-2 rounded-full"
                    style={{
                      backgroundColor: `var(--chart-${(index % 4) + 2})`,
                    }}
                  />
                  {trend ? (
                    <span className="font-medium text-foreground">{trend}</span>
                  ) : null}
                  <span>vs {conference.year ?? conference.name}</span>
                </li>
              );
            })}
        </ul>
      ) : null}
    </div>
  );
}

function BreakdownTable({
  chart,
  countLabel,
}: {
  chart: AnalyticsChartData;
  countLabel: string;
}) {
  return (
    <div className="overflow-x-auto border-y">
      <table className="w-full min-w-md text-left text-base sm:text-sm">
        <thead className="text-muted-foreground">
          <tr>
            <th className="py-3 pr-4 font-medium" scope="col">
              Status
            </th>
            <th className="px-4 py-3 text-right font-medium" scope="col">
              {countLabel}
            </th>
            <th className="py-3 pl-4 text-right font-medium" scope="col">
              Share
            </th>
          </tr>
        </thead>
        <tbody>
          {chart.breakdown.length ? (
            chart.breakdown.map((row) => (
              <tr className="border-t" key={row.id}>
                <th className="py-3 pr-4 font-normal" scope="row">
                  {row.label}
                </th>
                <td className="px-4 py-3 text-right tabular-nums">
                  {row.count.toLocaleString()}
                </td>
                <td className="py-3 pl-4 text-right text-muted-foreground tabular-nums">
                  {row.share}%
                </td>
              </tr>
            ))
          ) : (
            <tr className="border-t">
              <td className="py-4 text-muted-foreground" colSpan={3}>
                No data yet
              </td>
            </tr>
          )}
        </tbody>
        <tfoot>
          <tr className="border-t font-medium">
            <th className="py-3 pr-4" scope="row">
              Total received
            </th>
            <td className="px-4 py-3 text-right tabular-nums">
              {chart.total?.toLocaleString() ?? 0}
            </td>
            <td className="py-3 pl-4 text-right text-muted-foreground tabular-nums">
              {chart.total ? "100%" : "0%"}
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
}

function TicketSalesPanel({ series }: { series: AnalyticsChartSeries[] }) {
  const chart = series[0].chart;
  const hasExplicitComparisons = series.length > 1;
  const mixSeries = hasExplicitComparisons
    ? series.map(({ chart: seriesChart, conference }, index) => ({
        breakdown: seriesChart.breakdown,
        color: `var(--chart-${(index % 5) + 1})`,
        id: conference.code,
        label: String(conference.year ?? conference.name),
      }))
    : [
        {
          breakdown: chart.breakdown,
          color: "var(--chart-1)",
          id: "current",
          label: chart.currentLabel.match(/\d{4}/)?.[0] ?? "Current",
        },
        ...(chart.comparisonBreakdown.length
          ? [
              {
                breakdown: chart.comparisonBreakdown,
                color: "var(--chart-2)",
                id: "previous",
                label: chart.comparisonLabel.match(/\d{4}/)?.[0] ?? "Previous",
              },
            ]
          : []),
      ];
  const breakdownRows = Array.from(
    new Set(mixSeries.flatMap((item) => item.breakdown.map((row) => row.id))),
  ).map((id) => ({
    id,
    label:
      mixSeries.flatMap((item) => item.breakdown).find((row) => row.id === id)
        ?.label ?? id,
  }));

  return (
    <article className="grid @4xl:grid-cols-[16rem_minmax(0,1fr)]">
      <div className="flex flex-col gap-8 p-5 @4xl:border-r sm:p-6">
        <MetricHeading series={series} />
        <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-base sm:text-sm">
          {chart.details.map((detail) => (
            <div className="contents" key={detail.label}>
              <dt className="text-muted-foreground">{detail.label}</dt>
              <dd className="text-right font-medium tabular-nums">
                {detail.value}
              </dd>
            </div>
          ))}
        </dl>
      </div>
      <div className="min-w-0 border-t p-5 @4xl:border-t-0 sm:p-6">
        <CumulativeLineChart series={series} />
        {breakdownRows.length ? (
          <section className="mt-6 border-t pt-4">
            <div className="flex items-center justify-between gap-4 text-base sm:text-sm">
              <h3 className="font-medium">Ticket mix</h3>
              <p className="text-muted-foreground">
                {hasExplicitComparisons
                  ? `${mixSeries.length} conferences`
                  : "Current totals"}
              </p>
            </div>
            <dl className="mt-4 grid gap-4 @md:grid-cols-2 @3xl:grid-cols-4">
              {breakdownRows.map((row) => (
                <div className="min-w-0" key={row.id}>
                  <dt className="truncate font-medium">{row.label}</dt>
                  <dd className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 text-muted-foreground tabular-nums">
                    {mixSeries.map((item) => {
                      const value = item.breakdown.find(
                        (breakdown) => breakdown.id === row.id,
                      );

                      return (
                        <span
                          className="inline-flex items-center gap-1.5"
                          key={item.id}
                        >
                          <span
                            aria-hidden="true"
                            className="size-2 rounded-full"
                            style={{ backgroundColor: item.color }}
                          />
                          <span
                            className={
                              value ? "font-medium text-foreground" : undefined
                            }
                          >
                            {value?.count.toLocaleString() ?? "—"}
                          </span>
                          <span>
                            {value ? `${value.share}% · ` : ""}
                            {item.label}
                          </span>
                        </span>
                      );
                    })}
                  </dd>
                </div>
              ))}
            </dl>
          </section>
        ) : null}
        {chart.products.length ? (
          <section className="mt-6 border-t pt-4">
            <div className="flex items-center justify-between gap-4 text-base sm:text-sm">
              <h3 className="font-medium">Advertised tickets</h3>
              <p className="text-muted-foreground">Public site</p>
            </div>
            <dl className="mt-4 grid gap-4 @md:grid-cols-3">
              {chart.products.map((product) => (
                <div className="min-w-0" key={product.id}>
                  <dt className="truncate font-medium">{product.name}</dt>
                  <dd className="mt-1 flex items-baseline gap-2 text-muted-foreground">
                    <span className="font-medium text-foreground tabular-nums">
                      {product.price}
                    </span>
                    {product.tier ? <span>{product.tier}</span> : null}
                  </dd>
                </div>
              ))}
            </dl>
          </section>
        ) : null}
      </div>
    </article>
  );
}

function ProposalsPanel({ series }: { series: AnalyticsChartSeries[] }) {
  const chart = series[0].chart;

  return (
    <article className="flex min-w-0 flex-col gap-7 p-5 sm:p-6">
      <MetricHeading series={series} />
      <CumulativeLineChart series={series} />
      <BreakdownTable chart={chart} countLabel="Proposals" />
    </article>
  );
}

function StatusDistribution({ chart }: { chart: AnalyticsChartData }) {
  const chartData: Record<string, number | string> = { group: "Requests" };
  const chartConfig: ChartConfig = {};

  chart.breakdown.forEach((row, index) => {
    const key = `status${index}`;
    chartData[key] = row.count;
    chartConfig[key] = {
      color: `var(--chart-${(index % 5) + 1})`,
      label: row.label,
    };
  });

  return (
    <figure aria-label="Grant requests grouped by status">
      <ChartContainer
        className="h-5 w-full aspect-auto bg-muted"
        config={chartConfig}
        initialDimension={{ height: 20, width: 480 }}
      >
        <BarChart
          accessibilityLayer
          data={[chartData]}
          layout="vertical"
          margin={{ bottom: 0, left: 0, right: 0, top: 0 }}
          stackOffset="expand"
        >
          <XAxis hide type="number" />
          <YAxis dataKey="group" hide type="category" />
          <ChartTooltip
            content={<ChartTooltipContent hideLabel indicator="line" />}
            cursor={false}
            isAnimationActive={false}
          />
          {chart.breakdown.map((row, index) => (
            <Bar
              dataKey={`status${index}`}
              fill={`var(--color-status${index})`}
              isAnimationActive={false}
              key={row.id}
              stackId="status"
            />
          ))}
        </BarChart>
      </ChartContainer>
      <figcaption className="sr-only">
        Grant requests grouped by status.
      </figcaption>
    </figure>
  );
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat("en-IE", {
    currency: "EUR",
    maximumFractionDigits: 0,
    style: "currency",
  }).format(value);
}

function GrantsPanel({ series }: { series: AnalyticsChartSeries[] }) {
  const chart = series[0].chart;

  return (
    <article className="flex min-w-0 flex-col gap-7 p-5 sm:p-6">
      <MetricHeading series={series} />
      <CumulativeLineChart series={series} />
      <StatusDistribution chart={chart} />
      <BreakdownTable chart={chart} countLabel="Requests" />
      <div>
        <p className="text-base font-medium">Allocated</p>
        <p className="mt-2 text-3xl font-semibold tracking-tight tabular-nums">
          {formatCurrency(chart.allocatedTotal ?? 0)}
        </p>
        <p className="mt-1 max-w-sm text-base text-muted-foreground sm:text-sm">
          Approved, awaiting confirmation, and confirmed grants
        </p>
      </div>
    </article>
  );
}

export function ConferenceAnalytics({
  comparisonConferences,
  conference,
}: {
  comparisonConferences: AnalyticsConferenceData[];
  conference: AnalyticsConferenceData;
}) {
  const conferences = [conference, ...comparisonConferences];
  const chartSeries = (chartId: string) =>
    conferences.flatMap((seriesConference) => {
      const chart = seriesConference.analytics.find(
        (candidate) => candidate.id === chartId,
      );

      return chart ? [{ chart, conference: seriesConference }] : [];
    });
  const ticketSales = chartSeries("ticket-sales");
  const proposals = chartSeries("proposals-received");
  const grants = chartSeries("grants-received");

  if (!ticketSales.length || !proposals.length || !grants.length) {
    return null;
  }

  return (
    <section
      aria-labelledby="conference-analytics-title"
      className="@container overflow-hidden border-t bg-card"
      id="conference-analytics"
    >
      <h2 className="sr-only" id="conference-analytics-title">
        Conference analytics
      </h2>
      <TicketSalesPanel series={ticketSales} />
      <div className="grid border-t @5xl:grid-cols-2">
        <div className="min-w-0 @5xl:border-r">
          <ProposalsPanel series={proposals} />
        </div>
        <div className="min-w-0 border-t @5xl:border-t-0">
          <GrantsPanel series={grants} />
        </div>
      </div>
    </section>
  );
}
