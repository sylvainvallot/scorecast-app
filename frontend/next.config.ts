import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  rewrites: async () => {
    return [
      {
        source: "/api/py/:path*",
        destination: process.env.NODE_ENV === "production"
          ? "http://scorecast-backend:8000/api/py/:path*"
          : "http://localhost:8000/api/py/:path*",
      },
      
    ];
  },
  output: "standalone",
};

export default nextConfig;
