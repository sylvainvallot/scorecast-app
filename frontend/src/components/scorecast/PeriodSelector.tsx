import { Field, FieldDescription, FieldLabel } from "@/components/ui/field";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "../ui/select";

const PERIOD_OPTIONS = [
    { value: "full_time", label: "Full Time" },
    { value: "first_half", label: "End of 1st Period" },
    // { value: "second_half", label: "Second Half" },
];

export default function PeriodSelector({
    onSelect,
}: {
    onSelect: (period: string) => void;
}) {
    return (
        <Field>
            <FieldLabel htmlFor="period">
                Period
            </FieldLabel>
            <Select
                defaultValue="full_time"
                onOpenChange={(value) => onSelect(value)}
            >
                <SelectTrigger id="period">
                    <SelectValue placeholder="Select period" />
                </SelectTrigger>
                <SelectContent>
                    {PERIOD_OPTIONS.map((option) => (
                        <SelectItem key={option.value} value={option.value}>
                            {option.label}
                        </SelectItem>
                    ))}
                </SelectContent>
            </Select>
            <FieldDescription>
                Select the period of the match
            </FieldDescription>
        </Field>
    );
}
