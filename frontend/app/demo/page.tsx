"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { DocumentUpload } from "@/components/demo/document-upload"
import { WorkflowResults } from "@/components/demo/workflow-results"
import { BriefNoteForm } from "@/components/demo/brief-note-form"
import { CareCoordinationForm } from "@/components/demo/care-coordination-form"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { docWeaverAPI } from "@/lib/api"
import type { CompleteWorkflowResponse, DocumentationResponse, CoordinationResponse } from "@/lib/api"

export default function DemoPage() {
  const [isProcessing, setIsProcessing] = useState(false)
  const [workflowResults, setWorkflowResults] = useState<CompleteWorkflowResponse | null>(null)
  const [documentationResults, setDocumentationResults] = useState<DocumentationResponse | null>(null)
  const [coordinationResults, setCoordinationResults] = useState<CoordinationResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState("upload")

  const handleDocumentUpload = async (files: File[]) => {
    setIsProcessing(true)
    setError(null)
    setWorkflowResults(null)
    setDocumentationResults(null)
    setCoordinationResults(null)

    try {
      const result = await docWeaverAPI.completeWorkflow(files)
      setWorkflowResults(result)
      setActiveTab("results")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to process documents")
    } finally {
      setIsProcessing(false)
    }
  }

  const handleBriefNoteSubmit = async (briefNote: string) => {
    setIsProcessing(true)
    setError(null)
    setDocumentationResults(null)
    setWorkflowResults(null)
    setCoordinationResults(null)

    try {
      const result = await docWeaverAPI.generateDocumentation(briefNote)
      setDocumentationResults(result)
      setActiveTab("results")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate documentation")
    } finally {
      setIsProcessing(false)
    }
  }

  const handleCoordinationSubmit = async (patientSummary: string, coordinationNeeds?: string) => {
    setIsProcessing(true)
    setError(null)
    setDocumentationResults(null)
    setWorkflowResults(null)
    setCoordinationResults(null)

    try {
      const result = await docWeaverAPI.careCoordination(patientSummary, coordinationNeeds)
      setCoordinationResults(result)
      setActiveTab("results")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate care coordination")
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <main className="min-h-screen bg-background">
      <Header />

      <section className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Hero */}
          <div className="text-center mb-12">
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-serif font-normal mb-6">
              Try DocWeaver Live
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Experience our AI-powered clinical intelligence platform. Upload documents or generate SOAP notes in real-time.
            </p>
          </div>

          {/* Demo Interface */}
          <div className="bg-card border border-border rounded-2xl p-8 shadow-lg">
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-3 mb-8">
                <TabsTrigger value="upload">Complete Workflow</TabsTrigger>
                <TabsTrigger value="brief-note">Generate SOAP Note</TabsTrigger>
                <TabsTrigger value="coordination">Care Coordination</TabsTrigger>
              </TabsList>

              <TabsContent value="upload" className="space-y-6">
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-semibold mb-2">Complete Clinical Workflow</h3>
                  <p className="text-muted-foreground">
                    Upload multiple patient documents to see multi-source data fusion, temporal analysis, and automated coordination in action.
                  </p>
                </div>
                <DocumentUpload
                  onUpload={handleDocumentUpload}
                  isProcessing={isProcessing}
                />
              </TabsContent>

              <TabsContent value="brief-note" className="space-y-6">
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-semibold mb-2">Smart Documentation</h3>
                  <p className="text-muted-foreground">
                    Enter a brief clinical note and watch it transform into a complete SOAP note with codes.
                  </p>
                </div>
                <BriefNoteForm
                  onSubmit={handleBriefNoteSubmit}
                  isProcessing={isProcessing}
                />
              </TabsContent>

              <TabsContent value="coordination" className="space-y-6">
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-semibold mb-2">Care Coordination</h3>
                  <p className="text-muted-foreground">
                    Generate referrals, patient education materials, and follow-up plans automatically.
                  </p>
                </div>
                <CareCoordinationForm
                  onSubmit={handleCoordinationSubmit}
                  isProcessing={isProcessing}
                />
              </TabsContent>
            </Tabs>

            {/* Error Display */}
            {error && (
              <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-800 text-sm">
                  <strong>Error:</strong> {error}
                  <br />
                  <span className="text-xs mt-2 block">
                    Make sure the FastAPI backend is running on port 8000. Run: <code className="bg-red-100 px-2 py-1 rounded">python clinical_orchestrator/api.py</code>
                  </span>
                </p>
              </div>
            )}

            {/* Results Display */}
            {(workflowResults || documentationResults || coordinationResults) && (
              <div className="mt-8">
                <WorkflowResults
                  workflowResults={workflowResults}
                  documentationResults={documentationResults}
                  coordinationResults={coordinationResults}
                />
              </div>
            )}
          </div>

          {/* Info Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
            <div className="bg-card border border-border rounded-xl p-6">
              <div className="text-3xl mb-3">📊</div>
              <h4 className="font-semibold mb-2">Multi-Source Fusion</h4>
              <p className="text-sm text-muted-foreground">
                Process 5+ documents in parallel with temporal analysis and causal detection
              </p>
            </div>
            <div className="bg-card border border-border rounded-xl p-6">
              <div className="text-3xl mb-3">📝</div>
              <h4 className="font-semibold mb-2">Smart Documentation</h4>
              <p className="text-sm text-muted-foreground">
                Generate complete SOAP notes with automated ICD-10 and CPT coding
              </p>
            </div>
            <div className="bg-card border border-border rounded-xl p-6">
              <div className="text-3xl mb-3">🔗</div>
              <h4 className="font-semibold mb-2">Care Coordination</h4>
              <p className="text-sm text-muted-foreground">
                Automated referrals, follow-ups, and patient education materials
              </p>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </main>
  )
}
