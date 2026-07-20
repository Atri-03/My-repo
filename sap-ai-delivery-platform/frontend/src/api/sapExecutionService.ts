import { resourceClient } from './client';
import type { Activation, AtcRemediation, AtcRun, ExecutionPlan, GeneratedObject, SapPackage, SapTransport } from './types';

export const sapPackagesApi = resourceClient<SapPackage>('sapExecution', '/packages');
export const sapTransportsApi = resourceClient<SapTransport>('sapExecution', '/transports');
export const generatedObjectsApi = resourceClient<GeneratedObject>('sapExecution', '/objects');
export const activationsApi = resourceClient<Activation>('sapExecution', '/activations');
export const atcRunsApi = resourceClient<AtcRun>('sapExecution', '/atc-runs');
export const atcRemediationsApi = resourceClient<AtcRemediation>('sapExecution', '/atc-remediations');
export const executionPlansApi = resourceClient<ExecutionPlan>('sapExecution', '/architect/plans');
