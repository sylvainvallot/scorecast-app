import ScoreForm from "@/components/scorecast/ScoreForm";
import Welcome from "@/components/Welcome";

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center p-8 sm:p-16">
      <main className="max-w-3xl w-full space-y-16">
        <Welcome />
        <div className="my-8">
          <ScoreForm />
        </div>
      </main>
    </div>
  );
}
