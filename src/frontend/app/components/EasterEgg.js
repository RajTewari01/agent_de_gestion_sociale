"use client";

import { useState, useEffect } from "react";
import { createPortal } from "react-dom";
import { useRouter } from "next/navigation";

export default function EasterEgg() {
  const [stage, setStage] = useState("idle"); 
  const [crackPaths, setCrackPaths] = useState([]);
  const router = useRouter();
  
  // Stages: idle -> cracking -> shattering -> blackout -> redirect

  const generateCracks = () => {
    const paths = [];
    const numRadials = Math.floor(Math.random() * 5) + 8; // 8 to 12 radial cracks
    const centerX = 50 + (Math.random() * 20 - 10);
    const centerY = 50 + (Math.random() * 20 - 10);
    
    const radials = [];

    // Generate Radial Cracks
    for (let i = 0; i < numRadials; i++) {
      let path = `M ${centerX} ${centerY}`;
      let currX = centerX;
      let currY = centerY;
      
      let baseAngle = (i * (Math.PI * 2)) / numRadials + (Math.random() * 0.2 - 0.1);
      const segments = Math.floor(Math.random() * 4) + 4; 
      
      const radialPoints = [];

      for (let j = 0; j < segments; j++) {
        const dist = 15 + Math.random() * 30;
        baseAngle += (Math.random() > 0.5 ? 1 : -1) * (Math.random() * 0.15); // Slight bend
        
        currX += Math.cos(baseAngle) * dist;
        currY += Math.sin(baseAngle) * dist;
        radialPoints.push({x: currX, y: currY});
        path += ` L ${currX} ${currY}`;
      }
      paths.push(path);
      radials.push(radialPoints);
    }
    
    // Generate Concentric (Spiderweb) Cracks connecting radials
    for (let i = 0; i < radials.length; i++) {
      const currentRadial = radials[i];
      const nextRadial = radials[(i + 1) % radials.length];
      
      const numConcentric = Math.min(currentRadial.length, nextRadial.length);
      for (let j = 0; j < numConcentric; j++) {
        // 70% chance to draw a transverse crack connecting the radials
        if (Math.random() > 0.3) {
          const p1 = currentRadial[j];
          const p2 = nextRadial[j];
          // Midpoint sag to simulate realistic stress fracture
          const midX = (p1.x + p2.x) / 2 + (Math.random() * 4 - 2);
          const midY = (p1.y + p2.y) / 2 + (Math.random() * 4 - 2);
          paths.push(`M ${p1.x} ${p1.y} L ${midX} ${midY} L ${p2.x} ${p2.y}`);
        }
      }
    }
    return paths;
  };

  const collapseDOM = () => {
    // Grab all structural/text elements AND panels AND footer to shatter
    const elements = document.querySelectorAll(
      "h1, h2, h4, p, li, span, button, .platform-icon, .tech-tag, .curve-divider, .premium-glass, .platform-btn, .sidebar, .hero-subtitle-box, .notes-container, img, svg, .official-footer, .footer-col, .footer-brand, .footer-bottom"
    );
    
    elements.forEach((el) => {
      // Skip easter egg elements
      if (el.closest('.easter-egg-container')) return;
      
      const dropY = window.innerHeight + 200;
      const rot = Math.random() * 180 - 90;
      const duration = 1 + Math.random() * 1.5;
      
      // Force hardware acceleration and relative positioning
      if (window.getComputedStyle(el).position === 'static') {
        el.style.position = 'relative';
      }
      
      el.style.transition = `transform ${duration}s cubic-bezier(0.55, 0.085, 0.68, 0.53), opacity ${duration}s ease-in`;
      el.style.transform = `translateY(${dropY}px) rotate(${rot}deg)`;
      el.style.opacity = '0';
    });
  };

  const trigger = (e) => {
    e.preventDefault();
    if (stage !== "idle") return;
    
    // 1. Generate new random crack pattern
    setCrackPaths(generateCracks());
    
    // 2. Start crack animation (Slowed down for suspense)
    setStage("cracking");
    
    // 3. Shatter the DOM (elements fall) after a long suspenseful crack
    setTimeout(() => {
      setStage("shattering");
      collapseDOM();
    }, 2500); // Wait 2.5s while cracks slowly draw
    
    // 4. Blackout the screen
    setTimeout(() => setStage("blackout"), 4500);
    
    // 5. Redirect to secret route
    setTimeout(() => {
       router.push("/secret");
       // Reset state shortly after redirecting so it's clean if they hit back
       setTimeout(() => {
         setStage("idle");
         window.location.reload(); 
       }, 500);
    }, 6000);
  };

  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  const overlay = (
    <div className={`easter-egg-container stage-${stage}`}>
      
      {/* Dynamic Screen Cracks */}
      {(stage === "cracking" || stage === "shattering") && (
        <div className="crack-overlay">
          <svg width="100%" height="100%" viewBox="0 0 100 100" preserveAspectRatio="none">
             {/* Background thick crack (outline) */}
             {crackPaths.map((d, i) => (
               <path 
                 key={`bg-${i}`}
                 d={d} 
                 className="crack-path crack-outline" 
                 style={{ animationDelay: `${Math.random() * 0.15}s` }}
               />
             ))}
             {/* Foreground thin crack (core) */}
             {crackPaths.map((d, i) => (
               <path 
                 key={`fg-${i}`}
                 d={d} 
                 className="crack-path crack-core" 
                 style={{ animationDelay: `${Math.random() * 0.15}s` }}
               />
             ))}
          </svg>
        </div>
      )}
    </div>
  );

  return (
    <>
      <a href="#surprise" onClick={trigger} className="surprise-link">Surprise</a>
      {mounted && stage !== "idle" && createPortal(overlay, document.body)}
    </>
  );
}
