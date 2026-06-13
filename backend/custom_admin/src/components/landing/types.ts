export type AdminModel = {
  name: string;
  object_name: string;
  admin_url: string | null;
  add_url: string | null;
  view_only: boolean;
  app_label: string;
  app_name: string;
};

export type Group = {
  title: string;
  models: AdminModel[];
};

export type AdminApp = {
  app_label: string;
  name: string;
  models: AdminModel[];
};

export type QuickLink = {
  title: string;
  description: string;
  url: string;
};
