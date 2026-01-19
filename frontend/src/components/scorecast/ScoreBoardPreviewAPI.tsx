import { useEffect, useState } from "react";
import { Scoreboard } from "@/lib/types/Scoreboard";
import Image from "next/image";
import { Badge } from "../ui/badge";
import { RadioIcon } from "lucide-react";

export default function ScoreBoardPreviewAPI({ payload }: { payload: Scoreboard }) {
    const [imageUrl, setImageUrl] = useState<string | null>(null);

    const isPayloadComplete = payload.homeScore !== null &&
        payload.awayScore !== null &&
        payload.homeTeam &&
        payload.awayTeam;

    useEffect(() => {
        if (!isPayloadComplete) return;

        const controller = new AbortController();

        const scoreBoardPayload = {
            home_team: payload.homeTeam,
            away_team: payload.awayTeam,
            home_score: payload.homeScore,
            away_score: payload.awayScore,
            home_subteam: payload.homeSubTeam,
            away_subteam: payload.awaySubTeam,
            period: payload.period,
        };

        if (payload.homeSubTeam === "principal") {
            scoreBoardPayload.home_subteam = undefined;
        }
        if (payload.awaySubTeam === "principal") {
            scoreBoardPayload.away_subteam = undefined;
        }
        fetch("/api/py/scorecast/scoreboard", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(scoreBoardPayload),
            signal: controller.signal,
        })
            .then((res) => {
                if (!res.ok) throw new Error("Failed to fetch image");
                return res.blob();
            })
            .then((blob) => {
                const url = URL.createObjectURL(blob);
                setImageUrl((prev) => {
                    if (prev) URL.revokeObjectURL(prev);
                    return url;
                });
            })
            .catch((err) => {
                if (err.name !== "AbortError") console.error(err);
            });

        return () => controller.abort();
    }, [
        isPayloadComplete,
        payload.awayScore,
        payload.awaySubTeam,
        payload.awayTeam,
        payload.homeScore,
        payload.homeSubTeam,
        payload.homeTeam,
        payload.period,
    ]);

    return (
        <div className="w-full rounded-xl px-4 py-3 backdrop-blur-2xl shadow-lg border bg-[#eeeeee] sm:min-h-55">
            <Badge
                variant="default"
                className="mb-4"
            >
                <RadioIcon />
                LIVE
            </Badge>

            {imageUrl && (
                <Image
                    src={imageUrl}
                    alt="Scoreboard preview"
                    className="max-w-full mx-auto w-auto h-auto"
                    width={400}
                    height={200}
                />
            )}
        </div>
    );
}
