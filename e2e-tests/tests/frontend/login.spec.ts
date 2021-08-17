import { nanoid } from "nanoid";
import { test, expect } from "@playwright/test";
import { PYCON_FRONTEND_URL } from "../config";

test.describe("User login", async () => {
  test("with not existent account fails", async ({ page }) => {
    const email = `e2e-does-not-exist-user@pythonit.dev`;
    const password = "fakelongpassword";

    await page.goto(`${PYCON_FRONTEND_URL}/en/login`);
    await page.waitForLoadState();

    await page.fill("data-testid=email-input", email);
    await page.fill("data-testid=password-input", password);
    await page.click("data-testid=login-button");

    await page.waitForLoadState();

    await expect(page).toHaveURL(/.*login/);
    await expect(
      page.locator("data-testid=wrong-username-or-password-alert"),
    ).toHaveText("Wrong username or password");
  });

  test("with improperly formatted email fails", async ({ page }) => {
    const email = `e2e-${nanoid()}-user@pythonit`;
    const password = "fakelongpassword";

    await page.goto(`${PYCON_FRONTEND_URL}/en/login`);
    await page.waitForLoadState();

    await page.fill("data-testid=email-input", email);
    await page.fill("data-testid=password-input", password);
    await page.click("data-testid=login-button");

    await page.waitForLoadState();

    await expect(page).toHaveURL(/.*login/);
    await expect(page.locator("data-testid=email-input-wrapper")).toContainText(
      "value is not a valid email address",
    );
  });
});
