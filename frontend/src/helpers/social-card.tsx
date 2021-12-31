export type CardType = "social" | "social-square" | "social-twitter";

export const getSize = (cardType: CardType) => {
  switch (cardType) {
    case "social":
      return { width: 1200, height: 630 };
    case "social-twitter":
      return { width: 1200, height: 600 };
    case "social-square":
      return { width: 1200, height: 1200 };
  }
};

export const getTitleFontSize = (cardType: CardType) => {
  switch (cardType) {
    case "social":
    case "social-twitter":
      return 7;
    case "social-square":
      return 8;
  }
};
