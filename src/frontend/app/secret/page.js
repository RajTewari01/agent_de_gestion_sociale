"use client";
import React, { useEffect, useRef, useState } from "react";
import { motion, useScroll, useTransform, useMotionValue, useSpring } from "framer-motion";

const entries = [
  { id:1, date:"XIII October MDCCCLXXXVIII", title:"The First Entry", sigil:"✦",
    image:"/story/castle1.jpg", caption:"Ashford Manor — through the fog.",
    epigraph:"\"I felt the pulse of the house beneath my skin.\"",
    text:"The wind whispered through cracked shutters, carrying a scent of rot and lavender. I arrived at the manor as the last light bled from the sky — a wound in the heavens that refused to close. The candles in the foyer flickered in an uneasy rhythm, casting verses of shadow upon the stone. I pressed my palm to the wall and felt the house breathe back." },
  { id:2, date:"II November MDCCCLXXXVIII", title:"Midnight Reflections", sigil:"⚜",
    image:"/story/castle3.jpg", caption:"The fortress at twilight.",
    epigraph:"\"The ink trembled as the quill met the page.\"",
    text:"I sat at the oak desk, surrounded by ancient tomes whose spines cracked like old bones. The fireplace roared, yet a chill clung to the air as if the cold itself were alive. In the corner, a portrait stared with eyes that followed my every movement. A raven cried somewhere in the dark, its voice threading through the walls like a needle through flesh." },
  { id:3, date:"I December MDCCCLXXXVIII", title:"The Unveiling", sigil:"◆",
    image:"/story/img1.png", caption:"The Watcher — guardian of forbidden archives.",
    epigraph:"\"Each shard showed a different night, a different breath.\"",
    text:"The mirror fractured under my trembling hand, splintering the reflected flames into a thousand ghosts. I watched my face multiply and distort — each fragment showing a version of myself I did not recognize. Then I heard it: a whisper that fell like blood upon my ears. Something moved behind me. When I turned, there was nothing — only the smell of iron and old roses." },
  { id:4, date:"XV January MDCCCLXXXIX", title:"The Whispering Hall", sigil:"☽",
    image:"/story/castle4.jpg", caption:"The cathedral of silence.",
    epigraph:"\"The walls urged me deeper into the darkness.\"",
    text:"The hallway stretched impossibly — far beyond the dimensions of the manor itself. Stone walls dripped with condensation that tasted of copper. A lone lantern threw trembling shadows that moved independently of the flame. Soft murmurs rose from beneath the floor, syllables I almost recognized, names I had forgotten I knew." },
  { id:5, date:"II February MDCCCLXXXIX", title:"The Final Seal", sigil:"†",
    image:"/story/castle5.jpg", caption:"Where the final seal was hidden.",
    epigraph:"\"A river of ink-black memories seeped into the floorboards.\"",
    text:"At the heart of the manor lay a vault sealed with iron and inscribed with sigils of forgotten rites. I knew — without knowing how — the sequence to trace upon the cold metal. As my finger completed the final arc, the seal fractured with a sound like a church bell rung underwater. Ink-black memories poured forth. I was not the first to write in this diary. I was the diary itself." },
];

