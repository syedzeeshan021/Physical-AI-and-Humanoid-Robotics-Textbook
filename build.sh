#!/bin/bash
set -e

echo "Installing dependencies..."
cd frontend
npm ci

echo "Building Docusaurus site..."
npm run build

echo "Build completed successfully!"