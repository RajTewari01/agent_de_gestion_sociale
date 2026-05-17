import { UnifrakturMaguntia, Cormorant_Garamond } from "next/font/google";
import "@/app/globals.css";

const unifraktur = UnifrakturMaguntia({ subsets: ["latin"], weight: "400", variable: "--font-unifraktur" });
const cormorant = Cormorant_Garamond({ subsets: ["latin"], weight: ["300", "400", "600"], variable: "--font-cormorant" });

export const metadata = {
  title: "The Archives",
  description: "An editorial deep-dive into the ancient architectures.",
};

export default function SecretRootLayout({ children }) {
  return (
    <div 
      className={`${unifraktur.variable} ${cormorant.variable}`}
      style={{ 
        backgroundColor: '#000000', 
        minHeight: '100vh', 
        width: '100%',
        position: 'absolute',
        top: 0,
        left: 0,
        zIndex: 9999,
        margin: 0,
        padding: 0
      }}
    >
      {children}
    </div>
  );
}
