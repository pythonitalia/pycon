import { createIdentityToken } from "../pastaporto/identity";
import { IS_DEV } from "../config";
import { PastaportoAction } from "./entities";

export class AuthAction extends PastaportoAction {
  async apply(context: any) {
    const identityToken = await createIdentityToken(
      parseInt(this.payload["id"], 10),
    );

    context.setCookies.push({
      name: "identity",
      value: identityToken,
      options: {
        httpOnly: true,
        maxAge: 60 * 15,
        path: "/",
        sameSite: true,
        secure: !IS_DEV,
      },
    });
  }
}
