import NextAuth, { AuthOptions, User as NextAuthUser } from "next-auth";
// import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import { PrismaAdapter } from "@next-auth/prisma-adapter";
import { PrismaClient } from "@prisma/client";
import asaw from "@/utils/asaw";
import { userService } from "@/lib/services";

// Extend the User type to include accessToken
interface User extends NextAuthUser {
	accessToken?: string;
}

const prisma = new PrismaClient();

export const authOptions = {
	adapter: PrismaAdapter(prisma),
	callbacks: {
		async jwt({ token, account, user, ...rest }) {
			// Persist the OAuth access_token and or the user id to the token right after signin
			if (account) {
				token.accessToken = account.access_token;
			}

			if (user?.id) {
				token.id = user.id;
			}

			// Add the access token from our credentials provider
			if (user && 'accessToken' in user) {
				token.accessToken = (user as User).accessToken;
			}

			return token;
		},
		signIn: async ({ user, account, profile }) => {
			if (!user.email) {
				return false;
			}
			if (account?.provider === "google") {
				// This would need to be updated to use the API service
				// For now, we'll keep using Prisma directly
				const [, existingUser] = await asaw(
					prisma.user.findUnique({
						where: { email: user.email }
					})
				);
				// if the user already exists via email,
				// update the user with their name and image from Google
				if (existingUser && !existingUser.name) {
					await asaw(
						prisma.user.update({
							where: { email: user.email },
							data: {
								name: profile?.name,
								// @ts-ignore - this is a bug in the types, `picture` is a valid on the `Profile` type
								image: profile?.picture,
							},
						})
					);
				}
			}

			return true;
		},
		async session({ session, token }: { session: any; token: any }) {
			try {
				// Ensure we have a user object
				if (!session.user) {
					session.user = {};
				}
				
				// Add the user ID to the session
				session.user.id = token.id;
				
				// Add the access token to the session
				session.accessToken = token.accessToken;
				
				// Log for debugging
				console.log("Session updated with token data:", {
					userId: token.id,
					hasAccessToken: !!token.accessToken
				});
			} catch (e) {
				console.error("Error in session callback:", e);
			}
			return session;
		},
	},
	providers: [
		// GoogleProvider({
		// 	clientId: process.env.GOOGLE_CLIENT_ID || "",
		// 	clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
		// }),
		CredentialsProvider({
			id: "login",
			name: "Credentials Login",
			credentials: {
				email: {
					label: "Email",
					type: "email",
					placeholder: "openlit@openlit.io",
				},
				password: { label: "Password", type: "password" },
			},
			async authorize(credentials) {
				if (!credentials) return null;
				
				try {
					// Use the API service to login
					const { access_token } = await userService.login(credentials.email, credentials.password);
					
					// Return a user object that NextAuth can use
					return {
						id: credentials.email,
						email: credentials.email,
						accessToken: access_token
					};
				} catch (error) {
					console.error("Login error:", error);
					return null;
				}
			},
		}),
		CredentialsProvider({
			id: "register",
			name: "Credentials Register",
			credentials: {
				email: {
					label: "Email",
					type: "email",
					placeholder: "openlit@openlit.io",
				},
				password: { label: "Password", type: "password" },
			},
			async authorize(credentials) {
				if (!credentials?.email || !credentials?.password) return null;
				
				try {
					// Use the API service to create a user
					const user = await userService.createUser(credentials.email, credentials.password);
					return user;
				} catch (error) {
					console.error("Registration error:", error);
					throw new Error(error instanceof Error ? error.message : "Registration failed");
				}
			},
		}),
	],
	pages: {
		signIn: "/login",
		newUser: "/register",
	},
	session: { 
		strategy: "jwt",
		maxAge: 30 * 24 * 60 * 60, // 30 days
	},
} as AuthOptions;

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
