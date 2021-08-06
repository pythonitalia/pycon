import { test, expect } from "@playwright/test";

test.describe("User can login", () => {
  test.beforeEach(async ({ page }) => {
    page.setDefaultTimeout(5000);
    await page.goto("http://localhost:3000/en/login");
  });

  test("with email and password", async ({ page }) => {
    await page.fill('[data-testid="email-input"]', "e2e-user@pythonit.dev");
    await page.fill('[data-testid="password-input"]', "fake");
    await page.click('[data-testid="login-button"]');
    // todo
  });
});
