import { getServerSession } from "next-auth/next";
import { authOptions } from "@/app/auth";
import asaw from "@/utils/asaw";
import { serverApi } from "@/lib/server-api";
import { User } from "@/types/user";
import { Session } from "next-auth";

// Extend the Session type to include accessToken and user with id
interface CustomSession extends Session {
	accessToken?: string;
	user?: {
		id?: string;
		name?: string | null;
		email?: string | null;
		image?: string | null;
	};
}

export async function getCurrentUser({
	selectPassword,
}: {
	selectPassword?: boolean;
} = {}): Promise<User | null> {
	try {
		const session = await getServerSession(authOptions) as CustomSession;

		if (!session?.user?.id) {
			console.log("No session or user ID found");
			return null;
		}

		try {
			// Use the server API to get the current user
			const user = await serverApi.get('/users/me/');
			
			if (!user) {
				console.log("No user data returned from API");
				return null;
			}
			
			return user;
		} catch (error) {
			console.error("Error getting current user:", error);
			return null;
		}
	} catch (error) {
		console.error("Error getting server session:", error);
		return null;
	}
}
