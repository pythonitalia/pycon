type Props = {
  label: string;
  // Optional value; until stats are wired (T5) this stays undefined and the
  // card shows a placeholder dash.
  value?: number | string;
};

export const StatCard = ({ label, value }: Props) => {
  return (
    <div className="rounded-lg border border-gray-200 bg-white px-4 py-3 shadow-sm">
      <div className="text-2xl font-semibold text-[#417690]">
        {value ?? "—"}
      </div>
      <div className="text-xs uppercase tracking-wide text-gray-500 mt-1">
        {label}
      </div>
    </div>
  );
};
