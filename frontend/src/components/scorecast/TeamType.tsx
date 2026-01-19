import { Field, FieldLabel } from "@/components/ui/field";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const TEAM_TYPES = [
    { value: "mixed", label: "Mixed" },
    { value: "men", label: "Men" },
    { value: "women", label: "Women" },
];

export default function TeamType({
    onSelect,
}: {
    onSelect?: (teamType: string) => void;
}) {
    return (
        <Field>
            <FieldLabel htmlFor="subteam">Team Type</FieldLabel>
            <Select
                defaultValue="mixed"
                onValueChange={(value) => onSelect && onSelect(value)}
                >
                    <SelectTrigger id="team-type">
                        <SelectValue
                            placeholder="Select team type"
                        />
                    </SelectTrigger>
                    <SelectContent>
                        {TEAM_TYPES.map((type) => (
                            <SelectItem key={type.value} value={type.value}>
                                {type.label}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
        </Field>
    )
}