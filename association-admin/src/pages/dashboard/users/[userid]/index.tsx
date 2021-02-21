import Head from "next/head";
import { useRouter } from "next/router";

import { BackIcon } from "~/components/back-icon";
import { Button } from "~/components/button";
import { Card } from "~/components/card";
import { DashboardPageWrapper } from "~/components/dashboard-page-wrapper";
import { Heading } from "~/components/heading";
import { Loading } from "~/components/loading";
import { PageHeader } from "~/components/page-header";
import { Table } from "~/components/table";
import { UserPills } from "~/components/user-pills";

import { useUserDetailQuery } from "./user.generated";

type UserInfoProps = {
  label: string;
  text: string | React.ReactElement;
};

const UserInfo: React.FC<UserInfoProps> = ({ label, text }) => (
  <li className="flex flex-col">
    <span className="text-sm font-medium text-gray-500">{label}</span>
    <span className="mt-1 text-sm text-gray-900">{text}</span>
  </li>
);

const valueOrPlaceholder = (value: string, placeholder: string = "Unset") =>
  value || placeholder;

const UserDetail = () => {
  const { query } = useRouter();
  const userId = query.userid as string;
  const [{ fetching, data, error }] = useUserDetailQuery({
    variables: {
      id: userId,
    },
    pause: typeof userId === "undefined",
  });

  if (!userId) {
    return null;
  }

  if (fetching) {
    return <Loading />;
  }

  if (error) {
    // TODO Handle error
    return null;
  }

  const user = data?.user;

  return (
    <>
      <Head>
        <title>User</title>
      </Head>
      <DashboardPageWrapper>
        <PageHeader
          backTo="back"
          headingContent={user?.fullname || user?.name || user?.email}
        >
          <div className="mt-2 -ml-2">
            <UserPills user={user} />
          </div>
        </PageHeader>

        <div className="px-6">
          <div className="grid grid-cols-1 gap-3">
            <Card
              heading={
                <Heading
                  subtitle="Personal details about the user"
                  size="medium"
                >
                  User information
                </Heading>
              }
            >
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <UserInfo label="ID" text={`${user.id}`} />
                <UserInfo
                  label="Email"
                  text={
                    <>
                      {valueOrPlaceholder(user.email)}
                      <Button
                        type="button"
                        href={`mailto:${encodeURIComponent(user.email)}`}
                        block={false}
                        className="mt-1"
                      >
                        Contact user
                      </Button>
                    </>
                  }
                />
                <UserInfo
                  label="Fullname"
                  text={valueOrPlaceholder(user.fullname)}
                />
                <UserInfo label="Name" text={valueOrPlaceholder(user.name)} />
                <UserInfo
                  label="Gender"
                  text={valueOrPlaceholder(user.gender)}
                />
                <UserInfo
                  label="Date of birth"
                  text={valueOrPlaceholder(user.dateBirth)}
                />
                <UserInfo
                  label="Country"
                  text={valueOrPlaceholder(user.country)}
                />
              </ul>
            </Card>
            <Card
              heading={<Heading size="medium">Association history</Heading>}
            >
              <Table
                border
                keyGetter={(item) => `${item.id}`}
                rowGetter={(item) => [
                  "20 Gennaio 2020",
                  "20 Gennaio 2021",
                  "Stripe",
                ]}
                data={[{ id: 1 }, { id: 2 }, { id: 3 }]}
                headers={["Start", "End", "Where"]}
              />
            </Card>
          </div>
        </div>
      </DashboardPageWrapper>
    </>
  );
};

export default UserDetail;
