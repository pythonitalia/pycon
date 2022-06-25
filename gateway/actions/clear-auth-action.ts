import { IS_DEV } from "../config";
import { PastaportoAction } from "./entities";

type Options = void;

export class ClearAuthAction extends PastaportoAction<Options, void, void> {
  async apply(context: any) {
    context.setCookies.splice(0, context.setCookies.length);

    context.res.cookie("identity", "invalid", {
      maxAge: -1,
      httpOnly: true,
      path: "/",
      sameSite: "none",
      secure: !IS_DEV,
    });

    context.res.cookie("refreshIdentity", "invalid", {
      maxAge: -1,
      httpOnly: true,
      path: "/",
      sameSite: "none",
      secure: !IS_DEV,
    });
  }
}
