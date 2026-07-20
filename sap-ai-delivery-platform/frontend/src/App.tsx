import { FluentProvider, webLightTheme } from '@fluentui/react-components';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { TranscriptQueuePage } from './pages/TranscriptQueuePage';
import { RequirementViewPage } from './pages/RequirementViewPage';
import { FsReviewPage } from './pages/FsReviewPage';
import { TsReviewPage } from './pages/TsReviewPage';
import { RagSearchPage } from './pages/RagSearchPage';
import { KnowledgeExplorerPage } from './pages/KnowledgeExplorerPage';
import { AuditDashboardPage } from './pages/AuditDashboardPage';
import { WorkflowMonitorPage } from './pages/WorkflowMonitorPage';
import { AgentMonitorPage } from './pages/AgentMonitorPage';
import { McpMonitorPage } from './pages/McpMonitorPage';
import { ConfigurationPage } from './pages/ConfigurationPage';
import { AdministrationPage } from './pages/AdministrationPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <FluentProvider theme={webLightTheme}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<DashboardPage />} />
              <Route path="transcript-queue" element={<TranscriptQueuePage />} />
              <Route path="requirement-view" element={<RequirementViewPage />} />
              <Route path="fs-review" element={<FsReviewPage />} />
              <Route path="ts-review" element={<TsReviewPage />} />
              <Route path="rag-search" element={<RagSearchPage />} />
              <Route path="knowledge-explorer" element={<KnowledgeExplorerPage />} />
              <Route path="audit-dashboard" element={<AuditDashboardPage />} />
              <Route path="workflow-monitor" element={<WorkflowMonitorPage />} />
              <Route path="agent-monitor" element={<AgentMonitorPage />} />
              <Route path="mcp-monitor" element={<McpMonitorPage />} />
              <Route path="configuration" element={<ConfigurationPage />} />
              <Route path="administration" element={<AdministrationPage />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </FluentProvider>
    </QueryClientProvider>
  );
}

export default App;
