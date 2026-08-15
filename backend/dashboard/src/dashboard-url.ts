export function dashboardUrl(
  conferenceCode: string,
  {
    comparisonCodes = [],
  }: {
    comparisonCodes?: string[];
  } = {},
) {
  const params = new URLSearchParams();

  for (const code of comparisonCodes) {
    params.append("compare", code);
  }
  const path = `/dashboard/${encodeURIComponent(conferenceCode)}`;
  const query = params.toString();

  return query ? `${path}?${query}` : path;
}
