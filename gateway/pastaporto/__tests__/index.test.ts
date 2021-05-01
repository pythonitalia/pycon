import { createRefreshToken, createIdentityToken } from "../identity";
import { canRefreshIdentity, createPastaporto } from "../index";
import { fetchUserInfo } from "../user-info";

const mockedFetchUserInfo = fetchUserInfo as jest.Mock;

jest.mock("../user-info", () => ({
  fetchUserInfo: jest.fn(),
}));

jest.mock("../../config");

describe("Pastaporto creation flow", () => {
  beforeEach(() => {
    mockedFetchUserInfo.mockReset();
  });

  test("Create without identity returns an unauthenticated pastaporto", async () => {
    const context = {
      setCookies: [],
    };

    const unauthenticated = await createPastaporto(null, context, null);
    expect(unauthenticated.userInfo).toBe(null);
    expect(unauthenticated.credentials).toStrictEqual([]);
  });

  test("Create from expired without refresh token fails", async () => {
    mockedFetchUserInfo.mockReturnValue({
      id: 1,
      email: "test@email.it",
      isStaff: false,
      isActive: true,
      jwtAuthId: 1,
    });

    const context = {
      setCookies: [],
    };

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const token = createIdentityToken("1", 1);

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-25 14:35:31Z").getTime());

    await expect(createPastaporto(token, context, null)).rejects.toThrow(
      "Identity is not valid (expired token)",
    );
    expect(context.setCookies).toStrictEqual([]);
  });

  test("Refresh token flow with expired identity", async () => {
    mockedFetchUserInfo.mockReturnValue({
      id: 1,
      email: "test@email.it",
      isStaff: false,
      isActive: true,
      jwtAuthId: 1,
    });

    const context = {
      setCookies: [],
    };

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const token = createIdentityToken("1", 1);

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-25 14:35:31Z").getTime());

    const refreshToken = createRefreshToken("1", 1);

    const pastaporto = await createPastaporto(token, context, refreshToken);
    expect(pastaporto.credentials).toStrictEqual(["authenticated"]);
    expect(pastaporto.userInfo).toHaveProperty("id", 1);
    expect(context.setCookies).toBeArrayOfSize(1);
    expect(context.setCookies[0]).toHaveProperty("name", "identity");
  });

  test("Auth fails with expired identity and refresh token", async () => {
    mockedFetchUserInfo.mockReturnValue({
      id: 1,
      email: "test@email.it",
      isStaff: false,
      isActive: true,
      jwtAuthId: 1,
    });

    const context = {
      setCookies: [],
    };

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const token = createIdentityToken("1", 1);
    const refreshToken = createRefreshToken("1", 1);

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2022-10-25 14:35:31Z").getTime());

    await expect(
      createPastaporto(token, context, refreshToken),
    ).rejects.toThrowError("Identity is not valid (expired token)");
  });

  test("If jwt auth id changed old tokens are invalid", async () => {
    mockedFetchUserInfo.mockReturnValue({
      id: 1,
      email: "test@email.it",
      isStaff: false,
      isActive: true,
      jwtAuthId: 2,
    });

    const context = {
      setCookies: [],
    };

    const token = createIdentityToken("1", 1);

    // This token is for jwt auth 1, API will return 2

    await expect(createPastaporto(token, context, null)).rejects.toThrow(
      "Not authenticated",
    );
    expect(context.setCookies).toBeArrayOfSize(2);
    expect(context.setCookies).toContainEqual({
      name: "identity",
      value: "",
      options: {
        httpOnly: true,
        maxAge: -1,
        path: "/",
        sameSite: "none",
        secure: false,
      },
    });
    expect(context.setCookies).toContainEqual({
      name: "refreshIdentity",
      value: "",
      options: {
        httpOnly: true,
        maxAge: -1,
        path: "/",
        sameSite: "none",
        secure: false,
      },
    });
  });

  test("Different jwt auth and expired identity, refresh token fails", async () => {
    mockedFetchUserInfo.mockReturnValue({
      id: 1,
      email: "test@email.it",
      isStaff: false,
      isActive: true,
      jwtAuthId: 2,
    });

    const context = {
      setCookies: [],
    };

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const token = createIdentityToken("1", 1);

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-25 14:35:31Z").getTime());

    const refreshToken = createRefreshToken("1", 1);

    await expect(
      createPastaporto(token, context, refreshToken),
    ).rejects.toThrow("Not authenticated");

    expect(context.setCookies).toBeArrayOfSize(2);
    expect(context.setCookies).toContainEqual({
      name: "identity",
      value: "",
      options: {
        httpOnly: true,
        maxAge: -1,
        path: "/",
        sameSite: "none",
        secure: false,
      },
    });
    expect(context.setCookies).toContainEqual({
      name: "refreshIdentity",
      value: "",
      options: {
        httpOnly: true,
        maxAge: -1,
        path: "/",
        sameSite: "none",
        secure: false,
      },
    });
  });
});

describe("Can refresh token", () => {
  test("rejects expired token", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const testToken = createRefreshToken("10", 1);

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2050-03-20 14:35:31Z").getTime());

    expect(
      canRefreshIdentity(testToken, { sub: "10", jwtAuthId: 1 }),
    ).toBeFalse();
  });

  test("rejects token for a different user", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const testToken = createRefreshToken("10", 1);

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2050-03-20 14:35:31Z").getTime());

    expect(
      canRefreshIdentity(testToken, { sub: "30", jwtAuthId: 1 }),
    ).toBeFalse();
  });

  test("accepts valid token", () => {
    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const testToken = createRefreshToken("10", 1);

    jest
      .useFakeTimers("modern")
      .setSystemTime(new Date("2021-04-20 14:35:31Z").getTime());

    expect(
      canRefreshIdentity(testToken, { sub: "10", jwtAuthId: 1 }),
    ).toBeTrue();
  });
});
