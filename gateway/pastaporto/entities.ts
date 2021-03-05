import { IDENTITY_SECRET, PASTAPORTO_SECRET } from "../config";
import jwt from "jsonwebtoken";
import { promisify } from "util";

const jwtVerify = promisify(jwt.verify);
const jwtSign = promisify(jwt.sign);

enum Credential {
  STAFF = "staff",
  AUTHENTICATED = "authenticated",
}

class UserInfo {
  constructor(readonly id: number, readonly email: string) {}

  data() {
    return {
      id: this.id,
      email: this.email,
    };
  }
}

type DecodedIdentity = {
  sub: number;
};

export class Pastaporto {
  constructor(
    readonly userInfo: UserInfo | null = null,
    readonly credentials: Credential[] = [],
  ) {}

  async sign(): Promise<string> {
    return (await jwtSign(
      {
        userInfo: this.userInfo?.data?.() ?? null,
        credentials: this.credentials,
      },
      PASTAPORTO_SECRET,
      // @ts-ignore
      { expiresIn: "1m" },
    )) as string;
  }

  static unauthenticated() {
    return new Pastaporto(null, []);
  }

  static async fromIdentityToken(token: string) {
    // @ts-ignore
    const decoded = (await jwtVerify(
      token,
      // @ts-ignore
      IDENTITY_SECRET,
    )) as DecodedIdentity;
    console.log("decoded token is:", decoded);

    // call internal API to get user info
    const userInfo = {
      id: decoded.sub,
      email: "test@email.it",
      isStaff: true,
    };

    return new Pastaporto(new UserInfo(userInfo.id, userInfo.email), [
      Credential.AUTHENTICATED,
    ]);
  }
}
