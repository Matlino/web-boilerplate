import Image from "next/image";
import { headers } from "next/headers";

async function getBaseUrl() {
  const h = await headers();
  const host = h.get("host") ?? "localhost:3000";
  const isLocalhost = host.includes("localhost") || host.startsWith("127.0.0.1");
  const protocol = isLocalhost ? "http" : "https";
  return `${protocol}://${host}`;
}

async function getStatus() {
  try {
    const baseUrl = await getBaseUrl();
    const res = await fetch(`${baseUrl}/api/`, { cache: "no-store" });
    if (!res.ok) {
      return { status: "error" } as const;
    }
    return (await res.json()) as { status: string };
  } catch {
    return { status: "offline" } as const;
  }
}

export default async function Home() {
  const data = await getStatus();
  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />
        <div className="font-mono text-sm/6">
          Backend status: <span className="font-semibold">{data.status}</span>
        </div>
      </main>
    </div>
  );
}
