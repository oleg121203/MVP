/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    appDir: true,
    serverComponentsExternalPackages: ['@tensorflow/tfjs'],
  },
  images: {
    domains: ['cdn.jsdelivr.net'],
  },
}

module.exports = nextConfig
