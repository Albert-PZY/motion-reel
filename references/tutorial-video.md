# Tutorial Video Design

Tutorial and explainer videos need strong information pacing. The viewer should
always know what to look at and why it matters.

## Script Shape

Use an exploratory structure instead of announcement-only narration:

1. Pose a concrete question or confusion.
2. Show a simple intuition.
3. Test or animate the intuition step by step.
4. Formalize the result only after the viewer has seen the mechanism.
5. Recap the key idea with a fast visual replay.

Avoid:

```text
First this is the input layer. Next this is the convolution layer.
```

Prefer:

```text
You can recognize this digit immediately. But what does the computer see?

It does not see a drawing. It sees a grid of numbers.

Now the question becomes: how can a small pattern detector find a line inside
that grid?
```

## Scene Granularity

Use one scene for one concept:

| Scene type | Purpose |
|---|---|
| Hook | Show the question or stakes |
| Input | Reveal what data the system actually receives |
| Mechanism | Animate one operation slowly |
| Acceleration | Repeat the same operation faster after it is understood |
| Formalization | Add formula, labels, or code |
| Summary | Replay the full pipeline |

## Process Animation

Process animation should show how work happens, not only what the result is.

For a convolution example:

```text
0-3s: introduce the operation
3-12s: first window position in full detail
12-18s: second and third positions at medium speed
18-23s: remaining positions quickly
23-25s: show the completed feature map
```

Script the pauses:

```text
Let us calculate the first position.

[window moves]

The filter covers these nine numbers.

[cells highlight]

Multiply each input by its matching weight.

[terms appear one by one]

Now add them. This result is written into the first cell of the feature map.
```

## Useful Components

### Staggered Reveal

```tsx
const StaggeredGroup: React.FC<{
  children: React.ReactNode;
  delayPerItem?: number;
}> = ({ children, delayPerItem = 8 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <>
      {React.Children.map(children, (child, index) => {
        const delay = index * delayPerItem;
        const progress = spring({
          frame: frame - delay,
          fps,
          config: { damping: 12, stiffness: 100 },
        });

        if (frame < delay) return null;
        return <group scale={Math.max(0, progress)}>{child}</group>;
      })}
    </>
  );
};
```

### Step-By-Step Calculation

```tsx
const StepByStepCalc: React.FC<{
  steps: string[];
  startFrame: number;
  framesPerStep?: number;
}> = ({ steps, startFrame, framesPerStep = 20 }) => {
  const frame = useCurrentFrame();

  return (
    <div style={{ color: "white", fontFamily: "monospace", fontSize: 24 }}>
      {steps.map((step, index) => {
        const stepStart = startFrame + index * framesPerStep;
        const opacity = interpolate(frame, [stepStart, stepStart + 10], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const isResult = index === steps.length - 1;

        return (
          <span
            key={`${step}-${index}`}
            style={{
              color: isResult ? "#83c167" : "white",
              fontWeight: isResult ? 700 : 400,
              opacity,
            }}
          >
            {step}{" "}
          </span>
        );
      })}
    </div>
  );
};
```

### Sliding Window

```tsx
const SlidingWindow: React.FC<{
  gridSize: number;
  windowSize: number;
  stride: number;
  currentStep: number;
}> = ({ gridSize, windowSize, stride, currentStep }) => {
  const outputSize = Math.floor((gridSize - windowSize) / stride) + 1;
  const totalSteps = outputSize * outputSize;
  const step = Math.min(currentStep, totalSteps - 1);

  const row = Math.floor(step / outputSize) * stride;
  const col = (step % outputSize) * stride;
  const cellSize = 0.12;
  const gap = 0.01;
  const offset = (gridSize / 2 - 0.5) * (cellSize + gap);
  const windowOffset = (windowSize / 2 - 0.5) * (cellSize + gap);

  const x = col * (cellSize + gap) - offset + windowOffset;
  const y = row * (cellSize + gap) - offset + windowOffset;

  return (
    <mesh position={[x, y, 0.05]}>
      <boxGeometry
        args={[
          windowSize * cellSize + (windowSize - 1) * gap,
          windowSize * cellSize + (windowSize - 1) * gap,
          0.02,
        ]}
      />
      <meshStandardMaterial
        color="#ff6b6b"
        emissive="#ff6b6b"
        emissiveIntensity={0.3}
        opacity={0.6}
        transparent
      />
    </mesh>
  );
};
```

## Semantic Colors

Use a semantic palette:

```ts
export const COLORS = {
  background: "#000000",
  positive: "#58c4dd",
  negative: "#ff6b6b",
  highlight: "#f5d90a",
  result: "#83c167",
  text: "#ffffff",
  neutral: "#888888",
  accent: "#ff8c00",
};
```

Avoid changing color meanings between scenes.

## Common Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| 3D spectacle first | Motion distracts from the idea | Use the simplest view that explains the concept |
| Random colors | Viewers cannot infer meaning | Define a semantic color map |
| Everything appears at once | Attention has no path | Reveal items sequentially and highlight the focus |
| Only explains "what" | Motivation is missing | Ask "why" before showing the mechanism |
| One huge scene | Timing and code become brittle | Split by concept and use scene config |
| Progress exceeds 100% | Derived progress is unclamped | Use `Math.min(1, progress)` or interpolation clamps |

