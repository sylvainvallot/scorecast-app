"use client";
import { useState } from "react";
import { Badge } from "./ui/badge";

function PingDot(colorClass: string) {
    return (
        <span className="relative flex size-2">
            <span
                className={`absolute inline-flex h-full w-full animate-ping rounded-full ${colorClass} opacity-75`}
            >
            </span>
            <span
                className={`relative inline-flex size-2 rounded-full ${colorClass}`}
            >
            </span>
        </span>
    );
}

export default function StatusDB() {
    const [status, setStatus] = useState<string>("unknown");

    fetch("/api/py/utils/status")
        .then((response) => response.json())
        .then((data) => setStatus(data.status))
        .catch(() => setStatus("error"));

    let statusClass = "bg-red-500";

    if (status === "ok") {
        statusClass = "bg-green-500";
    }

    return (
        <Badge variant="outline" className="flex items-center space-x-4 py-2 px-4">
            {PingDot(statusClass)}
            <span>
                {status === "ok" ? "API Online" : "API Offline"}
            </span>
        </Badge>
    );
}
