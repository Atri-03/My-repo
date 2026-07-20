FROM node:22-slim AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ARG VITE_TRANSCRIPT_SERVICE_URL
ARG VITE_DOCUMENT_EXTRACTION_SERVICE_URL
ARG VITE_FS_SERVICE_URL
ARG VITE_TS_SERVICE_URL
ARG VITE_REVIEW_SERVICE_URL
ARG VITE_APPROVAL_SERVICE_URL
ARG VITE_AUDIT_SERVICE_URL
ARG VITE_RAG_SERVICE_URL
ARG VITE_USER_SERVICE_URL
ARG VITE_WORKFLOW_SERVICE_URL
ARG VITE_MCP_GATEWAY_SERVICE_URL
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q -O - http://localhost:80/ || exit 1
