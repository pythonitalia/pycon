import * as cheerio from "cheerio";
import * as fs from "node:fs/promises";
import * as pathModule from "node:path";

const BASE_OUTPUT_PATH = "output";

const PAGES_TO_IGNORE = [
  "/en/login",
  "/it/login",
  "/en/tickets",
  "/it/tickets",
  "/it/",
  "/en/",
  "/en/_error",
  "/it/_error",
];

const VISITED_URLS = new Set();

const scape = async (url: string, host: string) => {
  console.log(`Scraping: ${url}`);
  try {
    const response = await fetch(url);
    const path = url.replace(host, "");

    const body = await response.text();
    const newUrls = await findUrls(body);

    await storePage(path, body);

    for (const newUrl of newUrls) {
      await scape(`${host}${newUrl}`, host);
    }

    console.log("links", newUrls);
  } catch (e) {
    console.log("Error while scraping", e);
  }
};

const storePage = async (path: string, body: string) => {
  const finalPath = `${BASE_OUTPUT_PATH}/${path}/index.html`;
  await fs.mkdir(pathModule.dirname(finalPath), { recursive: true });
  await fs.writeFile(finalPath, body);
};

const findUrls = async (body: string) => {
  const parsableBody = cheerio.load(body);
  const links = parsableBody("a, script");
  const urlsFound: Set<string> = new Set();

  links.map((_, linkElement) => {
    const link = linkElement.attribs.href ?? linkElement.attribs.src;

    if (!link) {
      return;
    }

    if (link.startsWith("http") || link.startsWith("mailto")) {
      return;
    }

    if (PAGES_TO_IGNORE.includes(link)) {
      return;
    }

    if (VISITED_URLS.has(link)) {
      return;
    }

    VISITED_URLS.add(link);
    urlsFound.add(link);
  });

  return urlsFound;
};

(async () => {
  try {
    await fs.rm(BASE_OUTPUT_PATH, { recursive: true });
  } catch (e) {}

  await fs.mkdir(BASE_OUTPUT_PATH);

  await scape("https://pycon.it/en", "https://pycon.it");
})();
