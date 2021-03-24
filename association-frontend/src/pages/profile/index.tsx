import { userInfo } from "os";

import { useMeQuery } from "~/components/user-provider/me.generated";

const ProfilePage = (props) => {
  const [{ data, fetching, error }] = useMeQuery();
  console.log(data);
  return (
    <div>
      <div className="relative bg-white">
        <div className="flex justify-between items-center max-w-7xl mx-auto px-4 py-6 sm:px-6 md:justify-start md:space-x-10 lg:px-8">
          <h1>Hello {data?.me.name}</h1>
          <p>{data?.me.email}</p>
        </div>
      </div>
    </div>
  );
};
export default ProfilePage;
