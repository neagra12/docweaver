"use client"

import { useState, useEffect, useRef } from "react"

const testimonials = [
  {
    name: "Dr. Sarah Chen",
    role: "Chief of Cardiology",
    content: "DocWeaver has transformed how we manage clinical documentation. Our efficiency improved by 40%.",
    avatar: "/placeholder.svg?height=48&width=48",
  },
  {
    name: "Dr. Michael Rodriguez",
    role: "Hospital Administrator",
    content: "The AI-powered insights help us identify patterns we never could before. Invaluable tool.",
    avatar: "/placeholder.svg?height=48&width=48",
  },
  {
    name: "Dr. Emily Watson",
    role: "Emergency Department Director",
    content: "Streamlined our ER workflows significantly. Staff loves how intuitive the interface is.",
    avatar: "/placeholder.svg?height=48&width=48",
  },
]

const testimonials2 = [
  {
    name: "Dr. James Patterson",
    role: "Clinical Director",
    content: "The compliance features give us peace of mind. HIPAA-ready and audit-proof.",
    avatar: "/placeholder.svg?height=48&width=48",
  },
  {
    name: "Dr. Lisa Thompson",
    role: "Lab Director",
    content: "Integration with our existing systems was seamless. Best decision we made this year.",
    avatar: "/placeholder.svg?height=48&width=48",
  },
  {
    name: "Dr. David Kumar",
    role: "Chief Medical Officer",
    content: "Real-time analytics drive better clinical decisions. Highly recommend to any healthcare facility.",
    avatar: "/placeholder.svg?height=48&width=48",
  },
]

const duplicatedTestimonials = [...testimonials, ...testimonials, ...testimonials]
const duplicatedTestimonials2 = [...testimonials2, ...testimonials2, ...testimonials2]

export function TestimonialsSection() {
  const [isPaused, setIsPaused] = useState(false)
  const [isInitialized, setIsInitialized] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)
  const scrollRef2 = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const timer = setTimeout(() => {
      if (scrollRef2.current) {
        scrollRef2.current.scrollLeft = scrollRef2.current.scrollWidth / 3
      }
      setIsInitialized(true)
    }, 100)
    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    if (isPaused || !isInitialized || !scrollRef.current) return

    const scrollContainer = scrollRef.current
    let animationFrameId: number
    let isActive = true

    const scroll = () => {
      if (!isActive || !scrollContainer) return

      scrollContainer.scrollLeft += 1
      const maxScroll = scrollContainer.scrollWidth / 3

      if (scrollContainer.scrollLeft >= maxScroll) {
        scrollContainer.scrollLeft = 0
      }

      animationFrameId = requestAnimationFrame(scroll)
    }

    animationFrameId = requestAnimationFrame(scroll)

    return () => {
      isActive = false
      cancelAnimationFrame(animationFrameId)
    }
  }, [isPaused, isInitialized])

  useEffect(() => {
    if (isPaused || !isInitialized || !scrollRef2.current) return

    const scrollContainer = scrollRef2.current
    let animationFrameId: number
    let isActive = true

    const scrollReverse = () => {
      if (!isActive || !scrollContainer) return

      scrollContainer.scrollLeft -= 1

      if (scrollContainer.scrollLeft <= 0) {
        scrollContainer.scrollLeft = scrollContainer.scrollWidth / 3
      }

      animationFrameId = requestAnimationFrame(scrollReverse)
    }

    animationFrameId = requestAnimationFrame(scrollReverse)

    return () => {
      isActive = false
      cancelAnimationFrame(animationFrameId)
    }
  }, [isPaused, isInitialized])

  return (
    <section id="testimonials" className="py-32 px-6 relative overflow-hidden">
      <div className="max-w-7xl mx-auto mb-16 text-center">
        <h2 className="text-4xl md:text-5xl lg:text-6xl font-serif font-normal mb-6">
          Trusted by healthcare leaders
        </h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          See what healthcare professionals say about DocWeaver
        </p>
      </div>

      <div className="space-y-8">
        <div
          className="flex gap-6 overflow-x-auto scroll-smooth pb-4"
          ref={scrollRef}
          onMouseEnter={() => setIsPaused(true)}
          onMouseLeave={() => setIsPaused(false)}
        >
          {duplicatedTestimonials.map((testimonial, i) => (
            <div
              key={i}
              className="flex-shrink-0 w-80 rounded-2xl border border-border bg-card p-6"
            >
              <p className="text-foreground mb-6 leading-relaxed">
                "{testimonial.content}"
              </p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-muted" />
                <div>
                  <p className="font-medium text-sm text-foreground">
                    {testimonial.name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {testimonial.role}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div
          className="flex gap-6 overflow-x-auto scroll-smooth pb-4"
          ref={scrollRef2}
          onMouseEnter={() => setIsPaused(true)}
          onMouseLeave={() => setIsPaused(false)}
        >
          {duplicatedTestimonials2.map((testimonial, i) => (
            <div
              key={i}
              className="flex-shrink-0 w-80 rounded-2xl border border-border bg-card p-6"
            >
              <p className="text-foreground mb-6 leading-relaxed">
                "{testimonial.content}"
              </p>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-muted" />
                <div>
                  <p className="font-medium text-sm text-foreground">
                    {testimonial.name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {testimonial.role}
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
