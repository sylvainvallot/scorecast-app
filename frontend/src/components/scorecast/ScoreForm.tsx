"use client";

import { Team } from "@/lib/types/Team";
import { Button } from "@/components/ui/button";
import {
    Field,
    FieldDescription,
    FieldGroup,
    FieldLabel,
    FieldLegend,
    FieldSet,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { useEffect, useMemo, useState } from "react";
import ResultBadge from "./ResultBadge";
import Loading from "./Loading";
import SubTeamSelector from "./SubTeamSelector";
import ScoreBoardPreviewAPI from "./ScoreBoardPreviewAPI";
import TeamType from "./TeamType";
import PeriodSelector from "./PeriodSelector";

export default function ScoreForm() {
    const [myTeam, setMyTeam] = useState<Team>();

    const [teamList, setTeamList] = useState<Team[]>([]);

    const [homeScore, setHomeScore] = useState<number | null>(null);
    const [awayScore, setAwayScore] = useState<number | null>(null);
    const [awayTeam, setAwayTeam] = useState<Team["id"] | null>(null);

    const [homeSubTeam, setHomeSubTeam] = useState<string | undefined>(
        undefined,
    );
    const [awaySubTeam, setAwaySubTeam] = useState<string | undefined>(
        undefined,
    );

    const [teamType, setTeamType] = useState<string>("mixed");

    const [isGenerating, setIsGenerating] = useState<boolean>(false);

    const [period, setPeriod] = useState<string>("full_time");

    const ScoreBoardPayload = {
        homeTeam: myTeam ? myTeam.id : "",
        awayTeam: awayTeam ? awayTeam : "",
        homeScore: homeScore !== null ? homeScore : 0,
        awayScore: awayScore !== null ? awayScore : 0,
        homeSubTeam: homeSubTeam,
        awaySubTeam: awaySubTeam,
        teamType: teamType,
        period: period,
    };

    const result = useMemo<"win" | "loss" | "draw" | null>(() => {
        if (homeScore === null || awayScore === null) return null;
        if (homeScore > awayScore) return "win";
        if (homeScore < awayScore) return "loss";
        return "draw";
    }, [homeScore, awayScore]);

    useEffect(() => {
        fetch("/api/py/teams/my-team")
            .then((res) => res.json())
            .then((data) => {
                setMyTeam(data);
            })
            .catch(console.error);
    }, []);

    useEffect(() => {
        fetch("/api/py/teams/list")
            .then((res) => res.json())
            .then((data) => {
                setTeamList(data);
            })
            .catch(console.error);
    }, []);

    async function generateScoreCast(e: React.FormEvent) {
        e.preventDefault();
        if (!myTeam || awayScore === null || homeScore === null || !awayTeam) {
            alert("Please fill in all required fields.");
            return;
        }
        setIsGenerating(true);

        const scoreCastPayload = {
            "home_team": myTeam.id,
            "away_team": awayTeam,
            "home_score": homeScore,
            "away_score": awayScore,
            "home_subteam": homeSubTeam,
            "away_subteam": awaySubTeam,
            "team_type": teamType,
            "period": period,
        };

        if (homeSubTeam === "principal") {
            scoreCastPayload.home_subteam = undefined;
            scoreCastPayload.team_type = "mixed";
        }
        if (awaySubTeam === "principal") {
            scoreCastPayload.away_subteam = undefined;
        }

        try {
            const response = await fetch("/api/py/scorecast/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(scoreCastPayload),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const blob = await response.blob();

            const disposition = response.headers.get("Content-Disposition");

            let filename = `scorecast_${Date.now()}.mp4`;
            if (disposition) {
                const match = disposition.match(/filename="(.+)"/);
                if (match && match[1]) {
                    filename = match[1];
                }
            }
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            setIsGenerating(false);
        } catch (error) {
            console.error("Error generating ScoreCast:", error);
            setIsGenerating(false);
        }
    }

    return (
        <div className="w-full my-8 border border-white rounded-2xl bg-white backdrop-blur-lg shadow-lg">
            {isGenerating && <Loading />}
            <form className="p-8">
                <FieldGroup>
                    <FieldSet>
                        <FieldLegend className="flex flex-row w-full gap-4 items-center justify-between">
                            Match Score
                            {result && <ResultBadge result={result} />}
                        </FieldLegend>
                        <FieldGroup className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                            <Field>
                                <FieldLabel htmlFor="home-score">
                                    Home
                                </FieldLabel>
                                <Input
                                    type="number"
                                    id="home-score"
                                    min={0}
                                    max={999}
                                    placeholder="0"
                                    value={homeScore ?? ""}
                                    onChange={(e) => {
                                        const value = e.target.value;
                                        if (value.length <= 3) {
                                            setHomeScore(
                                                value === ""
                                                    ? null
                                                    : Number(value),
                                            );
                                        }
                                    }}
                                />
                                <FieldDescription>
                                    Enter the {myTeam?.name} score
                                </FieldDescription>
                            </Field>

                            <Field>
                                <FieldLabel htmlFor="away-score">
                                    Away
                                </FieldLabel>
                                <Input
                                    type="number"
                                    id="away-score"
                                    min={0}
                                    max={999}
                                    placeholder="0"
                                    value={awayScore ?? ""}
                                    onChange={(e) => {
                                        const value = e.target.value;
                                        if (value.length <= 3) {
                                            setAwayScore(
                                                value === ""
                                                    ? null
                                                    : Number(value),
                                            );
                                        }
                                    }}
                                />
                                <FieldDescription>
                                    Enter the away team score
                                </FieldDescription>
                            </Field>
                            <PeriodSelector onSelect={setPeriod} className="col-span-2 sm:col-span-1" />
                        </FieldGroup>
                    </FieldSet>

                    <FieldSet className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <SubTeamSelector
                            teamId={myTeam ? myTeam.id : null}
                            teamList={teamList}
                            onSelect={setHomeSubTeam}
                            placeholder={`${myTeam?.name} sub-team`}
                            title={`${myTeam?.name} sub-team`}
                        />
                        {
                            homeSubTeam === "principal" ||
                            homeSubTeam == undefined ? (
                                <TeamType onSelect={setTeamType} />
                            ) : null
                        }
                    </FieldSet>
                    <FieldSet>
                        <FieldLegend>Select Away Team</FieldLegend>
                        <FieldGroup className="">
                            <Field>
                                <Select
                                    defaultValue=""
                                    onValueChange={(value) => {
                                        setAwayTeam(value);
                                        setAwaySubTeam(undefined);
                                    }}
                                >
                                    <SelectTrigger id="away-team-select">
                                        <SelectValue placeholder="away team" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {teamList.map((team) => (
                                            <SelectItem
                                                key={team.id}
                                                value={team.id}
                                            >
                                                {team.name} - {team.city}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </Field>

                            {/* Select Away Sub Team (Optional) */}
                            {awayTeam && (
                                <SubTeamSelector
                                    title={`Select ${awayTeam} sub-team`}
                                    placeholder={`${awayTeam} sub-team`}
                                    teamId={awayTeam}
                                    teamList={teamList}
                                    onSelect={setAwaySubTeam}
                                />
                            )}
                        </FieldGroup>
                    </FieldSet>
                    <ScoreBoardPreviewAPI payload={ScoreBoardPayload} />
                    {/* <ScorecastPreview data={preview} /> */}
                    <Field orientation="horizontal">
                        <Button
                            onClick={(e) => generateScoreCast(e)}
                            disabled={isGenerating}
                        >
                            Generate ScoreCast
                        </Button>
                        <Button
                            variant="outline"
                            type="button"
                            onClick={() => {
                                setHomeScore(null);
                                setAwayScore(null);
                                setHomeSubTeam(undefined);
                                setAwaySubTeam(undefined);
                            }}
                        >
                            Clear
                        </Button>
                    </Field>
                </FieldGroup>
            </form>
        </div>
    );
}
