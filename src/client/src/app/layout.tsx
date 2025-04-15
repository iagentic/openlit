import type { Metadata } from "next";
import { cookies } from "next/headers";
import { Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
	title: "iAgentic | Enterprice Agentic Platform",
	description:
		"Unified Platform  for Developing, Running tracking and analyzing usage patterns of Agentic Framework.",
};

export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	const cookieStore = cookies();
	const theme = cookieStore.get("theme");

	return (
		<html lang="en" className={`scroll-smooth ${theme?.value || ""}`}>
			<body className={`${inter.className} bg-white dark:bg-black`}>
				{children}
				<Toaster position="bottom-right" />
			</body>
		</html>
	);
}
