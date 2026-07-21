import { AnimatePresence, motion } from 'framer-motion'
import type { Explanation } from '../types/recommendation'

interface ExplanationPanelProps {
  explanation: Explanation | undefined
}

export function ExplanationPanel({ explanation }: ExplanationPanelProps) {
  return (
    <div className="flex flex-col gap-3 rounded-2xl border border-neutral-800 bg-neutral-900 p-4">
      <h2 className="text-xs font-semibold uppercase tracking-wide text-neutral-500">
        Recommended because
      </h2>
      <AnimatePresence mode="wait">
        {!explanation ? (
          <p className="text-sm text-neutral-500">Waiting for a recommendation…</p>
        ) : (
          <motion.ul
            key={explanation.reasons.join('|')}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
            className="flex flex-col gap-2"
          >
            {explanation.reasons.map((reason) => (
              <li key={reason} className="flex items-start gap-2 text-sm text-neutral-200">
                <span className="mt-0.5 text-emerald-400">✓</span>
                <span>{reason}</span>
              </li>
            ))}
          </motion.ul>
        )}
      </AnimatePresence>
    </div>
  )
}
