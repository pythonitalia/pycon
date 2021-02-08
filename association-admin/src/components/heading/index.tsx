type Props = {
  align?: "center" | "left";
};

export const Heading: React.FC<Props> = ({ align = "left", children }) => (
  <h1 className={`text-${align} text-2xl font-extrabold text-gray-900`}>
    {children}
  </h1>
);
