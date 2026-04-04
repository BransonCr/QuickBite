import { formatEarnedDate } from "../services/badgeService";

export default function BadgeCard({ badge }) {
  const {
    name,
    description,
    icon,
    condition,
    unlocked,
    current,
    total,
    earnedAt,
  } = badge;
  const pct =
    total > 0 ? Math.min(100, Math.round((current / total) * 100)) : 0;
  const dateLabel = formatEarnedDate(earnedAt);

  return (
    <div
      className={`relative rounded-xl border-2 p-5 flex flex-col transition-shadow hover:shadow-md ${
        unlocked ? "border-green-400 bg-green-50" : "border-gray-200 bg-white"
      }`}
    >
      {/* Status indicator */}
      <div className="absolute top-3 right-3">
        {unlocked ? (
          <span className="flex items-center justify-center w-6 h-6 rounded-full bg-green-500 text-white text-xs font-bold">
            ✓
          </span>
        ) : (
          <span className="text-gray-300 text-lg leading-none">🔒</span>
        )}
      </div>

      {/* Icon */}
      <div
        className={`text-4xl mb-3 select-none ${unlocked ? "" : "grayscale opacity-40"}`}
      >
        {icon}
      </div>

      {/* Name */}
      <h3
        className={`font-bold text-base mb-1 ${unlocked ? "text-gray-900" : "text-gray-500"}`}
      >
        {name}
      </h3>

      {/* Description */}
      <p
        className={`text-sm mb-2 flex-1 ${unlocked ? "text-gray-700" : "text-gray-400"}`}
      >
        {description}
      </p>

      {/* Condition */}
      <p
        className={`text-xs font-medium mb-3 ${unlocked ? "text-green-600" : "text-gray-400"}`}
      >
        {condition}
      </p>

      {/* Footer: earned date or progress */}
      {unlocked ? (
        dateLabel && (
          <p className="text-xs text-green-500">Earned {dateLabel}</p>
        )
      ) : (
        <div>
          <div className="flex justify-between text-xs text-gray-400 mb-1">
            <span>
              {badge.requirement?.type === "total_spent"
                ? `$${current.toFixed(2)} / $${total}`
                : `${current} / ${total}`}
            </span>
            <span>{pct}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-orange-400 h-2 rounded-full transition-all duration-500"
              style={{ width: `${pct}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
