import { useState, useEffect, useRef, useCallback } from "react";

const STORAGE_KEY = "quickbite_user_id";
const SEGMENTS = [5, 7, 8, 10, 12, 15, 17, 20];
const COLORS = [
  "#e07b39","#f4a261","#2a9d8f","#e9c46a",
  "#264653","#e76f51","#a8dadc","#457b9d",
];
const N = SEGMENTS.length;
const ARC = (2 * Math.PI) / N;

async function apiFetch(path, options = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return res.json();
}

export default function SpinWheelPage() {
  const canvasRef = useRef(null);
  const angleRef = useRef(0);
  const animFrameRef = useRef(null);

  const [userId, setUserId] = useState(
    () => localStorage.getItem(STORAGE_KEY) ?? ""
  );
  const [input, setInput] = useState(userId);
  const [spinning, setSpinning] = useState(false);
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function drawWheel(angle) {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const cx = 160, cy = 160, r = 150;
    ctx.clearRect(0, 0, 320, 320);

    for (let i = 0; i < N; i++) {
      const start = angle + i * ARC;
      const end = start + ARC;

      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, r, start, end);
      ctx.closePath();
      ctx.fillStyle = COLORS[i];
      ctx.fill();
      ctx.strokeStyle = "#fff";
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(start + ARC / 2);
      ctx.textAlign = "right";
      ctx.fillStyle = "#fff";
      ctx.font = "bold 15px sans-serif";
      ctx.fillText(`${SEGMENTS[i]}%`, r - 12, 5);
      ctx.restore();
    }

    ctx.beginPath();
    ctx.arc(cx, cy, 20, 0, 2 * Math.PI);
    ctx.fillStyle = "#fff";
    ctx.fill();
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  const fetchStatus = useCallback(async (id) => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch(`/wheel/status/${id}`);
      setStatus(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    drawWheel(0);
    fetchStatus(userId);
  }, [userId, fetchStatus]);

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;
    localStorage.setItem(STORAGE_KEY, trimmed);
    setUserId(trimmed);
    setResult(null);
    setStatus(null);
  }

  async function spin() {
    if (spinning || !userId || !status?.can_spin) return;
    setSpinning(true);
    setResult(null);
    setError(null);

    let data;
    try {
      data = await apiFetch(`/wheel/spin/${userId}`, { method: "POST" });
    } catch (e) {
      setError(e.message);
      setSpinning(false);
      return;
    }

    const extraSpins = (5 + Math.floor(Math.random() * 5)) * 2 * Math.PI;
    const wonIndex = SEGMENTS.indexOf(data.discount_percent);
    const segmentMid = wonIndex * ARC + ARC / 2;
    const targetAngle = 2 * Math.PI - segmentMid - Math.PI / 2;
    const total =
      extraSpins +
      ((targetAngle - (angleRef.current % (2 * Math.PI)) + 2 * Math.PI) %
        (2 * Math.PI));

    const duration = 3500;
    const startTime = performance.now();
    const startAngle = angleRef.current;

    function animate(now) {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1);
      const ease = 1 - Math.pow(1 - t, 4);
      angleRef.current = startAngle + total * ease;
      drawWheel(angleRef.current);

      if (t < 1) {
        animFrameRef.current = requestAnimationFrame(animate);
      } else {
        setSpinning(false);
        setResult(data);
        setStatus((prev) => ({ ...prev, can_spin: false }));
      }
    }

    animFrameRef.current = requestAnimationFrame(animate);
  }

  const canSpin = !!userId && status?.can_spin === true && !spinning;

  return (
    <div className="max-w-xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-1">Spin & Save</h1>
      <p className="text-gray-500 mb-8">
        Spin once a month for a discount on your next QuickBite order.
      </p>

      <form onSubmit={handleSubmit} className="flex gap-2 mb-8">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter your customer ID"
          className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
        />
        <button
          type="submit"
          className="bg-orange-500 hover:bg-orange-600 text-white font-medium text-sm px-4 py-2 rounded-lg transition-colors"
        >
          Load
        </button>
        {userId && (
          <button
            type="button"
            onClick={() => {
              localStorage.removeItem(STORAGE_KEY);
              setUserId("");
              setInput("");
              setStatus(null);
              setResult(null);
            }}
            className="text-sm text-gray-400 hover:text-gray-600 px-2"
          >
            Clear
          </button>
        )}
      </form>

      <div className="flex flex-col items-center gap-6">
        <div className="relative">
          <div
            className="absolute left-1/2 -translate-x-1/2 z-10"
            style={{
              top: -18,
              width: 0,
              height: 0,
              borderLeft: "12px solid transparent",
              borderRight: "12px solid transparent",
              borderTop: "28px solid #e07b39",
            }}
          />
          <canvas
            ref={canvasRef}
            width={320}
            height={320}
            className="rounded-full"
          />
        </div>

        <button
          onClick={spin}
          disabled={!canSpin}
          className="px-10 py-3 rounded-lg text-white font-semibold text-lg transition-opacity"
          style={{
            background: "#e07b39",
            opacity: canSpin ? 1 : 0.45,
            cursor: canSpin ? "pointer" : "not-allowed",
          }}
        >
          {!userId
            ? "Enter your ID to spin"
            : loading
            ? "Loading..."
            : spinning
            ? "Spinning..."
            : status?.can_spin
            ? "Spin the Wheel"
            : "Already spun this month"}
        </button>

        {error && (
          <div className="w-full bg-red-50 border border-red-200 rounded-xl p-4 text-center">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {result && (
          <div className="w-full bg-orange-50 border border-orange-200 rounded-xl p-6 text-center">
            <p className="text-gray-500 text-sm mb-1">You won</p>
            <p className="text-5xl font-bold text-orange-500 mb-2">
              {result.discount_percent}% OFF
            </p>
            <p className="text-gray-600 text-sm">
              Use code{" "}
              <span className="font-mono font-semibold text-gray-800 bg-orange-100 px-2 py-0.5 rounded">
                {result.discount_code}
              </span>{" "}
              at checkout
            </p>
          </div>
        )}

        {!result && status && !status.can_spin && (
          <div className="w-full bg-gray-50 border border-gray-200 rounded-xl p-5 text-center">
            <p className="text-gray-500 text-sm mb-1">Your current discount</p>
            <p className="text-3xl font-bold text-orange-400 mb-2">
              {status.discount_percent}% OFF
            </p>
            <p className="text-gray-600 text-sm mb-3">
              Code:{" "}
              <span className="font-mono font-semibold text-gray-800 bg-gray-100 px-2 py-0.5 rounded">
                {status.discount_code}
              </span>
              {status.is_redeemed && (
                <span className="ml-2 text-xs text-green-600 font-medium">
                  ✓ Redeemed
                </span>
              )}
            </p>
            <p className="text-xs text-gray-400">
              Next spin available: {status.next_spin_date}
            </p>
          </div>
        )}

        {!userId && (
          <div className="text-center text-gray-400 text-sm">
            <p>Enter your customer ID above to spin</p>
          </div>
        )}
      </div>
    </div>
  );
}