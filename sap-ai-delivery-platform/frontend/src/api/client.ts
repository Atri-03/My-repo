import axios, { type AxiosInstance } from 'axios';
import { serviceBaseUrls, type ServiceName } from './config';

const clients = new Map<ServiceName, AxiosInstance>();

/** Returns (and memoizes) an Axios instance configured for a backend service. */
export function getClient(service: ServiceName): AxiosInstance {
  let client = clients.get(service);
  if (!client) {
    client = axios.create({
      baseURL: serviceBaseUrls[service],
      headers: { 'Content-Type': 'application/json' },
    });
    clients.set(service, client);
  }
  return client;
}

/** Generic REST resource helpers (list/get/create/update/remove) for a given path. */
export function resourceClient<TRead, TCreate = Partial<TRead>, TUpdate = Partial<TRead>>(
  service: ServiceName,
  path: string,
) {
  return {
    list: async (params?: Record<string, unknown>): Promise<TRead[]> => {
      const { data } = await getClient(service).get<TRead[]>(path, { params });
      return data;
    },
    get: async (id: string): Promise<TRead> => {
      const { data } = await getClient(service).get<TRead>(`${path}/${id}`);
      return data;
    },
    create: async (payload: TCreate): Promise<TRead> => {
      const { data } = await getClient(service).post<TRead>(path, payload);
      return data;
    },
    update: async (id: string, payload: TUpdate): Promise<TRead> => {
      const { data } = await getClient(service).patch<TRead>(`${path}/${id}`, payload);
      return data;
    },
    remove: async (id: string): Promise<void> => {
      await getClient(service).delete(`${path}/${id}`);
    },
  };
}

/** Fetches the `/health` endpoint of a service (mounted outside the versioned API prefix). */
export async function getServiceHealth(service: ServiceName): Promise<{ status: string; service: string }> {
  const base = serviceBaseUrls[service].replace(/\/api\/v1\/?$/, '');
  const { data } = await axios.get<{ status: string; service: string }>(`${base}/health`);
  return data;
}
