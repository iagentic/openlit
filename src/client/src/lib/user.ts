import { compare, genSaltSync, hashSync } from "bcrypt-ts";
import prisma from "./prisma";
import asaw from "@/utils/asaw";
import { getCurrentUser } from "./session";
import { User } from "@/types/user";
import { moveSharedDBConfigToDBUser } from "./db-config";
import getMessage from "@/constants/messages";
import { userService } from "./services";

function exclude<User extends Record<string, unknown>, K extends keyof User>(
	user: User,
	keys: K[] = ["password"] as K[]
): Omit<User, K> {
	return Object.fromEntries(
		Object.entries(user).filter(([key]) =>
			typeof keys.includes === "function" ? !keys.includes(key as K) : true
		)
	) as Omit<User, K>;
}

// This function is kept for backward compatibility
// It will be deprecated in favor of userService.getUserByEmail
export const getUserByEmail = async ({
	email,
	selectPassword = false,
}: {
	email?: string;
	selectPassword?: boolean;
}) => {
	if (!email) throw new Error("No email Provided");
	
	try {
		// Use the API service to get the user
		const user = await userService.getCurrentUser();
		return exclude(user, selectPassword ? [] : undefined);
	} catch (error) {
		throw new Error("No user with this email exists");
	}
};

// This function is kept for backward compatibility
// It will be deprecated in favor of userService.getUserById
export const getUserById = async ({
	id,
	selectPassword = false,
}: {
	id?: string;
	selectPassword?: boolean;
}) => {
	if (!id) return null;
	
	try {
		// Use the API service to get the user
		const user = await userService.getCurrentUser();
		return exclude(user, selectPassword ? [] : undefined);
	} catch (error) {
		return null;
	}
};

// This function is kept for backward compatibility
// It will be deprecated in favor of userService.createUser
export const createNewUser = async (
	{
		email,
		password,
	}: {
		email: string;
		password: string;
	},
	options?: { selectPassword?: boolean }
) => {
	try {
		// Use the API service to create a user
		const user = await userService.createUser(email, password);
		return exclude(user, options?.selectPassword ? [] : undefined);
	} catch (error) {
		throw new Error("Cannot create a user!");
	}
};

// This function is kept for backward compatibility
// It will be deprecated in favor of userService.updateUser
export const updateUser = async ({
	data,
	where,
}: {
	data: any;
	where: any;
}) => {
	if (!where || !Object.keys(where).length)
		throw new Error("No where clause defined");
	
	try {
		// Use the API service to update the user
		const user = await userService.updateUserProfile(data);
		return user;
	} catch (error) {
		throw new Error("Cannot update user");
	}
};

// This function is kept for backward compatibility
// It will be deprecated in favor of userService.updateUserProfile
export const updateUserProfile = async ({
	currentPassword,
	newPassword,
	name,
}: {
	currentPassword?: string;
	newPassword?: string;
	name?: string;
}) => {
	const user = await getCurrentUser({ selectPassword: true });

	if (!user) throw new Error(getMessage().UNAUTHORIZED_USER);

	const updatedUserObject: Partial<User> = {};

	if (newPassword) {
		if (!currentPassword)
			throw new Error("Provide current password to update it to new one!");
		const passwordsMatch = await doesPasswordMatches(
			currentPassword,
			user.password || ""
		);
		if (!passwordsMatch) throw new Error("Wrong current password!");
		updatedUserObject.password = getHashedPassword(newPassword);
	}

	if (name) {
		updatedUserObject.name = name;
	}

	if (Object.keys(updatedUserObject).length === 0)
		throw new Error("Nothing to update!");

	return updateUser({
		data: updatedUserObject,
		where: { id: user.id },
	});
};

const getHashedPassword = (password: string): string => {
	const salt = genSaltSync(10);
	const hash = hashSync(password, salt);
	return hash;
};

export const doesPasswordMatches = async (
	password: string,
	userPassword: string
): Promise<boolean> => {
	return await compare(password, userPassword);
};
