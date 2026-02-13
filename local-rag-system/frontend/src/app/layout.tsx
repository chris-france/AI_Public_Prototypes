import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Local RAG System",
  description: "Retrieval Augmented Generation with Llama 3",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
