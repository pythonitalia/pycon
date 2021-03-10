import { PASTAPORTO_SECRET } from "../config";
import jwt from "jsonwebtoken";
import { promisify } from "util";
import { fetchUserInfo, User } from "./user-info";
import { decodeIdentity } from "./identity";

const jwtSign = promisify(jwt.sign);

enum Credential {
  STAFF = "staff",
  AUTHENTICATED = "authenticated",
}

class UserInfo {
  constructor(
    readonly id: number,
    readonly email: string,
    readonly isStaff: boolean,
  ) {}

  data() {
    return {
      id: this.id,
      email: this.email,
      isStaff: this.isStaff,
    };
  }
}

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
    const decoded = await decodeIdentity(token);
    const userInfo = await fetchUserInfo(decoded.sub);

    return new Pastaporto(
      new UserInfo(userInfo.id, userInfo.email, userInfo.isStaff),
      getCredentialsFromUser(userInfo),
    );
  }
}

const getCredentialsFromUser = (user: User): Credential[] => {
  const credentials = [Credential.AUTHENTICATED];
  if (user.isStaff) {
    credentials.push(Credential.STAFF);
  }
  return credentials;
};
