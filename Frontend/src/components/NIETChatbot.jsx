"use client"

import { useState } from "react"
import NIETChatbotMessages from "./NIETChatbotMessages"

export default function NIETChatbot() {
  const [open, setOpen] = useState(false)

  return (
    <>
      {!open && (
        <div className="fixed bottom-6 right-6 z-[100]">
          <button
            onClick={() => setOpen(true)}
            className="starky-dock-btn flex items-center justify-center group"
            aria-label="Open Chat"
            title="Open Chat"
          >
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2.5}
                d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
              />
            </svg>
          </button>
        </div>
      )}

      {open && (
        <div className="fixed inset-0 z-[90] pointer-events-none flex flex-col items-end justify-end p-3 sm:p-6">
          <div className="relative pointer-events-auto w-full sm:w-[400px] md:w-[480px] lg:w-[560px] h-full sm:h-[min(720px,calc(100vh-80px))] md:h-[min(820px,calc(100vh-60px))] lg:h-[min(900px,calc(100vh-40px))] bg-white flex flex-col rounded-3xl transform-gpu shadow-[0_25px_50px_rgba(0,0,0,0.25)] overflow-hidden border border-slate-100/50 backdrop-blur-sm">
            {/* Desktop Close Button */}
            <button
              onClick={() => setOpen(false)}
              className="absolute -top-3 -right-3 z-[101] w-9 h-9 rounded-full bg-[#e2111f] items-center justify-center transition-all duration-300 hover:scale-110 active:scale-95 hidden sm:flex border-2 border-white shadow-lg"
              aria-label="Close Chat"
            >
              <svg className="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            {/* Mobile Close Button */}
            <button
              onClick={() => setOpen(false)}
              className="absolute -top-3 -right-3 z-[101] w-8 h-8 rounded-full bg-[#e2111f] items-center justify-center shadow-lg transition-all duration-300 active:scale-95 flex sm:hidden border-2 border-white"
              aria-label="Close Chat"
            >
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>

            <div className="flex-1 flex flex-col overflow-hidden">
              <NIETChatbotMessages />
            </div>
          </div>
        </div>
      )}
    </>
  )
}