import React, { useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './StepThrough.css';

interface PoseStep {
  pose: string;
  duration: number; // seconds
  description?: string;
}

interface GeneratedFlow {
  routine_name?: string;
  flow_sequence?: PoseStep[];
}

const StepThrough: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const flow = (location.state as { flow?: GeneratedFlow } | null)?.flow;

  const sequence: PoseStep[] = useMemo(() => {
    return Array.isArray(flow?.flow_sequence)
      ? (flow!.flow_sequence as PoseStep[]).map(step => ({
          pose: step.pose,
          duration: Number(step.duration) || 0,
          description: (step as any).description,
        }))
      : [];
  }, [flow]);

  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [remainingSeconds, setRemainingSeconds] = useState<number>(0);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [isComplete, setIsComplete] = useState<boolean>(false);

  useEffect(() => {
    if (!flow || sequence.length === 0) {
      navigate('/flow-generator', { replace: true });
      return;
    }
    setCurrentIndex(0);
    setRemainingSeconds(sequence[0]?.duration || 0);
    setIsPlaying(false);
    setIsComplete(false);
  }, [flow, sequence, navigate]);

  useEffect(() => {
    if (!isPlaying) return;
    if (isComplete) return;

    const tick = () => {
      setRemainingSeconds(prev => {
        if (prev > 1) return prev - 1;
        // Advance to next step
        setCurrentIndex(idx => {
          const nextIndex = idx + 1;
          if (nextIndex < sequence.length) {
            setRemainingSeconds(sequence[nextIndex].duration);
            return nextIndex;
          } else {
            setIsPlaying(false);
            setIsComplete(true);
            return idx; // stay on last index
          }
        });
        return 0;
      });
    };

    const intervalId = window.setInterval(tick, 1000);
    return () => window.clearInterval(intervalId);
  }, [isPlaying, isComplete, sequence]);

  const handlePlay = () => {
    if (sequence.length === 0) return;
    if (isComplete) return;
    setIsPlaying(true);
  };

  const handlePause = () => {
    setIsPlaying(false);
  };

  const handleReset = () => {
    if (sequence.length === 0) return;
    setIsPlaying(false);
    setIsComplete(false);
    setCurrentIndex(0);
    setRemainingSeconds(sequence[0].duration);
  };

  const handleSkip = () => {
    if (sequence.length === 0) return;
    setCurrentIndex(idx => {
      const nextIndex = idx + 1;
      if (nextIndex < sequence.length) {
        setRemainingSeconds(sequence[nextIndex].duration);
        return nextIndex;
      } else {
        setIsPlaying(false);
        setIsComplete(true);
        setRemainingSeconds(0);
        return idx;
      }
    });
  };

  const handleJumpTo = (targetIndex: number) => {
    if (targetIndex < 0 || targetIndex >= sequence.length) return;
    setIsComplete(false);
    setCurrentIndex(targetIndex);
    setRemainingSeconds(sequence[targetIndex].duration);
  };

  const formatTime = (totalSeconds: number): string => {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    const mm = String(minutes).padStart(2, '0');
    const ss = String(seconds).padStart(2, '0');
    return `${mm}:${ss}`;
  };

  const current = sequence[currentIndex];

  return (
    <div className="step-through">
      <div className="container">
        <div className="step-header">
          <h1>{flow?.routine_name || 'Your Yoga Flow'}</h1>
          <p>Step through your generated routine pose by pose.</p>
        </div>

        <div className="player-card">
          <div className="pose-info">
            <div className="pose-meta">
              <span className="pose-index">{Math.min(currentIndex + 1, sequence.length)}</span>
              <span className="pose-count">/ {sequence.length}</span>
            </div>
            <div className="pose-name">
              {isComplete ? 'Completed! Great job 🎉' : current?.pose || ''}
            </div>
          </div>

          <div className="timer-display">
            {formatTime(isComplete ? 0 : remainingSeconds)}
          </div>

          {!isComplete && current?.description && (
            <div className="pose-description">
              {current.description}
            </div>
          )}

          <div className="controls">
            <button className="btn btn-secondary" onClick={() => console.log("clicked save")}>
              Save Routine
            </button>
            <button
              className="btn btn-primary"
              onClick={handlePlay}
              disabled={isPlaying || isComplete || sequence.length === 0}
            >
              ▶ Play
            </button>
            <button
              className="btn btn-tertiary"
              onClick={handlePause}
              disabled={!isPlaying}
            >
              ⏸ Pause
            </button>
            <button
              className="btn btn-tertiary"
              onClick={handleSkip}
              disabled={sequence.length === 0 || isComplete}
            >
              ⏭ Skip
            </button>
            <button
              className="btn btn-secondary"
              onClick={handleReset}
              disabled={sequence.length === 0}
            >
              ⟲ Reset
            </button>
          </div>
        </div>

        {sequence.length > 0 && (
          <div className="up-next">
            <h3>Up Next</h3>
            <div className="next-list">
              {sequence
                .slice(currentIndex + 1, currentIndex + 16)
                .map((s, i) => {
                  const absoluteIndex = currentIndex + 1 + i;
                  return (
                    <div
                      key={`${currentIndex}-${absoluteIndex}`}
                      className="next-item clickable"
                      onClick={() => handleJumpTo(absoluteIndex)}
                      role="button"
                      aria-label={`Jump to pose ${s.pose}`}
                    >
                      <span className="next-name">{s.pose}</span>
                      <span className="next-duration">{s.duration}s</span>
                    </div>
                  );
                })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StepThrough;


