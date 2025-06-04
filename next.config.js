/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
  },
  experimental: {
    serverComponentsExternalPackages: ['openid-client'],
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
  webpack: (config, { isServer }) => {
    // Exclude problematic packages
    config.resolve.alias = {
      ...config.resolve.alias,
      'oidc-token-hash': false,
      'openid-client': false,
    };
    
    // Handle fallbacks for client-side
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
        dns: false,
        child_process: false,
        module: false,
      };
    }
    
    // Important: return the modified config
    return config;
  },
};

// Disable type checking and linting in development
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer(nextConfig);
