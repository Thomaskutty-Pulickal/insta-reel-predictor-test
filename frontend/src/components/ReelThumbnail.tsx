interface ReelThumbnailProps {
  emoji: string
  color: string
  className?: string
}

/** No real video/thumbnail assets exist in this demo - every reel renders
 * as a category-colored gradient block with its emoji, generated purely
 * from data the backend already sends. */
export function ReelThumbnail({ emoji, color, className = '' }: ReelThumbnailProps) {
  return (
    <div
      className={`flex items-center justify-center ${className}`}
      style={{
        background: `linear-gradient(135deg, ${color}66, ${color}1a)`,
        borderBottom: `1px solid ${color}55`,
      }}
    >
      <span style={{ fontSize: '3.5rem' }}>{emoji}</span>
    </div>
  )
}