/* ═══ Diary Entry — alternating image + text layout ═══ */
function DiaryEntry({ entry, index }) {
  const isOdd = index % 2 !== 0;

  return (
    <motion.article
      initial={{ opacity: 0, y: 60 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, ease: "easeOut" }}
      viewport={{ once: true, margin: "-50px" }}
      style={{
        display: "flex",
        flexDirection: isOdd ? "row-reverse" : "row",
        gap: "2.5rem",
        alignItems: "center",
        maxWidth: "1100px",
        margin: "0 auto 6rem",
        padding: "0 2rem",
      }}
    >
      {/* IMAGE SIDE */}
      <motion.div
        style={{ flex: "1 1 50%", position: "relative", overflow: "hidden", borderRadius: "4px" }}
        whileHover={{ scale: 1.02 }}
        transition={{ duration: 0.4 }}
      >
        <img
          src={entry.image}
          alt={entry.caption}
          style={{
            width: "100%",
            height: "420px",
            objectFit: "cover",
            display: "block",
            filter: "sepia(0.15) brightness(0.75) contrast(1.05)",
            borderRadius: "4px",
          }}
        />
        {/* Subtle edge vignette only */}
        <div style={{
          position: "absolute", inset: 0, borderRadius: "4px",
          background: "radial-gradient(ellipse at 50% 50%, transparent 50%, rgba(10,5,5,0.4) 100%)",
          pointerEvents: "none",
        }} />
        {/* Thin red border glow */}
        <div style={{
          position: "absolute", inset: 0, borderRadius: "4px",
          border: "1px solid rgba(139,0,0,0.2)",
          boxShadow: "inset 0 0 30px rgba(139,0,0,0.08)",
          pointerEvents: "none",
        }} />
        {/* Caption below image */}
        <div style={{
          fontFamily: "var(--font-cormorant),serif", fontStyle: "italic",
          fontSize: "0.7rem", color: "rgba(200,160,160,0.6)",
          marginTop: "0.6rem", paddingLeft: "0.3rem",
        }}>
          {entry.caption}
        </div>
      </motion.div>

      {/* TEXT SIDE */}
      <div style={{ flex: "1 1 50%" }}>
        {/* Chapter label */}
        <motion.div
          style={{
            fontFamily: "var(--font-cormorant),serif", fontSize: "0.6rem",
            letterSpacing: "0.5em", textTransform: "uppercase",
            color: "rgba(139,0,0,0.5)", marginBottom: "0.8rem",
          }}
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
          viewport={{ once: true }}
        >
          Chapter {entry.id}
        </motion.div>

        {/* Sigil */}
        <motion.div
          style={{
            fontSize: "1.6rem", color: "#8B0000",
            filter: "drop-shadow(0 0 10px rgba(139,0,0,0.5))",
            marginBottom: "0.8rem",
          }}
          initial={{ scale: 0 }}
          whileInView={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 120, damping: 14, delay: 0.2 }}
          viewport={{ once: true }}
        >
          {entry.sigil}
        </motion.div>

        {/* Date */}
        <div style={{
          fontFamily: "var(--font-cormorant),serif", fontSize: "0.65rem",
          letterSpacing: "0.25em", color: "rgba(180,120,120,0.6)", marginBottom: "0.6rem",
        }}>
          {entry.date}
        </div>

        {/* Title */}
        <motion.h2
          style={{
            fontFamily: "var(--font-unifraktur),cursive",
            fontSize: "clamp(1.5rem, 3vw, 2.2rem)", fontWeight: 400,
            color: "#dfc0b8", lineHeight: 1.3, marginBottom: "1rem",
            textShadow: "0 0 25px rgba(139,0,0,0.2)",
          }}
          initial={{ opacity: 0, x: isOdd ? 30 : -30 }}
          whileInView={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          viewport={{ once: true }}
        >
          {entry.title}
        </motion.h2>

        {/* Divider */}
        <motion.div
          style={{
            width: "60px", height: "1px", marginBottom: "1rem",
            background: "linear-gradient(90deg, #8B0000, transparent)",
            transformOrigin: "left",
          }}
          initial={{ scaleX: 0 }}
          whileInView={{ scaleX: 1 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
        />

        {/* Epigraph */}
        <p style={{
          fontFamily: "var(--font-cormorant),serif", fontStyle: "italic",
          fontSize: "0.85rem", color: "rgba(180,100,100,0.7)",
          marginBottom: "1.2rem", lineHeight: 1.6,
        }}>
          {entry.epigraph}
        </p>

        {/* Body text */}
        <motion.p
          style={{
            fontFamily: "var(--font-cormorant),serif", fontSize: "1rem",
            lineHeight: 1.95, color: "#d4b8b0",
          }}
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.4 }}
          viewport={{ once: true }}
        >
          {entry.text}
        </motion.p>
      </div>
    </motion.article>
  );
}

