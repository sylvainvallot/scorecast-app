export default function Loading() {
    return (
        <div
            className="fixed inset-0 z-9999 flex items-center justify-center rounded-2xl backdrop-blur-lg border"
            style={{
                backgroundColor: "rgba(0, 0, 0, 0.05)",
            }}
        >
            <div className="flex flex-col items-center">
                {/* Spinning circle */}
                <div
                    className="mb-4"
                    style={{
                        width: "64px", // w-16
                        height: "64px", // h-16
                        border: "4px solid white", // border-4 + border-white
                        borderTop: "4px solid #ec4899", // border-t-pink-600
                        borderRadius: "50%", // rounded-full
                        animation: "spin 1s linear infinite", // animate-spin
                    }}
                >
                    <style>
                        {`
              @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
              }
            `}
                    </style>
                </div>
                {/* loading text */}
                <span className="text-black font-semibold text-xl">
                    Generating ScoreCast...
                </span>
            </div>
        </div>
    );
}
