"use client"

import { Check } from "lucide-react"
import { useState, useEffect, useRef } from "react"
import { motion } from "framer-motion"

const features = [
  "Multi-Source Data Fusion - Process 5+ documents in parallel",
  "Temporal Trend Analysis - Track changes over time",
  "Automated SOAP Note Generation from brief notes",
  "ICD-10 & CPT Code Extraction with AI",
  "Care Coordination with auto-referrals",
  "20+ Specialized AI Agents working together",
  "Real-time Document Processing",
  "HIPAA Compliant & Secure Infrastructure",
]

const allTransactions = [
  { name: "ER Discharge Notes", amount: "+847", category: "Documents", color: "from-emerald-400 to-teal-500" },
  { name: "Lab Results", amount: "+1,240", category: "Insights", color: "from-blue-400 to-indigo-500" },
  { name: "Cardiology Reports", amount: "+562", category: "Documents", color: "from-amber-400 to-orange-500" },
  { name: "Consultation Notes", amount: "+1,923", category: "Documents", color: "from-rose-400 to-pink-500" },
  { name: "Test Analysis", amount: "+678", category: "Insights", color: "from-violet-400 to-purple-500" },
  { name: "Clinical Summary", amount: "+1,450", category: "Documents", color: "from-cyan-400 to-blue-500" },
  { name: "Patient Records", amount: "+892", category: "Documents", color: "from-lime-400 to-green-500" },
  { name: "Diagnostic Report", amount: "+1,105", category: "Insights", color: "from-fuchsia-400 to-pink-500" },
]

export function FeaturesSection() {
  const [balance, setBalance] = useState(12458)
  const scrollRef = useRef<HTMLDivElement>(null)
  const animationRef = useRef<number>()
  const scrollPosition = useRef(0)
  const lastUpdateTime = useRef(0)

  const tripleTransactions = [...allTransactions, ...allTransactions, ...allTransactions]

  useEffect(() => {
    const animate = (timestamp: number) => {
      if (!scrollRef.current) {
        animationRef.current = requestAnimationFrame(animate)
        return
      }

      if (!lastUpdateTime.current) lastUpdateTime.current = timestamp
      const deltaTime = timestamp - lastUpdateTime.current
      lastUpdateTime.current = timestamp

      scrollPosition.current += (deltaTime / 1000) * 35

      const singleSetHeight = scrollRef.current.scrollHeight / 3

      if (scrollPosition.current >= singleSetHeight) {
        scrollPosition.current = 0

        const randomTransaction = allTransactions[Math.floor(Math.random() * allTransactions.length)]
        const amount = Number.parseFloat(randomTransaction.amount.replace(/[$,]/g, ""))
        setBalance((prev) => prev + amount)
      }

      scrollRef.current.style.transform = `translateY(-${scrollPosition.current}px)`
      animationRef.current = requestAnimationFrame(animate)
    }

    animationRef.current = requestAnimationFrame(animate)

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [])

  return (
    <section id="features" className="py-28 px-6 relative overflow-hidden">
      <div className="absolute top-1/2 -translate-y-1/2 left-0 right-0 flex justify-center pointer-events-none z-0">
        <span className="font-bold text-center text-[20vw] sm:text-[18vw] md:text-[16vw] lg:text-[14vw] leading-none tracking-tighter text-zinc-100 whitespace-nowrap">
          FEATURES
        </span>
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-8 items-center">
          <div>
            <h2 className="text-4xl md:text-5xl lg:text-6xl font-serif font-normal mb-8 leading-tight">
              Everything you need for clinical excellence
            </h2>
            <ul className="space-y-4">
              {features.map((feature, i) => (
                <li key={i} className="flex items-center gap-3">
                  <Check className="w-5 h-5 text-foreground flex-shrink-0" />
                  <span className="text-lg text-foreground">{feature}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="relative h-96 rounded-2xl overflow-hidden border border-border bg-gradient-to-br from-background to-muted p-6">
            <div className="absolute top-0 left-0 right-0 w-full h-16 bg-gradient-to-b from-background to-transparent pointer-events-none z-10" />
            <div className="absolute bottom-0 left-0 right-0 w-full h-16 bg-gradient-to-t from-background to-transparent pointer-events-none z-10" />

            <div ref={scrollRef} className="space-y-4 will-change-transform">
              {tripleTransactions.map((transaction, i) => (
                <div
                  key={i}
                  className={`flex items-center gap-3 p-4 rounded-lg border border-border bg-card/50 backdrop-blur`}
                >
                  <div
                    className={`w-3 h-3 rounded-full bg-gradient-to-r ${transaction.color}`}
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">
                      {transaction.name}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {transaction.category}
                    </p>
                  </div>
                  <p className="text-sm font-medium text-foreground whitespace-nowrap">
                    {transaction.amount}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