/* ═══ MAIN PAGE ═══ */
export default function SecretPage() {
  const { scrollYProgress } = useScroll();
  const progressWidth = useTransform(scrollYProgress, [0, 1], ["0%", "100%"]);

  const heroRef = useRef(null);
  const { scrollYProgress: hp } = useScroll({ target: heroRef, offset: ["start start", "end start"] });
  const heroImgY = useTransform(hp, [0, 1], ["0%", "30%"]);
  const heroOpacity = useTransform(hp, [0, 0.7], [1, 0]);
  const heroTitleY = useTransform(hp, [0, 1], [0, -80]);

  // Custom cursor
  const cx = useMotionValue(0), cy = useMotionValue(0);
  const sx = useSpring(cx, { stiffness: 250, damping: 25 });
  const sy = useSpring(cy, { stiffness: 250, damping: 25 });
  useEffect(() => {
    const m = e => { cx.set(e.clientX - 10); cy.set(e.clientY - 10); };
    window.addEventListener("pointermove", m);
    return () => window.removeEventListener("pointermove", m);
  }, [cx, cy]);

  // Embers (client only)
  const [embers, setEmbers] = useState([]);
  useEffect(() => {
    setEmbers(Array.from({ length: 12 }, (_, i) => ({
      id: i, left: Math.random() * 100, size: Math.random() * 3 + 1,
      dur: Math.random() * 10 + 12, delay: Math.random() * 8,
      drift: (Math.random() - 0.5) * 50, h: window.innerHeight,
    })));
  }, []);

  return (
    <div style={{ background: "#0a0506", color: "#d4b8b0", position: "relative", overflowX: "hidden", cursor: "none" }}>

      {/* Cursor */}
      <motion.div style={{
        position: "fixed", top: 0, left: 0, x: sx, y: sy,
        width: 20, height: 20, borderRadius: "50%",
        border: "1px solid rgba(139,0,0,0.5)",
        background: "rgba(139,0,0,0.06)",
        boxShadow: "0 0 12px rgba(139,0,0,0.2)",
        pointerEvents: "none", zIndex: 9999, mixBlendMode: "screen",
      }} />

      {/* Film grain — very subtle */}
      <svg style={{ position: "fixed", inset: 0, width: "100%", height: "100%", pointerEvents: "none", zIndex: 50, opacity: 0.025, mixBlendMode: "overlay" }}>
        <filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="4" stitchTiles="stitch" /></filter>
        <rect width="100%" height="100%" filter="url(#g)" />
      </svg>

      {/* Light vignette */}
      <div style={{ position: "fixed", inset: 0, background: "radial-gradient(ellipse 75% 65% at 50% 50%, transparent 0%, rgba(0,0,0,0.3) 70%, rgba(0,0,0,0.6) 100%)", pointerEvents: "none", zIndex: 49 }} />

      {/* Progress bar */}
      <motion.div style={{
        position: "fixed", top: 0, left: 0, height: "2px",
        background: "linear-gradient(90deg, #3a0000, #8B0000, #cc3333, #8B0000)",
        width: progressWidth, zIndex: 100,
        boxShadow: "0 0 8px rgba(139,0,0,0.6)",
      }} />

      {/* Floating embers */}
      {embers.map(e => (
        <motion.div key={e.id} style={{
          position: "fixed", bottom: -20, left: `${e.left}%`,
          width: e.size, height: e.size, borderRadius: "50%",
          background: "radial-gradient(circle,rgba(255,100,30,0.8),rgba(139,0,0,0.3))",
          boxShadow: `0 0 ${e.size * 3}px rgba(255,60,0,0.4)`,
          pointerEvents: "none", zIndex: 2,
        }}
          animate={{ y: [0, -(e.h + 40)], x: [0, e.drift], opacity: [0, 0.7, 0.7, 0], scale: [0.5, 1, 0.8, 0.2] }}
          transition={{ repeat: Infinity, duration: e.dur, delay: e.delay, ease: "easeOut" }}
        />
      ))}

      {/* ═══════ HERO ═══════ */}
      <section ref={heroRef} style={{ position: "relative", height: "100vh", overflow: "hidden" }}>
        {/* BG image — brighter */}
        <motion.div style={{ position: "absolute", inset: "-15%", y: heroImgY }}>
          <img src="/story/img2.png" alt="Dark castle on mountain with blood moon"
            style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: "center 30%", filter: "brightness(0.55) contrast(1.1) saturate(0.75)" }} />
        </motion.div>

        {/* Gradient — less opaque so image shows through */}
        <div style={{ position: "absolute", inset: 0, background: "linear-gradient(to bottom, rgba(10,5,6,0.15) 0%, rgba(10,5,6,0.05) 40%, rgba(10,5,6,0.5) 80%, #0a0506 100%)" }} />

        {/* Hero text */}
        <motion.div style={{
          position: "relative", zIndex: 2, height: "100%",
          display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center",
          opacity: heroOpacity, y: heroTitleY,
        }}>
          {/* Glow behind title */}
          <motion.div style={{
            position: "absolute", width: "350px", height: "350px", borderRadius: "50%",
            background: "radial-gradient(circle, rgba(139,0,0,0.1) 0%, transparent 70%)",
            pointerEvents: "none",
          }}
            animate={{ scale: [1, 1.3, 1], opacity: [0.15, 0.35, 0.15] }}
            transition={{ repeat: Infinity, duration: 6, ease: "easeInOut" }}
          />

          <motion.div style={{ fontSize: "1rem", color: "#cc4444", opacity: 0.4, letterSpacing: "1.2em", marginBottom: "2rem" }}
            initial={{ opacity: 0 }} animate={{ opacity: 0.4 }} transition={{ delay: 0.5, duration: 2 }}>
            ✦ ✦ ✦
          </motion.div>

          <motion.h1 style={{
            fontFamily: "var(--font-unifraktur),cursive",
            fontSize: "clamp(3rem, 9vw, 7.5rem)", fontWeight: 400,
            color: "#cc3333",
            textShadow: "0 0 25px rgba(200,50,50,0.4), 0 0 60px rgba(139,0,0,0.2), 0 2px 40px rgba(0,0,0,0.6)",
            textAlign: "center", lineHeight: 1.05, margin: 0,
          }}
            initial={{ y: 50, opacity: 0, scale: 0.9 }}
            animate={{ y: 0, opacity: 1, scale: 1 }}
            transition={{ duration: 1.5, ease: [0.16, 1, 0.3, 1] }}
          >
            Blood &amp; Ink
          </motion.h1>

          <motion.p style={{
            fontFamily: "var(--font-cormorant),serif", fontStyle: "italic",
            fontSize: "clamp(0.85rem, 1.4vw, 1.1rem)",
            color: "rgba(220,180,180,0.7)", marginTop: "1rem", letterSpacing: "0.12em",
          }}
            initial={{ y: 25, opacity: 0 }} animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.6, duration: 1.2 }}
          >
            A cursed manuscript from the ruins of Ashford Manor
          </motion.p>

          <motion.div style={{ width: "180px", height: "1px", background: "linear-gradient(90deg, transparent, #cc3333, transparent)", marginTop: "2rem" }}
            initial={{ scaleX: 0 }} animate={{ scaleX: 1 }}
            transition={{ delay: 1, duration: 1 }}
          />

          {/* Scroll cue */}
          <div style={{ position: "absolute", bottom: "2.5rem", display: "flex", flexDirection: "column", alignItems: "center", gap: "0.4rem" }}>
            <motion.span style={{
              fontFamily: "var(--font-cormorant),serif", fontSize: "0.6rem",
              letterSpacing: "0.3em", textTransform: "uppercase", color: "rgba(200,100,100,0.5)",
            }}
              animate={{ opacity: [0.2, 0.7, 0.2] }}
              transition={{ repeat: Infinity, duration: 3 }}
            >
              Descend
            </motion.span>
            <motion.div style={{ width: "1px", height: "25px", background: "linear-gradient(to bottom, #cc3333, transparent)" }}
              animate={{ scaleY: [0.4, 1, 0.4], opacity: [0.3, 0.7, 0.3] }}
              transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
            />
          </div>
        </motion.div>
      </section>

      {/* ═══════ VOLUME HEADER ═══════ */}
      <motion.div
        style={{ textAlign: "center", padding: "5rem 2rem 4rem", position: "relative", zIndex: 10 }}
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <div style={{ fontFamily: "var(--font-cormorant),serif", fontSize: "0.6rem", letterSpacing: "0.5em", textTransform: "uppercase", color: "rgba(180,100,100,0.5)", marginBottom: "0.5rem" }}>
          Recovered Manuscript
        </div>
        <div style={{ fontFamily: "var(--font-unifraktur),cursive", fontSize: "clamp(1.2rem, 2.5vw, 1.6rem)", color: "#8a5050" }}>
          Volume I — The Ashford Confessions
        </div>
        <motion.div style={{ width: "120px", height: "1px", background: "linear-gradient(90deg, transparent, #8B0000, transparent)", margin: "1.5rem auto 0" }}
          initial={{ scaleX: 0 }} whileInView={{ scaleX: 1 }}
          transition={{ duration: 0.8, delay: 0.3 }} viewport={{ once: true }}
        />
      </motion.div>

      {/* ═══════ DIARY ENTRIES ═══════ */}
      <div style={{ position: "relative", zIndex: 10, paddingBottom: "4rem" }}>
        {entries.map((e, i) => <DiaryEntry key={e.id} entry={e} index={i} />)}
      </div>

      {/* ═══════ FOOTER ═══════ */}
      <footer style={{ position: "relative", zIndex: 10, textAlign: "center", padding: "4rem 2rem 3rem" }}>
        <motion.div style={{ width: "160px", height: "1px", background: "linear-gradient(90deg, transparent, #8B0000, transparent)", margin: "0 auto 2rem" }}
          initial={{ scaleX: 0 }} whileInView={{ scaleX: 1 }}
          transition={{ duration: 0.8 }} viewport={{ once: true }}
        />
        <motion.div style={{ fontSize: "1.3rem", color: "#8B0000", opacity: 0.5, marginBottom: "0.8rem" }}
          animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 30, ease: "linear" }}>
          ✦
        </motion.div>
        <div style={{ fontFamily: "var(--font-cormorant),serif", fontSize: "0.65rem", letterSpacing: "0.4em", textTransform: "uppercase", color: "rgba(140,80,80,0.5)" }}>
          End of Volume I
        </div>
        <div style={{ fontFamily: "var(--font-cormorant),serif", fontStyle: "italic", fontSize: "0.6rem", color: "rgba(140,80,80,0.3)", marginTop: "0.4rem" }}>
          The remaining volumes were never recovered.
        </div>
      </footer>
    </div>
  );
}
