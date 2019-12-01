/** @jsx jsx */
import { Box, Flex, Heading, Text } from "@theme-ui/components";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { MyProfileQuery } from "../../generated/graphql-backend";

export const MyOrders: React.SFC<{ profile: MyProfileQuery }> = ({
  profile: {
    me: { orders },
  },
}) => (
  <Box
    sx={{
      borderTop: "primary",
    }}
  >
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        my: 4,
        px: 3,
      }}
    >
      <Heading mb={2} as="h2">
        <FormattedMessage id="profile.myOrders" />
      </Heading>

      {orders.map(order => (
        <Box
          sx={{
            my: 3,
            py: 3,
            borderTop: "primary",
            borderColor: "violet",
          }}
          key={order.code}
        >
          <Heading
            as="h3"
            sx={{
              color: "orange",
            }}
          >
            <FormattedMessage id="profile.orderId">
              {text => `${text}${order.code}`}
            </FormattedMessage>
          </Heading>

          <Flex
            sx={{
              display: "inline-flex",
              border: "primary",
              borderRight: "none",
              my: 3,
            }}
          >
            <Box
              sx={{
                borderRight: "primary",
                p: 2,
              }}
            >
              <FormattedMessage id="profile.status">
                {statusLabel => (
                  <FormattedMessage
                    id={`profile.status.${order.status
                      .toString()
                      .toLowerCase()}`}
                  >
                    {status => `${statusLabel}${status}`}
                  </FormattedMessage>
                )}
              </FormattedMessage>
            </Box>
            <Box
              sx={{
                borderRight: "primary",
                p: 2,
              }}
            >
              <FormattedMessage id="profile.price">
                {text => `${text}${order.total}`}
              </FormattedMessage>
            </Box>
            <Box
              sx={{
                borderRight: "primary",
                p: 2,
              }}
            >
              <a href={order.url} target="_blank" rel="noopener noreferrer">
                <FormattedMessage id="profile.manageOrder" />
              </a>
            </Box>
          </Flex>

          <Heading
            as="h3"
            sx={{
              my: 2,
            }}
          >
            <FormattedMessage id="profile.items" />
          </Heading>

          <Box as="ul">
            {order.positions.map(position => (
              <Box as="li" key={position.id}>
                <Text
                  sx={{
                    fontWeight: "bold",
                    fontFamily: "heading",
                    fontSize: 2,
                    mt: 20,
                    mb: 1,
                  }}
                >
                  {position.name}
                </Text>
                <Text as="p">
                  <FormattedMessage id="profile.ticketFor">
                    {text =>
                      `${text} ${position.attendeeName}` +
                      (position.attendeeEmail
                        ? `(${position.attendeeEmail})`
                        : "")
                    }
                  </FormattedMessage>
                </Text>
                <Text as="p">
                  <FormattedMessage id="profile.price">
                    {text => `${text}${position.price}`}
                  </FormattedMessage>
                </Text>
              </Box>
            ))}
          </Box>
        </Box>
      ))}
    </Box>
  </Box>
);
