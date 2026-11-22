const readList = (name: string) =>
  (new URLSearchParams(window.location.search).get(name) ?? "")
    .split(",")
    .filter(Boolean);

export const readUrlState = () => ({
  proposalId: readList("proposal")[0] ?? null,
  excludeTags: readList("exclude"),
});

export const writeUrlState = ({
  proposalId,
  excludeTags,
}: {
  proposalId: string | null;
  excludeTags: string[];
}) => {
  const params = new URLSearchParams();
  if (proposalId) {
    params.set("proposal", proposalId);
  }
  if (excludeTags.length > 0) {
    params.set("exclude", excludeTags.join(","));
  }
  const query = params.toString();
  window.history.replaceState(
    null,
    "",
    `${window.location.pathname}${query ? `?${query}` : ""}`,
  );
};
