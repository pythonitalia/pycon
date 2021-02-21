export const DashboardPageWrapper: React.FC = ({ children }) => (
  <main
    className="flex-1 relative z-0 overflow-y-auto focus:outline-none"
    tabIndex={0}
  >
    {children}
  </main>
);
