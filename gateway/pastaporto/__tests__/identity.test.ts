import jwt, { JsonWebTokenError, TokenExpiredError } from "jsonwebtoken";
import {
  createIdentityToken,
  createRefreshToken,
  decodeIdentity,
  decodeRefreshToken,
  removeIdentityTokens,
} from "../identity";

const TEST_PRIVATE_KEY = `-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQC4d8AeK7bfuoc0yPtHeuHjo9MT25DP0JZoHbWscpZ9yjKlZvHv
4pGmwb481KRX+YwA4YazVlZ6bjd7iuaVuNry+LYhURr7IUakf1MR++DFqNFu6AFi
sZ3Nn4K0JoSJh+6NkyDV8D1G6P0phKjL5kIuUjrWIfwAlwJLzI2gUObm9wIDAQAB
AoGAHyF2dqEB97fO4YWZgnKmdHhNQuinA6s79s4svrGH3CqnaWp6IfWmhvHjXPi1
03L1waBNzy4e4gJ/soW6bEIKEPV3gFynVWVYA9AtDyjRCwbI1TzEFdqR961oySlp
g/6nM2VKZw8Zsjwgu3iRqiRV1LZLZ+wu4IvudWk2Yvc6tGECQQDr9edl4WzfzPbj
PP7kqbkiJ//HUkUA2x6GVt9Z3h1nNuMfed6fSMuKc9sFIZQ1YFPGunsZ3rZ+fgGz
eRuuSrk9AkEAyCJTMPL1MhLJ2A/LSw72fpwxnRbAZR83xP/6hgmkUtM1gSDND/E1
4zxghbSFmhtTRibdxcITT/+s5Q0zH0jcQwJADqDlIqTSGiHb4ISkjMqU5rAyJEpO
atoqz0tNd4XUrtRxSj9E9P0PWVsLZgsJ5DE/oF9pSFZNXBQ1yMmmVKzfRQJAQzp8
laHXygVTtne/w6v4E5nmdK2S3aU597xBbMtKXuRCQelB2Uwe3QGILwHwK09ojtU5
hFfoYuQxMRRZCvZPvwJAB70RhOrVaX83Oboqqu8rsCM1HDrHGPNznUfpOnUUkUC7
LZsBajFgIDr1OMCUeeo23oNOgdkpPPfGM5VKTLciCQ==
-----END RSA PRIVATE KEY-----`;

jest.mock("../../config", () => ({
  IDENTITY_SECRET: "abc",
  IS_DEV: true,
}));

describe("Decode Identity", () => {
  test("Decode valid not expired identity", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:00:00Z").getTime());

    const testToken = jwt.sign({}, "abc", {
      issuer: "gateway",
      audience: "identity",
      subject: "10",
      expiresIn: "15m",
      algorithm: "HS256",
    });

    expect(decodeIdentity(testToken, false)).toContainEntry(["sub", "10"]);
  });

  test("Allow expired tokens if specified", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:30:00Z").getTime());

    const testToken = jwt.sign({}, "abc", {
      issuer: "gateway",
      audience: "identity",
      subject: "10",
      expiresIn: "15m",
      algorithm: "HS256",
    });

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 15:00:00Z").getTime());

    expect(decodeIdentity(testToken, true)).toContainEntry(["sub", "10"]);
  });

  test("Ignore expired tokens by default", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:30:00Z").getTime());

    const testToken = jwt.sign({}, "abc", {
      issuer: "gateway",
      audience: "identity",
      subject: "10",
      expiresIn: "15m",
      algorithm: "HS256",
    });

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 15:30:00Z").getTime());

    expect(() => decodeIdentity(testToken, false)).toThrow(TokenExpiredError);
  });

  test.each([true, false])(
    "Reject tokens not issued by gateway and expiration %p",
    (ignoreExpiration) => {
      jest
        .useFakeTimers("modern")
        .setSystemTime(new Date("2021-03-20 14:25:00Z").getTime());

      const testToken = jwt.sign({}, "abc", {
        issuer: "other",
        audience: "identity",
        subject: "10",
        expiresIn: "15m",
        algorithm: "HS256",
      });

      expect(() =>
        decodeIdentity(testToken, ignoreExpiration),
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
      jest
        .useFakeTimers("modern")
        .setSystemTime(new Date("2021-03-20 14:35:00Z").getTime());

      const testToken = jwt.sign({}, "abc", {
        issuer: "gateway",
        audience: "refresh",
        subject: "10",
        expiresIn: "15m",
        algorithm: "HS256",
      });

      expect(() =>
        decodeIdentity(testToken, ignoreExpiration),
      ).toThrowWithMessage(
        JsonWebTokenError,
        "jwt audience invalid. expected: identity",
      );
    },
  );

  test.each([true, false])(
    "Ignore tokens with None algo and with expiration %p",
    (ignoreExpiration) => {
      jest
        .useFakeTimers("modern")
        .setSystemTime(new Date("2021-03-20 14:40:00Z").getTime());

      const testToken = jwt.sign({}, "abc", {
        issuer: "gateway",
        audience: "identity",
        subject: "10",
        expiresIn: "15m",
        algorithm: "none",
      });

      expect(() =>
        decodeIdentity(testToken, ignoreExpiration),
      ).toThrowWithMessage(JsonWebTokenError, "jwt signature is required");
    },
  );

  test.each([true, false])(
    "Ignore tokens not using HS256 algo and with expiration %p",
    async (ignoreExpiration) => {
      jest
        .useFakeTimers("modern")
        .setSystemTime(new Date("2021-03-20 14:45:00Z").getTime());

      const testToken = jwt.sign({}, TEST_PRIVATE_KEY, {
        issuer: "gateway",
        audience: "identity",
        subject: "10",
        expiresIn: "15m",
        algorithm: "RS256",
      });

      await expect(() =>
        decodeIdentity(testToken, ignoreExpiration),
      ).toThrowWithMessage(JsonWebTokenError, "invalid algorithm");
    },
  );

  test.each([true, false])(
    "Reject tokens with wrong secret and check expiration %p",
    async (ignoreExpiration) => {
      jest
        .useFakeTimers("modern")
        .setSystemTime(new Date("2021-03-20 14:40:31Z").getTime());

      const testToken = jwt.sign({}, "abc123", {
        issuer: "gateway",
        audience: "identity",
        subject: "10",
        expiresIn: "15m",
        algorithm: "HS256",
      });

      await expect(() =>
        decodeIdentity(testToken, ignoreExpiration),
      ).toThrowWithMessage(JsonWebTokenError, "invalid signature");
    },
  );
});

