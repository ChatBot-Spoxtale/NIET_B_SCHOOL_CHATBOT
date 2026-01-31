"use client"

import { useState, useEffect } from "react"
import NIETChatbotMessages from "./NIETChatbotMessages"

export default function NIETChatbot() {
  const [isIframe, setIsIframe] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const iframe = window.self !== window.top
    setIsIframe(iframe)
    if (iframe) setOpen(true)
  }, [])

  return (
    <>
      {/* Launcher ONLY on main site */}
      {!isIframe && !open && (
        <button
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 z-[100] w-14 h-14 rounded-2xl
                     bg-gradient-to-br from-[#e2111f] to-[#b00d18]
                     flex items-center justify-center shadow-lg
                     transition-all hover:scale-110"
        >
          💬
        </button>
      )}

      {/* Chat window */}
      {open && (
        <div className="fixed inset-0 z-[90] flex items-end justify-end p-2 sm:p-6">
          <div className="relative w-full sm:w-[380px] h-full sm:h-[520px]
                          bg-white rounded-[32px] shadow-xl overflow-hidden">

            {/* Close button ONLY outside iframe */}
            {!isIframe && (
              <button
                onClick={() => setOpen(false)}
                className="absolute -top-3 -right-3 z-[101]
                           w-7 h-7 rounded-full bg-[#e2111f] text-white"
              >
                ✕
              </button>
            )}

            <NIETChatbotMessages embed={isIframe} />
          </div>
        </div>
      )}
    </>
  )
}
