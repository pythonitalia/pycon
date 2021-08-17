import { nanoid } from "nanoid";
import { test, expect } from "@playwright/test";

test.describe("User register and login", async () => {
  test("with email and password", async ({ browser }) => {
    const email = `e2e-${nanoid()}-user@pythonit.dev`;
    const password = "fakelongpassword";

    const signUpContext = await browser.newContext();
    const signUpPage = await signUpContext.newPage();

    signUpPage.setDefaultTimeout(5000);
    await signUpPage.goto("http://localhost:3000/en/signup");

    await signUpPage.fill("data-testid=email-input", email);
    await signUpPage.fill("data-testid=password-input", password);
    await signUpPage.click("data-testid=signup-button");

    await signUpPage.waitForLoadState();
    await signUpPage.waitForNavigation();

    await expect(signUpPage).toHaveURL(/.*profile/);

    await signUpContext.close();

    const loginContext = await browser.newContext();
    const loginPage = await loginContext.newPage();

    await loginPage.goto("http://localhost:3000/en/login");
    await loginPage.fill("data-testid=email-input", email);
    await loginPage.fill("data-testid=password-input", password);
    await loginPage.click("data-testid=login-button");

    await loginPage.waitForLoadState();
    await loginPage.waitForNavigation();

    await expect(loginPage).toHaveURL(/.*profile/);

    await loginContext.close();
  });

  test("with wrong password fails", async ({ browser }) => {
    const email = `e2e-${nanoid()}-user@pythonit.dev`;
    const password = "fakelongpassword";

    const signUpContext = await browser.newContext();
    const signUpPage = await signUpContext.newPage();

    signUpPage.setDefaultTimeout(5000);
    await signUpPage.goto("http://localhost:3000/en/signup");

    await signUpPage.fill("data-testid=email-input", email);
    await signUpPage.fill("data-testid=password-input", password);
    await signUpPage.click("data-testid=signup-button");

    await signUpPage.waitForLoadState();
    await signUpPage.waitForNavigation();

    await expect(signUpPage).toHaveURL(/.*profile/);

    await signUpContext.close();

    const loginContext = await browser.newContext();
    const loginPage = await loginContext.newPage();

    await loginPage.goto("http://localhost:3000/en/login");
    await loginPage.fill("data-testid=email-input", email);
    await loginPage.fill("data-testid=password-input", "not-valid-password");
    await loginPage.click("data-testid=login-button");

    await loginPage.waitForLoadState();

    await expect(loginPage).toHaveURL(/.*login/);
    await expect(
      loginPage.locator("data-testid=wrong-username-or-password-alert"),
    ).toContainText("Wrong username or password");

    await loginContext.close();
  });
});
