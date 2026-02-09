"use client"

import { FileText, Brain, Lock } from "lucide-react"
import { useState, useEffect, useRef } from "react"

const services = [
  {
    icon: FileText,
    title: "Document Processing",
    description: "Automated extraction and analysis of clinical documents with AI-powered intelligence.",
  },
  {
    icon: Brain,
    title: "Intelligent Orchestration",
    description: "Smart coordination of document workflows across clinical departments and systems.",
  },
  {
    icon: Lock,
    title: "Secure & Compliant",
    description: "HIPAA-compliant infrastructure with enterprise-grade security and audit logging.",
  },
]

function AnimatedIcon({ Icon, delay = 0 }: { Icon: any; delay?: number }) {
  const [isVisible, setIsVisible] = useState(false)
  const iconRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.3 },
    )

    if (iconRef.current) {
      observer.observe(iconRef.current)
    }

    return () => observer.disconnect()
  }, [])

  return (
    <div ref={iconRef} className="relative">
      <Icon
        className={`text-foreground h-16 w-16 ${isVisible ? "animate-draw-icon" : ""}`}
        strokeWidth={1}
        style={{
          strokeDasharray: isVisible ? undefined : 1000,
          strokeDashoffset: isVisible ? undefined : 1000,
        }}
      />
    </div>
  )
}

export function ServicesSection() {
  const [isVisible, setIsVisible] = useState(false)
  const sectionRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.2 },
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => observer.disconnect()
  }, [])

  return (
    <section
      ref={sectionRef}
      id="how-it-works"
      className="py-24 px-6 bg-background relative overflow-hidden"
    >
      <div className="max-w-7xl mx-auto">
        <div
          className={`text-center mb-20 transition-all duration-1000 ${
            isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-serif font-normal mb-6">
            How it works
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Streamline your clinical documentation with intelligent automation
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 lg:gap-8">
          {services.map((service, index) => (
            <div
              key={index}
              className={`group transition-all duration-1000 ${
                isVisible
                  ? "opacity-100 translate-y-0"
                  : "opacity-0 translate-y-8"
              }`}
              style={{
                transitionDelay: isVisible ? `${(index + 1) * 150}ms` : "0ms",
              }}
            >
              <div className="flex flex-col gap-6 p-8 rounded-2xl border border-border bg-card hover:bg-background transition-colors">
                <AnimatedIcon Icon={service.icon} delay={index * 0.1} />
                <div>
                  <h3 className="text-xl font-serif font-normal mb-3">
                    {service.title}
                  </h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {service.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
