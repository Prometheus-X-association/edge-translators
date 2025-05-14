import simpleRestProvider from "ra-data-simple-rest";
import { DataProvider, fetchUtils } from "react-admin";
import { API_URL } from "./constants"

const httpClient = (
    url: string,
    options: fetchUtils.Options = {}
): Promise<{
    status: number;
    headers: Headers;
    body: string;
    json: any;
}> => {
    if (!options.headers) {
        options.headers = new Headers({ Accept: 'application/json' });
    }
    
    const auth = localStorage.getItem('auth');
    const { access_token } = auth ? JSON.parse(auth) : { access_token: "" };
    
    if (access_token) {
        (options.headers as Headers).set('Authorization', `Bearer ${access_token}`);
    }

    return fetchUtils.fetchJson(url, options);
};

export const dataProvider: DataProvider = {
    ...simpleRestProvider(API_URL, httpClient),
  
    getList: async (resource, params) => {
      const page = params.pagination?.page;
      const perPage = params.pagination?.perPage;
      const sort = params.sort?.field;
      const order = params.sort?.order;

      const query = {
        page: page,
        per_page: perPage,
        sort: sort,
        order: order,
        filter: JSON.stringify(params.filter),
      };
  
      const url = `${API_URL}/${resource}?${fetchUtils.queryParameters(query)}`;
  
      const { json, headers } = await httpClient(url);
  
      return {
        data: json,
        total: parseInt(headers.get("Content-Range")?.split("/")[1] ?? "0", 10),
      };
    },
  };