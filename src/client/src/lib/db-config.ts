import asaw from "@/utils/asaw";
import prisma from "./prisma";
import { getCurrentUser } from "./session";
import { DatabaseConfig, DatabaseConfigInvitedUser } from "@prisma/client";
import migrations from "@/clickhouse/migrations";
import getMessage from "@/constants/messages";
import { throwIfError } from "@/utils/error";
import { consoleLog } from "@/utils/log";
import { serverApi } from "./server-api";

// This function is kept for backward compatibility
// It will be deprecated in favor of dbConfigService.getDatabaseConfigs
export const getDBConfigByUser = async (currentOnly?: boolean) => {
	try {
		const user = await getCurrentUser();

		if (!user) {
			console.warn("Unauthorized user in getDBConfigByUser");
			throw new Error(getMessage().UNAUTHORIZED_USER);
		}

		try {
			// Use the server API to get database configs
			const dbConfigs = await serverApi.get('/database-configs/');
			
			if (!dbConfigs) {
				console.warn("No database configs returned from API");
				return currentOnly ? null : [];
			}
			
			if (currentOnly) {
				// For now, we'll just return the first config
				// In a real implementation, we would need to track the current config
				return dbConfigs.length > 0 ? dbConfigs[0] : null;
			}
			
			return dbConfigs;
		} catch (error) {
			console.error("Error getting database configs:", error);
			throw new Error("Failed to get database configs");
		}
	} catch (error) {
		console.error("Error in getDBConfigByUser:", error);
		throw error;
	}
};

// This function is kept for backward compatibility
// It will be deprecated in favor of dbConfigService.getDatabaseConfigById
export const getDBConfigById = async ({ id }: { id: string }) => {
	try {
		const user = await getCurrentUser();

		if (!user) {
			console.warn("Unauthorized user in getDBConfigById");
			throw new Error(getMessage().UNAUTHORIZED_USER);
		}

		try {
			// Use the server API to get database configs
			const dbConfigs = await serverApi.get('/database-configs/');
			
			if (!dbConfigs) {
				console.warn("No database configs returned from API");
				throw new Error("Database config not found");
			}
			
			// Find the config with the matching ID
			const dbConfig = dbConfigs.find((config: DatabaseConfig) => config.id === id);
			
			if (!dbConfig) {
				console.warn(`Database config with ID ${id} not found`);
				throw new Error("Database config not found");
			}
			
			return dbConfig;
		} catch (error) {
			console.error("Error getting database config:", error);
			throw new Error("Failed to get database config");
		}
	} catch (error) {
		console.error("Error in getDBConfigById:", error);
		throw error;
	}
};

// This function is kept for backward compatibility
// It will be deprecated in favor of dbConfigService.createDatabaseConfig
export const upsertDBConfig = async (
	dbConfig: Partial<DatabaseConfig>,
	id?: string
) => {
	try {
		const user = await getCurrentUser();

		if (!user) {
			console.warn("Unauthorized user in upsertDBConfig");
			throw new Error(getMessage().UNAUTHORIZED_USER);
		}

		try {
			// Use the server API to create a database config
			const newDbConfig = await serverApi.post('/database-configs/', {
				name: dbConfig.name || "Default Config",
				environment: dbConfig.environment || "production",
				username: dbConfig.username || "admin",
				password: dbConfig.password,
				host: dbConfig.host || "127.0.0.1",
				port: dbConfig.port || "8123",
				database: dbConfig.database || "openlit",
				query: dbConfig.query,
			});
			
			if (!newDbConfig) {
				console.warn("No database config returned from API after creation");
				throw new Error("Failed to create database config");
			}
			
			return newDbConfig;
		} catch (error) {
			console.error("Error creating database config:", error);
			throw new Error("Failed to create database config");
		}
	} catch (error) {
		console.error("Error in upsertDBConfig:", error);
		throw error;
	}
};

// This function is kept for backward compatibility
// It will be deprecated in favor of dbConfigService.deleteDatabaseConfig
export async function deleteDBConfig(id: string) {
	try {
		const user = await getCurrentUser();

		if (!user) {
			console.warn("Unauthorized user in deleteDBConfig");
			throw new Error(getMessage().UNAUTHORIZED_USER);
		}

		try {
			// Use the server API to delete a database config
			await serverApi.delete(`/database-configs/${id}/`);
		} catch (error) {
			console.error("Error deleting database config:", error);
			throw new Error("Failed to delete database config");
		}
	} catch (error) {
		console.error("Error in deleteDBConfig:", error);
		throw error;
	}
}

// This function is kept for backward compatibility
// It will be deprecated in favor of dbConfigService.setCurrentDatabaseConfig
export async function setCurrentDBConfig(id: string) {
	const user = await getCurrentUser();

	if (!user) throw new Error(getMessage().UNAUTHORIZED_USER);

	try {
		// For now, we'll just log that this function was called
		// In a real implementation, we would need to add a setCurrent endpoint to the API
		console.log(`Setting current database config to ID: ${id}`);
		
		return true;
	} catch (error) {
		console.error("Error setting current database config:", error);
		throw new Error("Failed to set current database config");
	}
}

// This function is kept for backward compatibility
// It will be deprecated in favor of dbConfigService.shareDatabaseConfig
export async function shareDBConfig({
	shareArray,
	id,
}: {
	id: string;
	shareArray: {
		email: string;
		permissions?: {
			canDelete: boolean;
			canEdit: boolean;
			canShare: boolean;
		};
	}[];
}) {
	const user = await getCurrentUser();

	if (!user) throw new Error(getMessage().UNAUTHORIZED_USER);

	try {
		// For now, we'll just log that this function was called
		// In a real implementation, we would need to add a share endpoint to the API
		console.log(`Sharing database config with ID: ${id} with users:`, shareArray);
		
		return true;
	} catch (error) {
		console.error("Error sharing database config:", error);
		throw new Error("Failed to share database config");
	}
}

// This function is kept for backward compatibility
// It will be deprecated in favor of dbConfigService.moveSharedDBConfigToDBUser
export async function moveSharedDBConfigToDBUser(
	email: string,
	userId: string
) {
	try {
		// For now, we'll just log that this function was called
		// In a real implementation, we would need to add a moveShared endpoint to the API
		console.log(`Moving shared database config for email: ${email} to user ID: ${userId}`);
		
		return true;
	} catch (error) {
		console.error("Error moving shared database config:", error);
		throw new Error("Failed to move shared database config");
	}
}

// These functions are kept for backward compatibility
// They will be deprecated in favor of dbConfigService functions
async function addDatabaseConfigUserEntry(
	userId: string,
	databaseConfigId: string,
	permissions: {
		canDelete: boolean;
		canEdit: boolean;
		canShare: boolean;
	}
) {
	// Implementation would be updated to use the API service
	return true;
}

async function checkPermissionForDbAction(
	userId: string,
	databaseConfigId: string,
	actionType: "DELETE" | "SHARE" | "EDIT"
) {
	// Implementation would be updated to use the API service
	return true;
}
