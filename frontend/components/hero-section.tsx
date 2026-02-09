"use client"
import { useEffect, useState } from "react"
import Link from "next/link"
import { AnimatedText } from "./animated-text"
import { ArrowUpRight } from "lucide-react"

export function HeroSection() {
  const [isVisible, setIsVisible] = useState(false)
  const [scrollProgress, setScrollProgress] = useState(0)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(true)
    }, 100)
    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    let rafId: number
    let currentProgress = 0

    const handleScroll = () => {
      const scrollY = window.scrollY
      const maxScroll = 400
      const targetProgress = Math.min(scrollY / maxScroll, 1)

      const smoothUpdate = () => {
        currentProgress += (targetProgress - currentProgress) * 0.1

        if (Math.abs(targetProgress - currentProgress) > 0.001) {
          setScrollProgress(currentProgress)
          rafId = requestAnimationFrame(smoothUpdate)
        } else {
          setScrollProgress(targetProgress)
        }
      }

      cancelAnimationFrame(rafId)
      smoothUpdate()
    }

    window.addEventListener("scroll", handleScroll, { passive: true })
    return () => {
      window.removeEventListener("scroll", handleScroll)
      cancelAnimationFrame(rafId)
    }
  }, [])

  const easeOutQuad = (t: number) => t * (2 - t)
  const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3)

  const scale = 1 - easeOutQuad(scrollProgress) * 0.15
  const borderRadius = easeOutCubic(scrollProgress) * 48
  const heightVh = 100 - easeOutQuad(scrollProgress) * 37.5

  return (
    <section className="pt-32 pb-20 px-6 min-h-screen flex items-center relative overflow-hidden">
      <div className="absolute inset-0 top-0">
        <div
          className="w-full will-change-transform overflow-hidden bg-gradient-to-br from-teal-400 to-cyan-500"
          style={{
            transform: `scale(${scale})`,
            borderRadius: `${borderRadius}px`,
            height: `${heightVh}vh`,
          }}
        />
      </div>

      <div
        className="absolute bottom-0 left-0 right-0 w-full overflow-hidden pointer-events-none z-[5] flex items-end justify-center"
        style={{
          transform: `translateY(${scrollProgress * 150}px)`,
          opacity: 1 - scrollProgress * 0.8,
          height: "100%",
        }}
      >
        <span
          className="block text-white font-bold text-[18vw] sm:text-[16vw] md:text-[14vw] lg:text-[12vw] tracking-tighter select-none text-center leading-none"
          style={{ marginBottom: "0" }}
        >
          DOCWEAVER
        </span>
      </div>

      <div className="max-w-7xl mx-auto w-full relative z-10">
        <div className="text-center mb-12">
          <div
            className={`transition-all duration-1000 delay-[800ms] ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 -translate-y-4"}`}
          >
            <h1 className="font-serif text-[3.5rem] sm:text-[4.5rem] md:text-[5.5rem] lg:text-[6.5rem] xl:text-[7.5rem] 2xl:text-[8.5rem] font-normal leading-tight mb-6 w-full px-4 max-w-6xl mx-auto text-balance">
              <AnimatedText text="Intelligent clinical documentation" delay={0.3} />
            </h1>
          </div>
        </div>

        <div className="flex flex-col items-center justify-center gap-8">
          <div className="relative">
            <div
              className={`relative w-[234px] md:w-[281px] lg:w-[351px] will-change-transform transition-all duration-[1500ms] ease-out delay-500 ${
                isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-[400px]"
              }`}
            >
              <p className="text-foreground text-center text-lg md:text-xl font-light">
                AI-powered document orchestration for clinical workflows
              </p>
            </div>
          </div>
          <div
            className={`flex flex-col sm:flex-row gap-4 mt-6 transition-all duration-1000 delay-[1000ms] ${
              isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
            }`}
          >
            <Link
              href="/demo"
              className="relative flex items-center justify-center gap-0 bg-foreground text-background rounded-full pl-6 pr-1.5 py-1.5 transition-all duration-300 group overflow-hidden hover:scale-105"
            >
              <span className="text-sm pr-4">Try Live Demo</span>
              <span className="w-10 h-10 bg-background rounded-full flex items-center justify-center">
                <ArrowUpRight className="w-4 h-4 text-foreground" />
              </span>
            </Link>
            <button
              onClick={() => document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })}
              className="relative flex items-center justify-center gap-0 border border-border rounded-full pl-6 pr-1.5 py-1.5 transition-all duration-300 group overflow-hidden"
            >
              <span className="absolute inset-0 bg-foreground rounded-full scale-x-0 origin-right group-hover:scale-x-100 transition-transform duration-300" />
              <span className="text-sm text-foreground group-hover:text-background pr-4 relative z-10 transition-colors duration-300">
                View Features
              </span>
              <span className="w-10 h-10 rounded-full flex items-center justify-center relative z-10">
                <ArrowUpRight className="w-4 h-4 text-foreground group-hover:text-background transition-colors duration-300" />
              </span>
            </button>
          </div>
        </div>
      </div>
    </section>
  )
}
