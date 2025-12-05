/// <reference types="vitest" />
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: "/command-line-parser/", // GitHub Pages base path (repository name)
  test: {
    globals: true,
    environment: "happy-dom",
  },
});
