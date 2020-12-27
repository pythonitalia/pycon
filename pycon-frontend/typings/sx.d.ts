import { SxProps } from "theme-ui";

declare module "react" {
  // eslint-disable-next-line @typescript-eslint/no-empty-interface
  interface HTMLAttributes<T> extends SxProps {}

  // eslint-disable-next-line @typescript-eslint/no-empty-interface
  interface SVGAttributes<T> extends SxProps {}
}
