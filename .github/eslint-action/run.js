const {chunk} = require("lodash");
const request = require("./request");

const {
    GITHUB_SHA,
    GITHUB_EVENT_PATH,
    GITHUB_TOKEN,
    GITHUB_WORKSPACE
} = process.env;
const event = require(GITHUB_EVENT_PATH);
const { repository } = event;
const {
    owner: { login: owner }
} = repository;
const { name: repo } = repository;

const checkName = "ESLint check";

const headers = {
    "Content-Type": "application/json",
    Accept: "application/vnd.github.antiope-preview+json",
    Authorization: `Bearer ${GITHUB_TOKEN}`,
    "User-Agent": "eslint-action"
};

async function createCheck() {
    const body = {
        name: checkName,
        head_sha: GITHUB_SHA,
        status: "in_progress",
        started_at: new Date()
    };

    const { data } = await request(
        `https://api.github.com/repos/${owner}/${repo}/check-runs`,
        {
            method: "POST",
            headers,
            body
        }
    );
    const { id } = data;
    return id;
}

function eslint() {
    const eslint = require("eslint");

    const cli = new eslint.CLIEngine({
        extensions: [".jsx", ".js", ".tsx", ".ts"]
    });
    const report = cli.executeOnFiles(["src/"]);

    // fixableErrorCount, fixableWarningCount are available too
    const { results, errorCount, warningCount } = report;

    const levels = ["", "warning", "failure"];

    const annotations = [];

    for (const result of results) {
        const { filePath, messages } = result;
        const path = filePath.substring(GITHUB_WORKSPACE.length + 1);
        for (const msg of messages) {
            const { line, severity, ruleId, message } = msg;
            const annotationLevel = levels[severity];
            annotations.push({
                path,
                start_line: line,
                end_line: line,
                annotation_level: annotationLevel,
                message: `[${ruleId}] ${message}`
            });
        }
    }

    return {
        conclusion: errorCount > 0 ? "failure" : "success",
        output: {
            title: checkName,
            summary: `${errorCount} error(s), ${warningCount} warning(s) found`
        },
        annotations
    };
}

async function updateCheck(id, conclusion, output, annotations) {
    // github has a limit of 50 annotations per request so we send
    // multiple requests
    const annotationChunks = chunk(annotations, 50);

    const requests = annotationChunks.map(chunk => {
        const body = {
            name: checkName,
            head_sha: GITHUB_SHA,
            status: "completed",
            completed_at: new Date(),
            conclusion,
            output: {
                ...output,
                annotations: chunk
            }
        };

        return request(
            `https://api.github.com/repos/${owner}/${repo}/check-runs/${id}`,
            {
                method: "PATCH",
                headers,
                body
            }
        );
    });

    await Promise.all(requests);
}

function exitWithError(err) {
    console.error("Error", err.stack);
    if (err.data) {
        console.error(err.data);
    }
    process.exit(1);
}

async function run() {
    const id = await createCheck();
    try {
        const { conclusion, output, annotations } = eslint();

        await updateCheck(id, conclusion, output, annotations);

        if (conclusion === "failure") {
            process.exit(78);
        }
    } catch (err) {
        await updateCheck(id, "failure");
        exitWithError(err);
    }
}

run().catch(exitWithError);
