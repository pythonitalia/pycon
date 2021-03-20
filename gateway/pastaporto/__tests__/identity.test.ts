import { JsonWebTokenError, TokenExpiredError } from "jsonwebtoken";
import {
  createIdentityToken,
  createRefreshToken,
  decodeIdentity,
  decodeRefreshToken,
  removeIdentityTokens,
} from "../identity";

jest.mock("../../config", () => ({
  IDENTITY_SECRET: "abc",
  IS_DEV: true,
}));

describe("Decode Identity", () => {
  //payload: {
  //   "iat": 1616248751,
  //   "exp": 1616249651,
  //   "aud": "identity",
  //   "iss": "gateway",
  //   "sub": "10"
  // }
  // Issued at 20 March 2021 13:59:11 GMT+00:00
  // Expires at 20 March 2021 14:14:11 GMT+00:00
  const validToken =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNDg3NTEsImV4cCI6MTYxNjI0OTY1MSwiYXVkIjoiaWRlbnRpdHkiLCJpc3MiOiJnYXRld2F5Iiwic3ViIjoiMTAifQ.a04dtYu5wsLaYKtchwrJAZsvzq9sI6kPN4d0pgNa8gk";

  test("Decode valid not expired identity", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:00:00Z").getTime());

    expect(decodeIdentity(validToken, false)).toContainEntry(["sub", "10"]);
  });

  test("Allow expired tokens if specified", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:30:00Z").getTime());

    expect(decodeIdentity(validToken, true)).toContainEntry(["sub", "10"]);
  });

  test("Ignore expired tokens by default", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:30:00Z").getTime());

    expect(() => decodeIdentity(validToken, false)).toThrow(TokenExpiredError);
  });

  test.each([true, false])(
    "Reject tokens not issued by gateway and expiration %p",
    (ignoreExpiration) => {
      // Expires at 20 March 2021 14:29:11 GMT+00:00
      const tokenWithWrongIssuer =
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNDk2NjEsImV4cCI6MTYxNjI1MDU2MSwiYXVkIjoiaWRlbnRpdHkiLCJpc3MiOiJ1c2VycyIsInN1YiI6IjEwIn0.D9rRwtrOHnnQhCB0ziyp-ujz3b2bX1_k6sG2kVSsgvE";

      jest
        .useFakeTimers("modern")
        .setSystemTime(new Date("2021-03-20 14:25:00Z").getTime());

      expect(() =>
        decodeIdentity(tokenWithWrongIssuer, ignoreExpiration),
      ).toThrowWithMessage(
        JsonWebTokenError,
        "jwt issuer invalid. expected: gateway",
      );
    },
  );

  test.each([true, false])(
    "Reject tokens with different audience and expiration %p",
    (ignoreExpiration) => {
      // Expires at 20 March 2021 14:45:57 GMT+00:00
      const tokenWithOtherAudience =
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNTA2NTcsImV4cCI6MTYxNjI1MTU1NywiYXVkIjoib3RoZXIiLCJpc3MiOiJnYXRld2F5Iiwic3ViIjoiMTAifQ.U7opmdprkIO3nBzkoJsbRFy9cZ4-PGoUQGGUBYwzRlk";

      jest
        .useFakeTimers("modern")
        .setSystemTime(new Date("2021-03-20 14:35:00Z").getTime());

      expect(() =>
        decodeIdentity(tokenWithOtherAudience, ignoreExpiration),
      ).toThrowWithMessage(
        JsonWebTokenError,
        "jwt audience invalid. expected: identity",
      );
    },
  );

  test.each([true, false])(
    "Ignore tokens with None algo and with expiration %p",
    (ignoreExpiration) => {
      // Expires at 20 March 2021 14:50:31 GMT+00:00
      const tokenSignedWithNoneAlgo =
        "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpYXQiOjE2MTYyNTA5MzEsImV4cCI6MTYxNjI1MTgzMSwiYXVkIjoib3RoZXIiLCJpc3MiOiJnYXRld2F5Iiwic3ViIjoiMTAifQ.";

      jest
        .useFakeTimers("modern")
        .setSystemTime(new Date("2021-03-20 14:40:00Z").getTime());

      expect(() =>
        decodeIdentity(tokenSignedWithNoneAlgo, ignoreExpiration),
      ).toThrowWithMessage(JsonWebTokenError, "jwt signature is required");
    },
  );

  test.each([true, false])(
    "Ignore tokens not using HS256 algo and with expiration %p",
    async (ignoreExpiration) => {
      // Expires at 20 March 2021 14:53:46 GMT+00:00
      const tokenSignedWithRS256 =
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnYXRld2F5Iiwic3ViIjoiMTAiLCJhdWQiOiJpZGVudGl0eSIsImlhdCI6MTYxNjI1MTQyNiwiZXhwIjoxNjE2MjUyMDI2fQ.DY8F5G9dtwstI4nBwKz-km12PHas_vJeAoGK6PFtw-i0U7XwBYPPCx1R8LawfFLSCpIwtdrqiFJQy02m3V85YBUmhvdGBaYTNnZYSehLSPcePkgrT0fB528hRmzYSDekrJkq5Sp3MJ694ZJ3LY1uDQbhG_-zv5DfOcDDFrTX8vYC36BFnilLhla-qpDHxi5NGS5JAqgLmK7YKxL8W_SlZqBSnhkccTzF9WNQnhX8CjdXJnAXZE6um8_ubvQiwwFI0l77M2_ZHRPHtugqwFv4mLRyWG40eYDxOcv2Th67F3IA3mA6juvHwbNUem3t8Oc65jkYWSECn0hFikQIgTSgRA";

      jest
        .useFakeTimers("modern")
        .setSystemTime(new Date("2021-03-20 14:45:00Z").getTime());

      await expect(() =>
        decodeIdentity(tokenSignedWithRS256, ignoreExpiration),
      ).toThrowWithMessage(JsonWebTokenError, "invalid algorithm");
    },
  );

  test.each([true, false])(
    "Reject tokens with wrong secret and check expiration %p",
    async (ignoreExpiration) => {
      // Expires at 20 March 2021 14:53:46 GMT+00:00
      // signed with abc123
      const testToken =
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNTA5MzEsImV4cCI6MTYxNjI1MTgzMSwiYXVkIjoiaWRlbnRpdHkiLCJpc3MiOiJnYXRld2F5Iiwic3ViIjoiMTAifQ.e_bwjvNXJfVVJ9pztXzkNA0jsKWvpQcYrjTJM6t2_hM";

      jest
        .useFakeTimers("modern")
        .setSystemTime(new Date("2021-03-20 14:40:31Z").getTime());

      await expect(() =>
        decodeIdentity(testToken, ignoreExpiration),
      ).toThrowWithMessage(JsonWebTokenError, "invalid signature");
    },
  );
});

