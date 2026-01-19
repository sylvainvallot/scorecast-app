import ScoreForm from "@/components/scorecast/ScoreForm";
import StatusDB from "@/components/StatusDB";
import Welcome from "@/components/Welcome";

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center p-8 sm:p-16">
      <main className="max-w-3xl w-full space-y-8">
        <Welcome />
        <div className="flex justify-end">
          <StatusDB />
        </div>
        <div className="my-8">
          <ScoreForm />
        </div>
      </main>
    </div>
  );
}
