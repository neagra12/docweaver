"use client"

import { useState, useEffect } from "react"

export function useToast() {
  return {
    toast: (options: { title?: string; description?: string }) => {
      console.log("Toast:", options)
    },
  }
}
