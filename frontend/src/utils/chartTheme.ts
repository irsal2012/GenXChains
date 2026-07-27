import { useUIStore } from '@/store/uiStore'

/**
 * Recharts styles its axes, legend and tooltip through props rather than CSS
 * classes, so Tailwind's `dark:` variants cannot reach them. Charts therefore
 * have to read the active theme themselves.
 *
 * Series colours are deliberately not themed: the saturated palette in use
 * (blue-600, green-600, amber-500, violet-600) holds contrast on both light
 * and dark surfaces, and recolouring it per theme would break the visual link
 * between a series and its legend entry elsewhere in the UI.
 */
export interface ChartTheme {
  /** CartesianGrid stroke. */
  grid: string
  /** Axis lines and tick labels. */
  axis: string
  /** Tooltip container style. */
  tooltipContent: React.CSSProperties
  /** Tooltip label (the x-value heading). */
  tooltipLabel: React.CSSProperties
  /** Legend wrapper style. */
  legend: React.CSSProperties
}

const LIGHT: ChartTheme = {
  grid: '#e5e7eb', // gray-200
  axis: '#6b7280', // gray-500
  tooltipContent: {
    backgroundColor: '#ffffff',
    border: '1px solid #e5e7eb',
    borderRadius: '0.5rem',
    color: '#111827',
  },
  tooltipLabel: { color: '#374151' },
  legend: { color: '#374151' },
}

const DARK: ChartTheme = {
  grid: '#374151', // gray-700
  axis: '#9ca3af', // gray-400
  tooltipContent: {
    backgroundColor: '#1f2937', // gray-800
    border: '1px solid #374151',
    borderRadius: '0.5rem',
    color: '#f3f4f6',
  },
  tooltipLabel: { color: '#d1d5db' },
  legend: { color: '#d1d5db' },
}

export function useChartTheme(): ChartTheme {
  const theme = useUIStore((s) => s.theme)
  return theme === 'dark' ? DARK : LIGHT
}
