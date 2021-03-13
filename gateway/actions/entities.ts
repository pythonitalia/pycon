import jwt from "jsonwebtoken";
import { createIdentityToken } from "../pastaporto/identity";
import { IS_DEV, PASTAPORTO_ACTION_SECRET } from "../config";

enum Action {
  AUTH = "auth",
}

type DecodedToken = {
  action: Lowercase<keyof typeof Action>;
  payload: { [key: string]: string };
};

export abstract class PastaportoAction {
  constructor(readonly payload: { [key: string]: string }) {}

  abstract apply(context: any): Promise<void>;

  static fromToken(token: string) {
    const decodedToken = jwt.verify(
      token,
      PASTAPORTO_ACTION_SECRET as string,
    ) as DecodedToken;

    const actionName = decodedToken.action.toUpperCase() as keyof typeof Action;
    const action = Action[actionName];

    switch (action) {
      case Action.AUTH:
        return new AuthAction(decodedToken.payload);
      default:
        throw new Error(
          `Unsupported pastaporto action: ${decodedToken.action}`,
        );
    }
  }
}

class AuthAction extends PastaportoAction {
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
