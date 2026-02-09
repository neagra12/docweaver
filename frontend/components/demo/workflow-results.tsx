"use client"

import { CheckCircle2, Clock, FileText, Activity, Users, ClipboardList } from "lucide-react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import type { CompleteWorkflowResponse, DocumentationResponse, CoordinationResponse } from "@/lib/api"

interface WorkflowResultsProps {
  workflowResults?: CompleteWorkflowResponse | null
  documentationResults?: DocumentationResponse | null
  coordinationResults?: CoordinationResponse | null
}

export function WorkflowResults({ workflowResults, documentationResults, coordinationResults }: WorkflowResultsProps) {
  if (!workflowResults && !documentationResults && !coordinationResults) {
    return null
  }

  return (
    <div className="space-y-6">
      {/* Success Banner */}
      <div className="bg-green-50 border-2 border-green-200 rounded-xl p-6">
        <div className="flex items-center gap-3">
          <CheckCircle2 className="w-8 h-8 text-green-600 flex-shrink-0" />
          <div>
            <h3 className="font-semibold text-green-900 text-lg">Processing Complete!</h3>
            <p className="text-green-700 text-sm">
              Your documents have been successfully analyzed by our AI agents.
            </p>
          </div>
        </div>
      </div>

      {/* Complete Workflow Results */}
      {workflowResults && (
        <div className="space-y-6">
          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-muted rounded-xl p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <FileText className="w-4 h-4" />
                <span className="text-xs font-medium">Documents</span>
              </div>
              <p className="text-2xl font-bold">{workflowResults.summary.documents_processed}</p>
            </div>
            <div className="bg-muted rounded-xl p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <Activity className="w-4 h-4" />
                <span className="text-xs font-medium">API Calls</span>
              </div>
              <p className="text-2xl font-bold">{workflowResults.summary.total_api_calls}</p>
            </div>
            <div className="bg-muted rounded-xl p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <Clock className="w-4 h-4" />
                <span className="text-xs font-medium">Time</span>
              </div>
              <p className="text-2xl font-bold">
                {workflowResults.summary.processing_time_seconds.toFixed(1)}s
              </p>
            </div>
            <div className="bg-muted rounded-xl p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <Users className="w-4 h-4" />
                <span className="text-xs font-medium">Actions</span>
              </div>
              <p className="text-2xl font-bold">{workflowResults.summary.actions_automated}</p>
            </div>
          </div>

          {/* Summary Card */}
          <div className="bg-card border border-border rounded-xl p-6">
            <h4 className="font-semibold text-lg mb-4">Workflow Summary</h4>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between py-2 border-b border-border">
                <span className="text-muted-foreground">Total API Calls:</span>
                <span className="font-semibold">{workflowResults.total_api_calls}</span>
              </div>
              <div className="flex justify-between py-2 border-b border-border">
                <span className="text-muted-foreground">Processing Time:</span>
                <span className="font-semibold">
                  {workflowResults.processing_time_seconds.toFixed(2)} seconds
                </span>
              </div>
              <div className="flex justify-between py-2 border-b border-border">
                <span className="text-muted-foreground">Documents Processed:</span>
                <span className="font-semibold">{workflowResults.summary.documents_processed}</span>
              </div>
              <div className="flex justify-between py-2">
                <span className="text-muted-foreground">Actions Automated:</span>
                <span className="font-semibold">{workflowResults.summary.actions_automated}</span>
              </div>
            </div>
          </div>

          {/* Message */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-900">
              <strong>💡 Complete Results:</strong> {workflowResults.message}
              <br />
              <span className="text-xs mt-2 block">
                For detailed analysis including temporal trends, causal relationships, and full clinical documentation,
                check the Streamlit demo or API response.
              </span>
            </p>
          </div>
        </div>
      )}

      {/* Documentation Results */}
      {documentationResults && (
        <div className="space-y-6">
          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="bg-muted rounded-xl p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <FileText className="w-4 h-4" />
                <span className="text-xs font-medium">SOAP Note</span>
              </div>
              <p className="text-2xl font-bold">✓</p>
            </div>
            <div className="bg-muted rounded-xl p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <Activity className="w-4 h-4" />
                <span className="text-xs font-medium">ICD-10 Codes</span>
              </div>
              <p className="text-2xl font-bold">{documentationResults.icd10_codes?.length || 0}</p>
            </div>
            <div className="bg-muted rounded-xl p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <Activity className="w-4 h-4" />
                <span className="text-xs font-medium">API Calls</span>
              </div>
              <p className="text-2xl font-bold">{documentationResults.api_calls_used}</p>
            </div>
          </div>

          {/* SOAP Note */}
          {documentationResults.soap_note && (
            <div className="bg-card border border-border rounded-xl p-8 shadow-sm">
              <div className="flex items-center gap-2 mb-6 border-b border-border pb-4">
                <ClipboardList className="w-6 h-6 text-blue-600" />
                <h4 className="font-bold text-xl">Generated SOAP Note</h4>
              </div>
              <div className="prose prose-sm max-w-none">
                <div className="prose prose-sm max-w-none prose-slate dark:prose-invert">
                  <div className="bg-muted/50 p-6 rounded-lg border border-border">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {documentationResults.soap_note}
                    </ReactMarkdown>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Billing Codes */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* ICD-10 Codes */}
            {documentationResults.icd10_codes && documentationResults.icd10_codes.length > 0 && (
              <div className="bg-card border border-border rounded-xl p-6">
                <h4 className="font-semibold mb-3">ICD-10 Codes</h4>
                <div className="space-y-2">
                  {documentationResults.icd10_codes.map((code, index) => (
                    <div
                      key={index}
                      className="bg-muted px-3 py-2 rounded-lg text-sm font-mono"
                    >
                      {code}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* CPT Codes */}
            {documentationResults.cpt_codes && documentationResults.cpt_codes.length > 0 && (
              <div className="bg-card border border-border rounded-xl p-6">
                <h4 className="font-semibold mb-3">CPT Codes</h4>
                <div className="space-y-2">
                  {documentationResults.cpt_codes.map((code, index) => (
                    <div
                      key={index}
                      className="bg-muted px-3 py-2 rounded-lg text-sm font-mono"
                    >
                      {code}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Message */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-sm text-green-900">
              <strong>✅ Success:</strong> {documentationResults.message}
            </p>
          </div>
        </div>
      )}

      {/* Care Coordination Results */}
      {coordinationResults && (
        <div className="space-y-6">
          {/* Handover Report - NEW FEATURE */}
          {coordinationResults.handover_report && (
            <div className="bg-card border-2 border-primary/20 rounded-xl p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <Users className="w-5 h-5 text-primary" />
                <h4 className="font-bold text-xl">Clinical Handover Report</h4>
              </div>
              <p className="text-xs text-muted-foreground mb-4 uppercase tracking-wider font-semibold">
                Internal Physician Briefing
              </p>
              <div className="prose prose-sm max-w-none prose-slate dark:prose-invert prose-headings:mb-2 prose-p:leading-relaxed">
                <div className="bg-white dark:bg-slate-900 p-8 rounded-lg border border-primary/20 leading-relaxed font-sans shadow-md">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {coordinationResults.handover_report}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
          )}

          {/* Referral Letter */}
          {coordinationResults.referral_letter && coordinationResults.referral_letter !== "No referral needed" && (
            <div className="bg-card border border-border rounded-xl p-8 shadow-sm">
              <div className="flex items-center gap-2 mb-6 border-b border-border pb-4">
                <FileText className="w-6 h-6 text-purple-600" />
                <h4 className="font-bold text-xl">Specialist Referral Letter</h4>
              </div>
              <div className="prose prose-sm max-w-none prose-slate dark:prose-invert">
                <div className="bg-muted/50 p-6 rounded-lg border border-border">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {coordinationResults.referral_letter}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
          )}

          {/* Patient Education */}
          {coordinationResults.patient_education && coordinationResults.patient_education !== "No specific materials" && (
            <div className="bg-card border border-border rounded-xl p-8 shadow-sm">
              <div className="flex items-center gap-2 mb-6 border-b border-border pb-4">
                <Users className="w-6 h-6 text-green-600" />
                <h4 className="font-bold text-xl">Patient Education Materials</h4>
              </div>
              <div className="prose prose-sm max-w-none prose-green dark:prose-invert">
                <div className="bg-green-50/50 p-6 rounded-lg border border-green-100">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {coordinationResults.patient_education}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
          )}

          {/* Follow-up Plan */}
          {coordinationResults.follow_up_plan && coordinationResults.follow_up_plan !== "Routine follow-up" && (
            <div className="bg-card border border-border rounded-xl p-8 shadow-sm">
              <div className="flex items-center gap-2 mb-4 border-b border-border pb-4">
                <Clock className="w-6 h-6 text-orange-600" />
                <h4 className="font-bold text-xl">Follow-up Plan</h4>
              </div>
              <p className="text-sm leading-relaxed text-muted-foreground bg-orange-50/30 p-4 rounded-lg border border-orange-100">
                {coordinationResults.follow_up_plan}
              </p>
            </div>
          )}

          {/* Message */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-sm text-green-900">
              <strong>✅ Coordination Complete:</strong> {coordinationResults.message}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
