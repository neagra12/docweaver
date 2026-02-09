"use client"

import { useState } from "react"
import { Loader2, UserCog, Stethoscope } from "lucide-react"

interface CareCoordinationFormProps {
  onSubmit: (patientSummary: string, coordinationNeeds?: string) => void
  isProcessing: boolean
}

export function CareCoordinationForm({ onSubmit, isProcessing }: CareCoordinationFormProps) {
  const [patientSummary, setPatientSummary] = useState("")
  const [coordinationNeeds, setCoordinationNeeds] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (patientSummary.trim()) {
      onSubmit(patientSummary, coordinationNeeds)
    }
  }

  const loadExample = () => {
    setPatientSummary(
      "52F DM2 with new onset microalbuminuria. A1C 6.8%. BP 138/82. " +
      "Needs ophthalmology referral for annual screening. " +
      "Start lisinopril 10mg daily. Follow-up in 3 months."
    )
    setCoordinationNeeds("Ophthalmology referral, medication education, diet plan")
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Patient Summary */}
      <div className="space-y-2">
        <label htmlFor="patient-summary" className="block text-sm font-semibold">
          Patient Summary
        </label>
        <textarea
          id="patient-summary"
          value={patientSummary}
          onChange={(e) => setPatientSummary(e.target.value)}
          placeholder="Enter patient summary or clinical context..."
          className="w-full min-h-[150px] p-4 border-2 border-border rounded-xl focus:border-foreground focus:outline-none transition-colors resize-none"
          disabled={isProcessing}
        />
      </div>

      {/* Specific Needs (Optional) */}
      <div className="space-y-2">
        <label htmlFor="coordination-needs" className="block text-sm font-semibold">
          Specific Coordination Needs (Optional)
        </label>
        <input
          id="coordination-needs"
          type="text"
          value={coordinationNeeds}
          onChange={(e) => setCoordinationNeeds(e.target.value)}
          placeholder="e.g., Cardiology referral, Diabetes education"
          className="w-full p-4 border-2 border-border rounded-xl focus:border-foreground focus:outline-none transition-colors"
          disabled={isProcessing}
        />
      </div>

      {/* Action Buttons */}
      <div className="flex justify-between items-center text-sm text-muted-foreground">
        <span>{patientSummary.length} characters</span>
        <button
          type="button"
          onClick={loadExample}
          className="text-foreground hover:underline font-medium"
          disabled={isProcessing}
        >
          Load Example
        </button>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={!patientSummary.trim() || isProcessing}
        className="w-full bg-foreground text-background rounded-full py-3 px-6 font-semibold transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
      >
        {isProcessing ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Coordinating Care...
          </>
        ) : (
          <>
            <UserCog className="w-5 h-5" />
            Generate Care Plan
          </>
        )}
      </button>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-900">
          <strong>🧠 Intelligent Coordination:</strong> Generate referral letters, patient education materials, 
          and follow-up plans automatically based on clinical context.
        </p>
      </div>
    </form>
  )
}
