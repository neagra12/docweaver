"use client"
import { useEffect, useState } from "react"

function useCountUp(end: number, duration = 2000, suffix = "") {
  const [count, setCount] = useState(0)
  const [hasStarted, setHasStarted] = useState(false)

  useEffect(() => {
    if (!hasStarted) return

    let startTime: number
    let animationFrame: number

    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime
      const progress = Math.min((currentTime - startTime) / duration, 1)

      const easeOutQuart = 1 - Math.pow(1 - progress, 4)
      setCount(Math.floor(easeOutQuart * end))

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate)
      }
    }

    animationFrame = requestAnimationFrame(animate)
    return () => cancelAnimationFrame(animationFrame)
  }, [end, duration, hasStarted])

  return { value: count + suffix, start: () => setHasStarted(true), hasStarted }
}

export function StatsSection() {
  const [isVisible, setIsVisible] = useState(false)

  const documents = useCountUp(10, 2000, "K+")
  const hospitals = useCountUp(250, 2000, "")
  const insights = useCountUp(50, 2000, "K+")

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isVisible) {
          setIsVisible(true)
          documents.start()
          hospitals.start()
          insights.start()
        }
      },
      { threshold: 0.3 },
    )

    const section = document.getElementById("stats-section")
    if (section) observer.observe(section)

    return () => observer.disconnect()
  }, [isVisible])

  return (
    <section id="stats-section" className="py-24 px-6 bg-background">
      <div className="max-w-4xl mx-auto"></div>
    </section>
  )
}
