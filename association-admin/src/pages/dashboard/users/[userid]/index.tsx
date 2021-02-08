import { Heading } from "~/components/heading";

const UserDetail = () => (
  <main
    className="flex-1 relative z-0 overflow-y-auto focus:outline-none"
    tabIndex={0}
  >
    <div className="border-b border-gray-200 px-6 py-4">
      <div className="flex-1 min-w-0">
        <Heading>User</Heading>
      </div>
    </div>
  </main>
);

export default UserDetail;
