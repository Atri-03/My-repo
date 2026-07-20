import { resourceClient } from './client';
import type { Project, Tenant, User } from './types';

export const tenantsApi = resourceClient<Tenant>('user', '/tenants');
export const projectsApi = resourceClient<Project>('user', '/projects');
export const usersApi = resourceClient<User>('user', '/users');
