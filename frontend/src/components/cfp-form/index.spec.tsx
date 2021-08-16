import {
  act,
  actWait,
  MockedProvider,
  render,
  screen,
  wait,
} from "~/test-utils";
import { CfpFormDocument, TagsDocument } from "~/types";

import { CfpForm } from "./index";

const MOCKS = [
  {
    request: {
      query: CfpFormDocument,
      variables: {
        conference: "unit-tests",
      },
    },
    result: {
      data: {
        conference: {
          id: "unit-tests",
          durations: [
            {
              name: "Short talk",
              id: 1,
              allowedSubmissionTypes: [
                {
                  id: 1,
                  name: "Talk",
                },
              ],
            },
            {
              name: "Long talk",
              id: 2,
              allowedSubmissionTypes: [
                {
                  id: 2,
                  name: "Workshop",
                },
              ],
            },
          ],
          audienceLevels: [
            {
              id: 1,
              name: "Beginner",
            },
            {
              id: 2,
              name: "Advanced",
            },
          ],
          submissionTypes: [
            {
              id: 1,
              name: "Talk",
            },
            {
              id: 2,
              name: "Workshop",
            },
          ],
          topics: [
            {
              id: 1,
              name: "Web",
            },
            {
              id: 2,
              name: "Infrastructure",
            },
          ],
          languages: [
            {
              code: "en",
              id: 1,
              name: "English",
            },
            {
              code: "it",
              id: 2,
              name: "Italian",
            },
          ],
        },
      },
    },
  },

  {
    request: {
      query: TagsDocument,
    },
    result: {
      data: {
        submissionTags: [
          {
            id: 1,
            name: "GraphQL",
          },
          {
            id: 2,
            name: "Python",
          },
        ],
      },
    },
  },
];

describe("Cfp Form", () => {
  test("Renders", async () => {
    render(
      <MockedProvider mocks={MOCKS}>
        <CfpForm
          onSubmit={jest.fn()}
          conferenceCode="unit-tests"
          submission={null}
          loading={false}
          error={null}
          data={null}
        />
      </MockedProvider>,
    );

    await actWait(1);

    // Make sure we render all the formats from the API
    expect(screen.getByText("Choose a format")).toBeInTheDocument();
    expect(screen.getByLabelText("Talk")).toBeInTheDocument();
    expect(screen.getByLabelText("Workshop")).toBeInTheDocument();
  });
});
