#!/bin/bash
# Generate TypeScript types from FastAPI OpenAPI spec

echo "Downloading OpenAPI Spec..."
# Wait for API to boot in CI
sleep 5

curl -s http://localhost:8000/openapi.json > /tmp/openapi.json

echo "Generating TypeScript interfaces..."
pnpm dlx openapi-typescript /tmp/openapi.json -o ../../packages/api-types/index.ts

echo "Types successfully generated in packages/api-types/index.ts"
