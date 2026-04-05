export const BADGES = [
  {
    id: "first_bite",
    name: "First Bite",
    description: "Your first step into the QuickBite world",
    icon: "🍔",
    condition: "Complete 1 order",
    requirement: { type: "order_count", threshold: 1 },
  },
  {
    id: "regular",
    name: "Regular",
    description: "You keep coming back for more",
    icon: "⭐",
    condition: "Complete 5 orders",
    requirement: { type: "order_count", threshold: 5 },
  },
  {
    id: "foodie",
    name: "Foodie",
    description: "A true food enthusiast",
    icon: "🍽️",
    condition: "Complete 10 orders",
    requirement: { type: "order_count", threshold: 10 },
  },
  {
    id: "power_user",
    name: "Power User",
    description: "You really love QuickBite",
    icon: "🚀",
    condition: "Complete 25 orders",
    requirement: { type: "order_count", threshold: 25 },
  },
  {
    id: "century",
    name: "Century Club",
    description: "An elite QuickBite member",
    icon: "💯",
    condition: "Complete 100 orders",
    requirement: { type: "order_count", threshold: 100 },
  },
  {
    id: "explorer",
    name: "Explorer",
    description: "Variety is the spice of life",
    icon: "🗺️",
    condition: "Order from 3 different restaurants",
    requirement: { type: "restaurant_count", threshold: 3 },
  },
  {
    id: "adventurer",
    name: "Adventurer",
    description: "Always trying something new",
    icon: "🧭",
    condition: "Order from 5 different restaurants",
    requirement: { type: "restaurant_count", threshold: 5 },
  },
  {
    id: "big_spender",
    name: "Big Spender",
    description: "Living the good life",
    icon: "💰",
    condition: "Spend over $100 total",
    requirement: { type: "total_spent", threshold: 100 },
  },
  {
    id: "high_roller",
    name: "High Roller",
    description: "No expense spared",
    icon: "💎",
    condition: "Spend over $500 total",
    requirement: { type: "total_spent", threshold: 500 },
  },
  {
    id: "tipper",
    name: "Generous Tipper",
    description: "You know tips make a difference",
    icon: "🤝",
    condition: "Leave a tip on any order",
    requirement: { type: "has_tip", threshold: 1 },
  },
];

function sortedByDate(orders) {
  return [...orders].sort(
    (a, b) => new Date(a.created_at) - new Date(b.created_at),
  );
}

function computeProgress(orders, badge) {
  const delivered = orders.filter((o) => o.status === "DELIVERED");
  const { type, threshold } = badge.requirement;

  switch (type) {
    case "order_count": {
      const sorted = sortedByDate(delivered);
      const count = sorted.length;
      return {
        current: Math.min(count, threshold),
        total: threshold,
        unlocked: count >= threshold,
        earnedAt: count >= threshold ? sorted[threshold - 1].created_at : null,
      };
    }
    case "restaurant_count": {
      const unique = new Set(delivered.map((o) => o.restaurant_id));
      const count = unique.size;
      const mostRecent = sortedByDate(delivered).at(-1);
      return {
        current: Math.min(count, threshold),
        total: threshold,
        unlocked: count >= threshold,
        earnedAt: count >= threshold ? (mostRecent?.created_at ?? null) : null,
      };
    }
    case "total_spent": {
      const total = delivered.reduce((sum, o) => sum + (o.total ?? 0), 0);
      const mostRecent = sortedByDate(delivered).at(-1);
      return {
        current: Math.min(Math.round(total * 100) / 100, threshold),
        total: threshold,
        unlocked: total >= threshold,
        earnedAt: total >= threshold ? (mostRecent?.created_at ?? null) : null,
      };
    }
    case "has_tip": {
      const tipped = sortedByDate(delivered).filter((o) => (o.tip ?? 0) > 0);
      return {
        current: tipped.length > 0 ? 1 : 0,
        total: 1,
        unlocked: tipped.length > 0,
        earnedAt: tipped.length > 0 ? tipped[0].created_at : null,
      };
    }
    default:
      return { current: 0, total: threshold, unlocked: false, earnedAt: null };
  }
}

export function getAllBadgesWithStatus(orders) {
  return BADGES.map((badge) => ({
    ...badge,
    ...computeProgress(orders, badge),
  }));
}

export function getRecentlyEarnedBadges(orders, limit = 3) {
  return getAllBadgesWithStatus(orders)
    .filter((b) => b.unlocked)
    .sort((a, b) => {
      if (!a.earnedAt && !b.earnedAt) return 0;
      if (!a.earnedAt) return 1;
      if (!b.earnedAt) return -1;
      return new Date(b.earnedAt) - new Date(a.earnedAt);
    })
    .slice(0, limit);
}

export function formatEarnedDate(dateStr) {
  if (!dateStr) return null;
  const d = new Date(dateStr);
  return isNaN(d.getTime())
    ? null
    : d.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
}
