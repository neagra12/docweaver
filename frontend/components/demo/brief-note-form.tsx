"use client"

import { useState } from "react"
import { Loader2, FileText } from "lucide-react"

interface BriefNoteFormProps {
  onSubmit: (briefNote: string) => void
  isProcessing: boolean
}

export function BriefNoteForm({ onSubmit, isProcessing }: BriefNoteFormProps) {
  const [briefNote, setBriefNote] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (briefNote.trim()) {
      onSubmit(briefNote)
    }
  }

  const loadExample = () => {
    setBriefNote(
      "52F DM2 f/u. A1C 6.8% (up from 6.5%). Microalbuminuria detected. BP 138/82. " +
      "Reports good medication compliance. LDL 95. Discussed diet, exercise. " +
      "Needs ophthalmology eval for diabetic retinopathy screening. RTC 3mo."
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Text Area */}
      <div className="space-y-2">
        <label htmlFor="brief-note" className="block text-sm font-semibold">
          Brief Clinical Note
        </label>
        <textarea
          id="brief-note"
          value={briefNote}
          onChange={(e) => setBriefNote(e.target.value)}
          placeholder="Enter a brief clinical note here..."
          className="w-full min-h-[200px] p-4 border-2 border-border rounded-xl focus:border-foreground focus:outline-none transition-colors resize-none"
          disabled={isProcessing}
        />
        <p className="text-xs text-muted-foreground">
          Enter a concise clinical note. Our AI will expand it into a complete SOAP note with codes.
        </p>
      </div>

      {/* Character Count */}
      <div className="flex justify-between items-center text-sm text-muted-foreground">
        <span>{briefNote.length} characters</span>
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
        disabled={!briefNote.trim() || isProcessing}
        className="w-full bg-foreground text-background rounded-full py-3 px-6 font-semibold transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
      >
        {isProcessing ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Generating Documentation...
          </>
        ) : (
          <>
            <FileText className="w-5 h-5" />
            Generate SOAP Note
          </>
        )}
      </button>

      {/* Info Box */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <p className="text-sm text-green-900">
          <strong>✨ What you'll get:</strong> Complete SOAP note with Subjective, Objective,
          Assessment, and Plan sections, plus ICD-10 codes and CPT codes automatically extracted.
        </p>
      </div>
    </form>
  )
}
