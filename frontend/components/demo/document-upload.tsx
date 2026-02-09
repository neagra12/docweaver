"use client"

import { useCallback, useState } from "react"
import { Upload, X, FileText, Loader2 } from "lucide-react"

interface DocumentUploadProps {
  onUpload: (files: File[]) => void
  isProcessing: boolean
}

export function DocumentUpload({ onUpload, isProcessing }: DocumentUploadProps) {
  const [dragActive, setDragActive] = useState(false)
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const files = Array.from(e.dataTransfer.files).filter(
        (file) => 
          file.type === "application/pdf" ||
          file.type === "text/plain" ||
          file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      )
      setSelectedFiles((prev) => [...prev, ...files])
    }
  }, [])

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const files = Array.from(e.target.files)
      setSelectedFiles((prev) => [...prev, ...files])
    }
  }, [])

  const removeFile = (index: number) => {
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleSubmit = () => {
    if (selectedFiles.length > 0) {
      onUpload(selectedFiles)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + " " + sizes[i]
  }

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div
        className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all ${
          dragActive
            ? "border-foreground bg-muted/50"
            : "border-border hover:border-foreground/50"
        } ${isProcessing ? "opacity-50 pointer-events-none" : ""}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-upload"
          className="hidden"
          onChange={handleFileSelect}
          multiple
          accept=".pdf,.txt,.docx"
          disabled={isProcessing}
        />
        
        <div className="space-y-4">
          <div className="w-16 h-16 mx-auto bg-muted rounded-full flex items-center justify-center">
            <Upload className="w-8 h-8 text-muted-foreground" />
          </div>
          
          <div>
            <label
              htmlFor="file-upload"
              className="text-foreground font-medium cursor-pointer hover:underline"
            >
              Click to upload
            </label>
            <span className="text-muted-foreground"> or drag and drop</span>
          </div>
          
          <p className="text-sm text-muted-foreground">
            PDF, TXT, or DOCX files (up to 10MB each)
          </p>
        </div>
      </div>

      {/* Selected Files */}
      {selectedFiles.length > 0 && (
        <div className="space-y-3">
          <h4 className="font-semibold text-sm">Selected Files ({selectedFiles.length})</h4>
          <div className="space-y-2">
            {selectedFiles.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-muted rounded-lg"
              >
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <FileText className="w-5 h-5 text-muted-foreground flex-shrink-0" />
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium truncate">{file.name}</p>
                    <p className="text-xs text-muted-foreground">{formatFileSize(file.size)}</p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="ml-2 p-1 hover:bg-background rounded transition-colors flex-shrink-0"
                  disabled={isProcessing}
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={selectedFiles.length === 0 || isProcessing}
        className="w-full bg-foreground text-background rounded-full py-3 px-6 font-semibold transition-all hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
      >
        {isProcessing ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            Processing Documents...
          </>
        ) : (
          <>
            <Upload className="w-5 h-5" />
            Process {selectedFiles.length} {selectedFiles.length === 1 ? "Document" : "Documents"}
          </>
        )}
      </button>

      {/* Demo Files Suggestion */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-900">
          <strong>💡 Tip:</strong> Try uploading the demo files from{" "}
          <code className="bg-blue-100 px-2 py-0.5 rounded text-xs">
            clinical_orchestrator/demo_data/
          </code>{" "}
          to see Sarah Chen's complete clinical workflow in action.
        </p>
      </div>
    </div>
  )
}
