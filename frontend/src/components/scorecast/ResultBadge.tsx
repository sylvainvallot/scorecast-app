import { Badge } from "@/components/ui/badge";

type Result = "win" | "draw" | "loss";

const RESULT_CONFIG: Record<
    Result,
    {
        label: string;
        type: "default" | "secondary" | "destructive";
        badge?: string[];
    }
> = {
    win: {
        label: "WIN",
        type: "default",
        badge: [
            "Momentum is yours!",
            "Great job!",
            "Keep it up!",
            "Fantastic result!",
            "Strong performance!",
        ],
    },
    draw: {
        label: "DRAW",
        type: "secondary",
        badge: [
            "So close!",
            "A hard-fought battle!",
            "Evenly matched!",
            "Well played by both sides!",
            "A balanced outcome!",
        ],
    },
    loss: {
        label: "LOSS",
        type: "destructive",
        badge: [
            "Tough luck!",
            "Better luck next time!",
            "Keep your head up!",
            "Learn and improve!",
            "Stay motivated!",
        ],
    },
};

export default function ResultBadge({ result }: { result: Result }) {
    const { label, type } = RESULT_CONFIG[result];

    return <Badge variant={type}>{label}</Badge>;
}