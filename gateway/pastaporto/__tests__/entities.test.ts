import jwt from "jsonwebtoken";

import { Credential, Pastaporto, UserInfo } from "../entities";
import { decodeIdentity } from "../identity";
import { fetchUserInfo } from "../user-info";

jest.mock("../../config");

const mockedFetchUserInfo = fetchUserInfo as jest.Mock;
const mockedDecodeIdentity = decodeIdentity as jest.Mock;

jest.mock("../identity", () => ({
  decodeIdentity: jest.fn(() => ({
    sub: "10",
  })),
}));

jest.mock("../user-info", () => ({
  fetchUserInfo: jest.fn(),
}));

describe("Unauthenticated pastaporto", () => {
  test("Create unauthenticated pastaporto", () => {
    const unauthenticated = Pastaporto.unauthenticated();
    expect(unauthenticated.userInfo).toBeNull();
    expect(unauthenticated.credentials).toBeEmpty();
  });

  test("Sign unauthenticated pastaporto", () => {
    jest.setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const unauthenticated = Pastaporto.unauthenticated();
    const expectedToken = jwt.sign(
      {
        userInfo: null,
        credentials: [],
      },
      "abc",
      {
        issuer: "gateway",
        expiresIn: "1m",
        algorithm: "HS256",
      },
    );

    expect(unauthenticated.sign()).toBe(expectedToken);
  });
});

describe("Pastaporto", () => {
  beforeEach(() => {
    mockedDecodeIdentity.mockClear();
    mockedFetchUserInfo.mockReset();
  });

  test("Create pastaporto from identity token", async () => {
    mockedFetchUserInfo.mockReturnValue({
      id: 10,
      email: "test@email.it",
      isStaff: false,
      isActive: true,
    });

    const pastaporto = await Pastaporto.fromIdentityToken("fake");

    expect(mockedDecodeIdentity).toBeCalledTimes(1);
    expect(mockedDecodeIdentity).toBeCalledWith("fake");

    expect(mockedFetchUserInfo).toBeCalledTimes(1);
    expect(mockedFetchUserInfo).toBeCalledWith("10");

    expect(pastaporto.userInfo).toStrictEqual(
      new UserInfo(10, "test@email.it", false),
    );
    expect(pastaporto.credentials).toStrictEqual([Credential.AUTHENTICATED]);
  });

  test("Create pastaporto from staff identity token", async () => {
    mockedFetchUserInfo.mockReturnValue({
      id: 10,
      email: "test@email.it",
      isStaff: true,
      isActive: true,
    });

    const pastaporto = await Pastaporto.fromIdentityToken("fake");

    expect(mockedFetchUserInfo).toBeCalledWith("10");

    expect(pastaporto.userInfo).toStrictEqual(
      new UserInfo(10, "test@email.it", true),
    );
    expect(pastaporto.credentials).toStrictEqual([
      Credential.AUTHENTICATED,
      Credential.STAFF,
    ]);
  });

  test("Raises an error if the user is not active", async () => {
    mockedFetchUserInfo.mockReturnValue({
      id: 10,
      email: "test@email.it",
      isStaff: true,
      isActive: false,
    });

    expect(Pastaporto.fromIdentityToken("fake")).rejects.toThrow(
      "No user found",
    );
    expect(mockedFetchUserInfo).toBeCalledWith("10");
  });

  test("Raises an error if the user is not found", async () => {
    mockedFetchUserInfo.mockReturnValue(null);

    expect(Pastaporto.fromIdentityToken("fake")).rejects.toThrow(
      "No user found",
    );
    expect(mockedFetchUserInfo).toBeCalledWith("10");
  });

  test("Sign authenticated pastaporto", () => {
    jest.setSystemTime(new Date("2021-03-20 14:35:31Z").getTime());

    const pastaporto = new Pastaporto(new UserInfo(5, "test@email.it", false), [
      Credential.AUTHENTICATED,
    ]);

    const expectedToken = jwt.sign(
      {
        userInfo: {
          id: 5,
          email: "test@email.it",
          isStaff: false,
        },
        credentials: [Credential.AUTHENTICATED],
      },
      "abc",
      {
        issuer: "gateway",
        expiresIn: "1m",
        algorithm: "HS256",
      },
    );

    expect(pastaporto.sign()).toBe(expectedToken);
  });
});
