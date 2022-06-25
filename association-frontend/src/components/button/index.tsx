import classnames from "classnames";
import React, { useEffect, useState } from "react";

type ButtonProps = {
  disabled?: boolean;
  text?: string;
  link?: string;
  type?: "button" | "reset" | "submit";
  fullWidth?: boolean;
  loading?: boolean;
  onClick?: (...args: any[]) => void;
};

const loadingEmojis = ["🐍", "🕑", "🕓", "🕗", "🕙", "🧨"];

export const Button = ({
  type,
  link,
  text,
  fullWidth,
  children,
  loading = false,
  ...props
}: React.PropsWithChildren<ButtonProps>) => {
  const [emojiIndex, setEmojiIndex] = useState(0);

  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setEmojiIndex((emojiIndex + 1) % loadingEmojis.length);
      }, 600);
      return () => clearInterval(interval);
    }
  }, [loading]);

  return (
    <button
      type={type}
      onClick={props.onClick}
      disabled={loading}
      className={classnames(
        "px-6 py-4 border border-transparent text-base font-bold text-bluecyan uppercase tracking-widest bg-yellow  hover:bg-bluecyan hover:text-yellow shadow-solidblue hover:shadow-solidyellow",
        {
          "w-full": fullWidth,
        },
      )}
    >
      <div className="flex flex-row space-x-4">
        {loading && <span>{loadingEmojis[emojiIndex]}</span>}
        {link && (
          <a href={link} target="_blank" rel="noopener noreferrer">
            {text}
          </a>
        )}
        {!link && <span>{text}</span>}
      </div>
    </button>
  );
};
