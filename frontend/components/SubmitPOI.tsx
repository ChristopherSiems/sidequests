"use client";

import { useState } from "react";

const DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

interface FormState {
  title: string;
  description: string;
  location: string;
  open_time: string;
  close_time: string;
  min_time_minutes: string;
  day: string;
}

const EMPTY: FormState = {
  title: "",
  description: "",
  location: "",
  open_time: "00:00",
  close_time: "23:59",
  min_time_minutes: "15",
  day: "Monday",
};

async function geocodeAddress(address: string): Promise<{ lat: number; lon: number } | null> {
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=1`;
  const res = await fetch(url, { headers: { "Accept-Language": "en" } });
  const data = await res.json();
  if (!data.length) return null;
  return { lat: parseFloat(data[0].lat), lon: parseFloat(data[0].lon) };
}

export default function SubmitPOI() {
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<FormState>(EMPTY);
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [errorMsg, setErrorMsg] = useState("");

  const set = (field: keyof FormState) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => setForm(f => ({ ...f, [field]: e.target.value }));

  const handleSubmit = async () => {
    if (!form.title.trim() || !form.location.trim()) {
      setErrorMsg("Title and location are required.");
      setStatus("error");
      return;
    }

    setStatus("loading");
    setErrorMsg("");

    // Geocode address → lat/lng
    const coords = await geocodeAddress(form.location);
    if (!coords) {
      setErrorMsg("Couldn't find that address. Try being more specific.");
      setStatus("error");
      return;
    }

    const payload = {
      title: form.title.trim(),
      description: form.description.trim(),
      location: form.location.trim(),
      latitude: coords.lat,
      longitude: coords.lon,
      open_time: form.open_time,
      close_time: form.close_time,
      min_time: parseInt(form.min_time_minutes, 10) * 60, // convert to seconds
      day: form.day,
      categories: "",
      image: "",
      link: "",
    };

    try {
      const res = await fetch(`${API_BASE}/pois`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      setStatus("success");
      setTimeout(() => {
        setOpen(false);
        setForm(EMPTY);
        setStatus("idle");
      }, 1800);
    } catch (err) {
      setErrorMsg(err instanceof Error ? err.message : "Submission failed.");
      setStatus("error");
    }
  };

  return (
    <>
      {/* ── Floating trigger button ── */}
      <button
        onClick={() => setOpen(true)}
        style={{
          position: "fixed",
          bottom: "24px",
          right: "24px",
          background: "#5a6472",
          color: "#fff",
          border: "none",
          borderRadius: "8px",
          padding: "10px 16px",
          fontSize: "13px",
          cursor: "pointer",
          boxShadow: "0 2px 8px rgba(0,0,0,0.18)",
          zIndex: 50,
          letterSpacing: "0.02em",
        }}
      >
        + Submit a Place
      </button>

      {/* ── Modal overlay ── */}
      {open && (
        <div
          onClick={(e) => e.target === e.currentTarget && setOpen(false)}
          style={{
            position: "fixed", inset: 0,
            background: "rgba(0,0,0,0.35)",
            display: "flex", alignItems: "center", justifyContent: "center",
            zIndex: 100,
          }}
        >
          <div style={{
            background: "#fff",
            borderRadius: "12px",
            padding: "32px 28px",
            width: "min(480px, 92vw)",
            maxHeight: "90vh",
            overflowY: "auto",
            boxShadow: "0 8px 32px rgba(0,0,0,0.18)",
            fontFamily: "inherit",
          }}>
            <h2 style={{ margin: "0 0 20px", fontSize: "20px", fontWeight: 700 }}>
              Submit a Place
            </h2>

            <Field label="Title *">
              <input value={form.title} onChange={set("title")} placeholder="e.g. Walk a lap around University Park" />
            </Field>

            <Field label="Description">
              <textarea value={form.description} onChange={set("description")} rows={3} placeholder="What makes this a good quick quest?" />
            </Field>

            <Field label="Address *">
              <input value={form.location} onChange={set("location")} placeholder="965 Main St, Worcester, MA 01610" />
              <span style={{ fontSize: "11px", color: "#888", marginTop: "4px", display: "block" }}>
                Lat/lng will be filled in automatically.
              </span>
            </Field>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
              <Field label="Opens">
                <input type="time" value={form.open_time} onChange={set("open_time")} />
              </Field>
              <Field label="Closes">
                <input type="time" value={form.close_time} onChange={set("close_time")} />
              </Field>
            </div>

            <Field label="Minimum time to complete (minutes)">
              <input
                type="number" min={1} max={480}
                value={form.min_time_minutes} onChange={set("min_time_minutes")}
              />
            </Field>

            <Field label="Day">
              <select value={form.day} onChange={set("day")}>
                {DAYS.map(d => <option key={d}>{d}</option>)}
              </select>
            </Field>

            {status === "error" && (
              <p style={{ color: "#c0392b", fontSize: "13px", margin: "8px 0 0" }}>{errorMsg}</p>
            )}
            {status === "success" && (
              <p style={{ color: "#27ae60", fontSize: "13px", margin: "8px 0 0" }}>✓ Place submitted successfully!</p>
            )}

            <div style={{ display: "flex", gap: "10px", marginTop: "24px", justifyContent: "flex-end" }}>
              <button onClick={() => setOpen(false)} style={ghostBtn}>Cancel</button>
              <button
                onClick={handleSubmit}
                disabled={status === "loading"}
                style={{ ...primaryBtn, opacity: status === "loading" ? 0.6 : 1 }}
              >
                {status === "loading" ? "Submitting…" : "Submit"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

// ── Tiny helper components ──

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ marginBottom: "14px" }}>
      <label style={{ display: "block", fontSize: "12px", fontWeight: 600, marginBottom: "5px", color: "#444" }}>
        {label}
      </label>
      <div style={{ display: "flex", flexDirection: "column" }}>{children}</div>
    </div>
  );
}

const inputBase: React.CSSProperties = {
  width: "100%", boxSizing: "border-box",
  border: "1px solid #ddd", borderRadius: "6px",
  padding: "8px 10px", fontSize: "14px",
  fontFamily: "inherit", outline: "none",
};

// Inject shared input styles via a style tag so we don't repeat per-element inline styles.
// In a real Next.js project you'd put this in globals.css instead.
if (typeof document !== "undefined") {
  const id = "poi-form-styles";
  if (!document.getElementById(id)) {
    const s = document.createElement("style");
    s.id = id;
    s.textContent = `
      .poi-form input, .poi-form textarea, .poi-form select {
        width: 100%; box-sizing: border-box;
        border: 1px solid #ddd; border-radius: 6px;
        padding: 8px 10px; font-size: 14px;
        font-family: inherit; outline: none;
        transition: border-color 0.15s;
      }
      .poi-form input:focus, .poi-form textarea:focus, .poi-form select:focus {
        border-color: #5a6472;
      }
      .poi-form textarea { resize: vertical; }
    `;
    document.head.appendChild(s);
  }
}

const primaryBtn: React.CSSProperties = {
  background: "#5a6472", color: "#fff",
  border: "none", borderRadius: "8px",
  padding: "10px 22px", fontSize: "14px",
  cursor: "pointer", fontFamily: "inherit",
};

const ghostBtn: React.CSSProperties = {
  background: "transparent", color: "#5a6472",
  border: "1px solid #ccc", borderRadius: "8px",
  padding: "10px 18px", fontSize: "14px",
  cursor: "pointer", fontFamily: "inherit",
};

