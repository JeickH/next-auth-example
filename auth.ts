import NextAuth, { type NextAuthOptions, type Session } from "next-auth"
import Credentials from "next-auth/providers/credentials"
import { getServerSession } from "next-auth/next"

// Extend the session type to include the user ID
declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      name?: string | null;
      email?: string | null;
      image?: string | null;
    };
  }
}

export const authOptions: NextAuthOptions = {
  providers: [
    Credentials({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        // TODO: Replace with actual API call to your FastAPI backend
        if (credentials?.email === "test@example.com" && credentials?.password === "password") {
          return {
            id: "1",
            name: "Test User",
            email: "test@example.com",
          }
        }
        return null
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id
      }
      return token
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string
      }
      return session
    },
  },
  pages: {
    signIn: "/auth/signin",
  },
  secret: process.env.NEXTAUTH_SECRET,
  debug: process.env.NODE_ENV === "development",
  session: {
    strategy: "jwt" as const,
  },
}

// Create the NextAuth handler
const handler = NextAuth(authOptions)

// Export individual methods
export const GET = handler.GET
export const POST = handler.POST
export const signIn = handler.signIn
export const signOut = handler.signOut

// Export the auth function for server components
export const auth = () => {
  return getServerSession(authOptions)
}

// Export the handler as default for API routes
export default handler
