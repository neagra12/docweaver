"use client"

import { useState } from "react"
import { ChevronDown } from "lucide-react"

const faqs = [
  {
    question: "How long does it take to process documents?",
    answer:
      "Most documents are processed within seconds. Our AI analyzes clinical documents in real-time, extracting key information and insights instantly. Batch processing for large volumes can be configured.",
  },
  {
    question: "What file formats are supported?",
    answer:
      "We support PDF, DOCX, TXT, and image files (JPG, PNG, TIFF). All formats are automatically converted and analyzed by our advanced OCR and NLP engines.",
  },
  {
    question: "Is DocWeaver HIPAA compliant?",
    answer:
      "Yes, DocWeaver is fully HIPAA compliant with end-to-end encryption, secure data centers, and comprehensive audit logging. We maintain SOC 2 Type II certification.",
  },
  {
    question: "Can we integrate with our existing EHR system?",
    answer:
      "Absolutely. We offer API integrations with major EHR systems including Epic, Cerner, and other HL7-compatible platforms. Our team can assist with custom integrations.",
  },
  {
    question: "What happens to our data if we cancel?",
    answer:
      "All your data is yours. Upon request, we provide complete data export in standard formats. We maintain data for 30 days after cancellation for compliance purposes.",
  },
  {
    question: "Do you offer training and support?",
    answer:
      "Yes, we provide comprehensive onboarding, training, documentation, and 24/7 support for enterprise customers. Standard plans include email support and extensive knowledge base access.",
  },
]

export function FAQSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(null)

  return (
    <section id="faq" className="py-24 px-6 pb-32">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-normal mb-6 text-balance font-serif">
            Frequently asked questions
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Everything you need to know about DocWeaver. Have a question not listed? Contact our support team.
          </p>
        </div>

        <div className="space-y-3">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className="bg-card border border-border rounded-xl overflow-hidden transition-all"
            >
              <button
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                className="w-full flex items-center justify-between px-6 py-5 hover:bg-muted/50 transition-colors"
              >
                <h3 className="text-base font-medium text-foreground text-left">
                  {faq.question}
                </h3>
                <ChevronDown
                  className={`w-5 h-5 text-muted-foreground flex-shrink-0 transition-transform ${
                    openIndex === index ? "rotate-180" : ""
                  }`}
                />
              </button>
              {openIndex === index && (
                <div className="px-6 pb-5 border-t border-border">
                  <p className="text-muted-foreground leading-relaxed text-sm">
                    {faq.answer}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
