import {
  Admin,
  Resource,
} from "react-admin";
import { Layout } from "./Layout";
import { dataProvider } from "./dataProvider";
import { authProvider } from "./authProvider";
import { APP_NAME } from "./constants"
import { Person } from "@mui/icons-material"
import { UserCreateForm, UserList, UserShow, UserEdit } from "./User"
export const App = () => (
  <Admin
    authProvider={authProvider}
    dataProvider={dataProvider}
    // i18nProvider={i18nProvider}
    // queryClient={queryClient}
    title={APP_NAME}
    layout={Layout}
  >
    <Resource
      name="users"
      options={undefined}
      icon={Person}
      list={UserList}
      edit={UserEdit}
      show={UserShow}
      create={UserCreateForm}
    />
  </Admin>
);
