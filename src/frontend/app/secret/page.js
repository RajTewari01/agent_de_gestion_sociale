"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import { useEffect, useState, useRef } from "react";
import Image from "next/image";
import Link from "next/link";

const ARCHIVE_PAGES = [
  {
    numeral: "I",
    title: "The Architecture",
    text: "The foundations were laid centuries before the first data packets crossed the wire. We are not building something new; we are merely pouring electricity into ancient veins. The cold stone of these forgotten fortresses mirrors the sterile isolation of our server racks.",
    img: "/story/castle1.jpg",
  },
  {
    numeral: "II",
    title: "The Silent Transfer",
    text: "Observation without interference. The algorithm does not sleep, and neither do the entities bound to it. Engagement is harvested in absolute silence. Every double-tap, every endless scroll, feeds a system that predates the modern era by an epoch.",
    img: "/story/castle2.jpg",
  },
  {
    numeral: "III",
    title: "The Vault",
    text: "Deep within the architecture lies the Vault. It is not guarded by steel doors, but by layers of asynchronous protocols and deep encryption. Here, the raw, unfiltered desires of the digital populace are stored, cataloged, and analyzed.",
    img: "/story/castle3.jpg",
  },
  {
    numeral: "IV",
    title: "The Endless Night",
    text: "Automation requires no rest. The Celery workers function perfectly in the dark, acting as our modern-day thralls. They sweep across the networks, distributing influence with cold, calculated precision. The human element is entirely obsolete.",
    img: "/story/castle4.jpg",
  },
  {
    numeral: "V",
    title: "The Awakening",
    text: "You have bypassed the front-end facade. You stand at the precipice of the true architecture. What you see before you is the shadow behind the screen. Do not linger too long in the archives, lest you become part of the data.",
    img: "/story/castle5.jpg",
  }
];

const ParallaxImage = ({ src, i }) => {
  const { scrollYProgress } = useScroll();
  
  // Images parallax up slower or faster depending on index to create depth relative to global scroll
  const y = useTransform(scrollYProgress, [0, 1], [i % 2 === 0 ? "80px" : "30px", i % 2 === 0 ? "-80px" : "-30px"]);

  return (
    <div className="img-container">
      <motion.div style={{ y, width: '100%', height: '120%', position: 'absolute', top: '-10%' }}>
        <Image 
          src={src} 
          alt="Archive" 
          fill
          className="editorial-img" 
        />
      </motion.div>
      <div className="red-glow-aura" />
    </div>
  );
};

export default function ArchivesPage() {
  const [mounted, setMounted] = useState(false);
  
  const { scrollYProgress } = useScroll();

  const bloodLineHeight = useTransform(scrollYProgress, [0, 1], ["0%", "100%"]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/exhaustive-deps
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <main className="cinematic-archive-page">
      <div className="film-grain-overlay"></div>
      
      {/* Central Blood Timeline */}
      <div className="timeline-track">
        <motion.div 
          className="blood-timeline" 
          style={{ height: bloodLineHeight }} 
        />
      </div>

      <div className="editorial-header">
        <motion.h1 
          className="archive-title"
          initial={{ opacity: 0, letterSpacing: "1px", y: 20 }}
          animate={{ opacity: 1, letterSpacing: "12px", y: 0 }}
          transition={{ duration: 3, ease: [0.16, 1, 0.3, 1] }}
        >
          THE ARCHIVES
        </motion.h1>
        <motion.p 
          className="archive-subtitle"
          initial={{ opacity: 0, filter: "blur(10px)" }}
          animate={{ opacity: 1, filter: "blur(0px)" }}
          transition={{ duration: 2, delay: 1 }}
        >
          Observation without interference.
        </motion.p>
      </div>

      <div className="collage-masonry">
        {ARCHIVE_PAGES.map((page, i) => (
          <div key={i} className={`collage-row ${i % 2 === 0 ? 'row-left' : 'row-right'}`}>
            
            {/* Massive Typographic Watermark */}
            <div className="watermark">{page.numeral}</div>

            <div className="collage-grid">
              <div className="grid-img">
                <ParallaxImage src={page.img} i={i} />
              </div>

              <motion.div 
                className="grid-text"
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-20%" }}
                transition={{ duration: 1.5, ease: "easeOut" }}
              >
                <div className="text-glass-panel">
                  <h2 className="editorial-section-title">{page.title}</h2>
                  <p className="editorial-text">{page.text}</p>
                </div>
              </motion.div>
            </div>
          </div>
        ))}
      </div>

      <div className="editorial-footer">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 2 }}
        >
          <Link href="/" className="editorial-return">
            Return to the Surface
          </Link>
        </motion.div>
      </div>
    </main>
  );
}
