import { type CSSProperties, useEffect, useState } from 'react'
import type { MetricWeightKey, MetricWeights } from '../types/games'

type MetricWeightsModalProps = {
  weights: MetricWeights
  error: string | null
  onCancel: () => void
  onDone: () => void
  onWeightChange: (metricKey: MetricWeightKey, value: number) => void
}

const metricRows: { key: MetricWeightKey; label: string }[] = [
  { key: 'total_goals', label: 'Total Goals' },
  { key: 'final_goal_diff', label: 'Final Goal Differential' },
  { key: 'lead_changes', label: 'Lead Changes' },
  { key: 'max_lead', label: 'Max Lead' },
  { key: 'max_time_between_goals', label: 'Max Time Between Goals' },
]

export const defaultMetricWeights: MetricWeights = {
  total_goals: 20,
  final_goal_diff: 20,
  lead_changes: 20,
  max_lead: 20,
  max_time_between_goals: 20,
}

export function MetricWeightsModal({
  weights,
  error,
  onCancel,
  onDone,
  onWeightChange,
}: MetricWeightsModalProps) {
  const [showIncompleteWarning, setShowIncompleteWarning] = useState(false)
  const totalWeight = Object.values(weights).reduce(
    (sum, weight) => sum + weight,
    0,
  )

  useEffect(() => {
    if (!showIncompleteWarning) {
      return
    }

    const timeoutId = window.setTimeout(() => {
      setShowIncompleteWarning(false)
    }, 3200)

    return () => window.clearTimeout(timeoutId)
  }, [showIncompleteWarning])

  function handleWeightChange(metricKey: MetricWeightKey, value: number) {
    const currentWeight = weights[metricKey]
    const totalWithoutCurrent = totalWeight - currentWeight
    const maxAllowedWeight = 100 - totalWithoutCurrent
    const nextWeight = Math.min(value, maxAllowedWeight)

    onWeightChange(metricKey, nextWeight)
  }

  function handleDone() {
    if (totalWeight < 100) {
      setShowIncompleteWarning(true)
      return
    }

    onDone()
  }

  return (
    <div className="modal-backdrop" role="presentation" onClick={onCancel}>
      <div
        className="modal metric-weights-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="metric-weights-modal-title"
        onClick={(event) => event.stopPropagation()}
      >
        <h2 id="metric-weights-modal-title">Metric Weights</h2>
        <div className="metric-weights-summary">
          <span>Total: {totalWeight}%</span>
          {totalWeight < 100 && (
            <strong>{100 - totalWeight}% unassigned</strong>
          )}
        </div>
        <div className="metric-weights-list">
          {metricRows.map((metric) => (
            <label className="metric-weight-row" key={metric.key}>
              <span className="metric-weight-label">{metric.label}</span>
              <input
                className={
                  weights[metric.key] === 100 ? 'metric-weight-slider-max' : ''
                }
                type="range"
                min="0"
                max="100"
                step="1"
                value={weights[metric.key]}
                style={
                  {
                    '--slider-value': `${weights[metric.key]}%`,
                  } as CSSProperties
                }
                onChange={(event) =>
                  handleWeightChange(metric.key, Number(event.target.value))
                }
              />
              <span className="metric-weight-value">
                {weights[metric.key]}%
              </span>
            </label>
          ))}
        </div>
        {showIncompleteWarning && (
          <div className="metric-weights-warning" role="alert">
            Weights currently sum to less than 100%.
          </div>
        )}
        {error !== null && (
          <div className="metric-weights-error" role="alert">
            {error}
          </div>
        )}
        <div className="modal-actions">
          <button
            type="button"
            className="modal-cancel-button"
            onClick={onCancel}
          >
            Cancel
          </button>
          <button
            type="button"
            className="modal-confirm-button"
            onClick={handleDone}
          >
            Done
          </button>
        </div>
      </div>
    </div>
  )
}
