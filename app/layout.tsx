import "./globals.css"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { auth } from "@/auth"
import { SessionProvider } from "@/components/providers/SessionProvider"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Oraculo - Sales Analytics Platform",
  description: "Plataforma de análisis de ventas predictivas",
}

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await auth()

  return (
    <html lang="es">
      <body className={inter.className}>
        <SessionProvider session={session}>
          <div className="flex h-full min-h-screen w-full flex-col">
            {children}
          </div>
        </SessionProvider>
      </body>
    </html>
  )
}
