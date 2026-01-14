import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  rewrites: async () => {
    return [
      {
        source: "/api/py/:path*",
        destination: "http://localhost:8000/api/py/:path*",
      },
    ];
  }
};

export default nextConfig;
