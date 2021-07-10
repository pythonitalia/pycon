import { default as NextLink } from "next/link";

type LinkProps = {
  text: string;
  to: string;
  className?: string;
};

export const Link: React.FC<LinkProps> = ({ text, to }) => {
  return (
    <div className="flex items-center justify-between ">
      <div className="mt-1 text-base">
        <NextLink href={to}>
          <a className="font-medium text-indigo-600 hover:text-indigo-500">
            {text}
          </a>
        </NextLink>
      </div>
    </div>
  );
};
