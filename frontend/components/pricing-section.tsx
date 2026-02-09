"use client"

import { Check } from "lucide-react"
import { useState } from "react"

const plans = [
  {
    name: "Starter",
    price: "$99",
    period: "per month",
    description: "Perfect for small clinics",
    features: [
      "Up to 1,000 documents/month",
      "Email support",
      "Basic analytics",
      "Single user",
    ],
    highlighted: false,
  },
  {
    name: "Professional",
    price: "$299",
    period: "per month",
    description: "For growing healthcare teams",
    features: [
      "Up to 10,000 documents/month",
      "Priority support",
      "Advanced analytics",
      "Up to 10 users",
      "API access",
    ],
    highlighted: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "contact us",
    description: "For large healthcare systems",
    features: [
      "Unlimited documents",
      "24/7 dedicated support",
      "Custom integrations",
      "Unlimited users",
      "SLA guarantee",
    ],
    highlighted: false,
  },
]

export function PricingSection() {
  const [annual, setAnnual] = useState(false)

  return (
    <section id="pricing" className="py-32 px-6 relative">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-serif font-normal mb-6">
            Simple, transparent pricing
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
            Choose the plan that fits your healthcare organization
          </p>
          <div className="flex items-center justify-center gap-4">
            <span
              className={`text-sm ${!annual ? "font-medium text-foreground" : "text-muted-foreground"}`}
            >
              Monthly
            </span>
            <button
              onClick={() => setAnnual(!annual)}
              className={`relative w-12 h-6 rounded-full transition-colors ${
                annual ? "bg-foreground" : "bg-border"
              }`}
            >
              <span
                className={`absolute top-1 left-1 w-4 h-4 bg-background rounded-full transition-transform ${
                  annual ? "translate-x-6" : ""
                }`}
              />
            </button>
            <span
              className={`text-sm ${annual ? "font-medium text-foreground" : "text-muted-foreground"}`}
            >
              Annually
              <span className="ml-2 text-xs text-green-600">Save 20%</span>
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 lg:gap-6">
          {plans.map((plan, i) => (
            <div
              key={i}
              className={`rounded-2xl border transition-all ${
                plan.highlighted
                  ? "border-foreground bg-foreground text-background scale-105"
                  : "border-border bg-card hover:border-foreground/30"
              } p-8`}
            >
              <h3 className="text-2xl font-serif font-normal mb-2">
                {plan.name}
              </h3>
              <p className={`text-sm mb-6 ${plan.highlighted ? "text-background/70" : "text-muted-foreground"}`}>
                {plan.description}
              </p>

              <div className="mb-6">
                <span className="text-4xl font-light">{plan.price}</span>
                <span className={`text-sm ${plan.highlighted ? "text-background/70" : "text-muted-foreground"}`}>
                  {" "}
                  {plan.period}
                </span>
              </div>

              <button
                className={`w-full py-3 rounded-lg mb-8 font-medium transition-colors ${
                  plan.highlighted
                    ? "bg-background text-foreground hover:bg-background/90"
                    : "border border-border bg-transparent hover:bg-muted"
                }`}
              >
                Get started
              </button>

              <ul className="space-y-3">
                {plan.features.map((feature, j) => (
                  <li key={j} className="flex items-start gap-3">
                    <Check className="w-5 h-5 flex-shrink-0 mt-0.5" />
                    <span className="text-sm">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