describe("Create identity", () => {
  test("Create identity", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const expectedToken = jwt.sign({}, "abc", {
      issuer: "gateway",
      audience: "identity",
      subject: "10",
      expiresIn: "15m",
      algorithm: "HS256",
    });

    expect(createIdentityToken("10")).toBe(expectedToken);
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

    const testToken = jwt.sign({}, "abc", {
      issuer: "gateway",
      audience: "refresh",
      subject: "10",
      expiresIn: "30 days",
      algorithm: "HS256",
    });

    expect(decodeRefreshToken(testToken, "10")).toContainEntry(["sub", "10"]);
  });

  test("Reject refresh token for another subject", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:40:31Z").getTime());

    const testToken = jwt.sign({}, "abc", {
      issuer: "gateway",
      audience: "refresh",
      subject: "10",
      expiresIn: "30 days",
      algorithm: "HS256",
    });

    expect(() => decodeRefreshToken(testToken, "20")).toThrowWithMessage(
      JsonWebTokenError,
      "jwt subject invalid. expected: 20",
    );
  });

  test("Reject expired refresh token", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2050-03-20 14:40:31Z").getTime());

    const testToken = jwt.sign({}, "abc", {
      issuer: "gateway",
      audience: "refresh",
      subject: "10",
      expiresIn: "5 days",
      algorithm: "HS256",
    });

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2050-04-01 14:40:31Z").getTime());

    expect(() => decodeRefreshToken(testToken, "10")).toThrow(
      TokenExpiredError,
    );
  });

  test("Reject refresh token with wrong audience", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:40:31Z").getTime());

    const testToken = jwt.sign({}, "abc", {
      issuer: "gateway",
      audience: "identity",
      subject: "10",
      expiresIn: "5 days",
      algorithm: "HS256",
    });

    expect(() => decodeRefreshToken(testToken, "10")).toThrowWithMessage(
      JsonWebTokenError,
      "jwt audience invalid. expected: refresh",
    );
  });

  test("Reject refresh token with wrong issuer", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:40:31Z").getTime());

    const testToken = jwt.sign({}, "abc", {
      issuer: "users",
      audience: "refresh",
      subject: "10",
      expiresIn: "5 days",
      algorithm: "HS256",
    });

    expect(() => decodeRefreshToken(testToken, "10")).toThrowWithMessage(
      JsonWebTokenError,
      "jwt issuer invalid. expected: gateway",
    );
  });

  test("Reject refresh token with wrong secret key", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:40:31Z").getTime());

    const testToken = jwt.sign({}, "abc123", {
      issuer: "gateway",
      audience: "refresh",
      subject: "10",
      expiresIn: "5 days",
      algorithm: "HS256",
    });

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

    const expectedToken = jwt.sign({}, "abc", {
      issuer: "gateway",
      audience: "refresh",
      subject: "10",
      expiresIn: "84 days",
      algorithm: "HS256",
    });

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
