import jwt from "jsonwebtoken";

import { PASTAPORTO_SECRET } from "../config";
import { decodeIdentity } from "./identity";
import { fetchUserInfo, User } from "./user-info";

export enum Credential {
  STAFF = "staff",
  AUTHENTICATED = "authenticated",
}

export class UserInfo {
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

  sign(): string {
    return jwt.sign(
      {
        userInfo: this.userInfo?.data?.() ?? null,
        credentials: this.credentials,
      },
      PASTAPORTO_SECRET!,
      { expiresIn: "1m", issuer: "gateway", algorithm: "HS256" },
    );
  }

  static unauthenticated() {
    return new Pastaporto(null, []);
  }

  static async fromIdentityToken(token: string) {
    const decoded = decodeIdentity(token);
    const userInfo = await fetchUserInfo(decoded.sub);

    if (!userInfo) {
      console.info(`User ID ${decoded.sub} not found`);
      throw new Error("No user found");
    }

    if (!userInfo.isActive) {
      console.info(`User ID: ${userInfo.id} is not active`);
      throw new Error("No user found");
    }

    console.info("created pastaporto from token");
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
