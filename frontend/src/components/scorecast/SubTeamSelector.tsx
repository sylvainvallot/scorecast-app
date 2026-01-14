import { Team } from "@/lib/types/Team";
import { Field, FieldLabel } from "@/components/ui/field";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

export default function SubTeamSelector({
    teamId,
    teamList,
    title,
    placeholder,
    onSelect,
}: {
    teamId: string | null;
    teamList: Team[];
    title?: string;
    placeholder: string;
    onSelect: (subTeam: string) => void;
}) {
    const subTeams = teamList.find((t) => t.id === teamId)?.subteams || [];

    if (subTeams.length === 0) {
        return null;
    }

    return (
        <Field>
            {title && <FieldLabel htmlFor="subteam">{title}</FieldLabel>}
            <Select
                defaultValue="principal"
                onValueChange={(value) => onSelect(value)}
            >
                <SelectTrigger id="subteam">
                    <SelectValue
                        placeholder={placeholder
                            ? placeholder
                            : "Select sub-team"}
                    />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="principal">Principal</SelectItem>
                    {subTeams.map((subTeam: string) => (
                        <SelectItem key={subTeam} value={subTeam}>
                            {subTeam}
                        </SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </Field>
    );
}