describe("Create identity", () => {
  test("Create identity", () => {
    // signed with "abc", at 2021-03-20 14:35:31Z
    const expectedIdentityToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNTA5MzEsImV4cCI6MTYxNjI1MTgzMSwiYXVkIjoiaWRlbnRpdHkiLCJpc3MiOiJnYXRld2F5Iiwic3ViIjoiMTAifQ.WfDXRSy_mlfS4wFkJzohGJY6mi2l38gza536Q4u50LQ";

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    expect(createIdentityToken("10")).toBe(expectedIdentityToken);
  });

  test("Empty subject fails", () => {
    expect(() => createIdentityToken("")).toThrow("Empty subject not allowed");
  });
});

describe("Decode refresh token", () => {
  test("Accept valid refresh token for subject", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:40:31Z").getTime());

    const testToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNTA5MzEsImV4cCI6MTYyMzY4MTMzMSwiYXVkIjoicmVmcmVzaCIsImlzcyI6ImdhdGV3YXkiLCJzdWIiOiIxMCJ9.14tohtJ9NfLFQ0wq6tKVHEC4Opphh37Z5xABsy7XVP8";

    expect(decodeRefreshToken(testToken, "10")).toContainEntry(["sub", "10"]);
  });

  test("Reject refresh token for another subject", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:40:31Z").getTime());

    const testToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNTA5MzEsImV4cCI6MTYyMzY4MTMzMSwiYXVkIjoicmVmcmVzaCIsImlzcyI6ImdhdGV3YXkiLCJzdWIiOiIxMCJ9.14tohtJ9NfLFQ0wq6tKVHEC4Opphh37Z5xABsy7XVP8";

    expect(() => decodeRefreshToken(testToken, "20")).toThrowWithMessage(
      JsonWebTokenError,
      "jwt subject invalid. expected: 20",
    );
  });

  test("Reject expired refresh token", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2050-03-20 14:40:31Z").getTime());

    const testToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNTA5MzEsImV4cCI6MTYyMzY4MTMzMSwiYXVkIjoicmVmcmVzaCIsImlzcyI6ImdhdGV3YXkiLCJzdWIiOiIxMCJ9.14tohtJ9NfLFQ0wq6tKVHEC4Opphh37Z5xABsy7XVP8";

    expect(() => decodeRefreshToken(testToken, "10")).toThrow(
      TokenExpiredError,
    );
  });

  test("Reject refresh token with wrong audience", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:40:31Z").getTime());

    const testToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNTA5MzEsImV4cCI6MTYyMzY4MTMzMSwiYXVkIjoiaWRlbnRpdHkiLCJpc3MiOiJnYXRld2F5Iiwic3ViIjoiMTAifQ.UQfAUpUc2h-Sbjl59or2cCSUQJ9fG0Vsky4HwbOtAhA";

    expect(() => decodeRefreshToken(testToken, "10")).toThrowWithMessage(
      JsonWebTokenError,
      "jwt audience invalid. expected: refresh",
    );
  });

  test("Reject refresh token with wrong issuer", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:40:31Z").getTime());

    const testToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNTA5MzEsImV4cCI6MTYyMzY4MTMzMSwiYXVkIjoicmVmcmVzaCIsImlzcyI6InVzZXJzIiwic3ViIjoiMTAifQ.Aw3FjtRtp50eeus_zrvLFoPpjJRM-wV5sRdrd3sYRPk";

    expect(() => decodeRefreshToken(testToken, "10")).toThrowWithMessage(
      JsonWebTokenError,
      "jwt issuer invalid. expected: gateway",
    );
  });

  test("Reject refresh token with wrong secret key", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:40:31Z").getTime());

    // signed with abc123
    const testToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNTA5MzEsImV4cCI6MTYyMzY4MTMzMSwiYXVkIjoicmVmcmVzaCIsImlzcyI6ImdhdGV3YXkiLCJzdWIiOiIxMCJ9.NZX6RETwxM4R0cBV5_Ubjo98gTeubPArTVKgs1BJpH8";

    expect(() => decodeRefreshToken(testToken, "10")).toThrowWithMessage(
      JsonWebTokenError,
      "invalid signature",
    );
  });
});

describe("Create refresh token", () => {
  test("Create refresh token", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const expectedToken =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MTYyNTA5MzEsImV4cCI6MTYyMzUwODUzMSwiYXVkIjoicmVmcmVzaCIsImlzcyI6ImdhdGV3YXkiLCJzdWIiOiIxMCJ9.8nF91uPV7ngknINxD0X9U58t-Z7JPwogQw9ngx6cNI4";

    expect(createRefreshToken("10")).toBe(expectedToken);
  });

  test("Cannot create refresh token with empty subject", () => {
    expect(() => createRefreshToken("")).toThrow("Empty subject not allowed");
  });
});

test("Clear identity tokens", async () => {
  const fakeContext = {
    setCookies: [],
  };

  await removeIdentityTokens(fakeContext);
  expect(fakeContext.setCookies).toContainEqual({
    name: "identity",
    value: "",
    options: {
      httpOnly: true,
      maxAge: -1,
      path: "/",
      sameSite: true,
      secure: false,
    },
  });
  expect(fakeContext.setCookies).toContainEqual({
    name: "refreshIdentity",
    value: "",
    options: {
      httpOnly: true,
      maxAge: -1,
      path: "/",
      sameSite: true,
      secure: false,
    },
  });
});
