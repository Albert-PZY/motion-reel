# Remotion Three

Use `@remotion/three` when the video benefits from spatial objects, product
motion, 3D data, characters, or camera moves. Do not use 3D just for decoration
in educational videos where a 2D diagram is clearer.

## Install

```bash
pnpm add three @react-three/fiber @remotion/three @types/three
```

Add drei only when needed:

```bash
pnpm add @react-three/drei
```

## Basic Scene

```tsx
import { useThree } from "@react-three/fiber";
import { ThreeCanvas } from "@remotion/three";
import {
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { useEffect } from "react";

const Cube = () => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();
  const camera = useThree((state) => state.camera);

  useEffect(() => {
    camera.position.set(0, 0, 5);
    camera.lookAt(0, 0, 0);
  }, [camera]);

  const rotation = interpolate(frame, [0, durationInFrames], [0, Math.PI * 2]);
  const scale = spring({ frame, fps, config: { damping: 10 } });

  return (
    <mesh rotation={[0, rotation, 0]} scale={scale}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#58c4dd" />
    </mesh>
  );
};

export const ThreeVideo = () => {
  const { width, height } = useVideoConfig();

  return (
    <ThreeCanvas width={width} height={height}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <Cube />
    </ThreeCanvas>
  );
};
```

## Camera Rules

Avoid infinite easing loops that never converge:

```tsx
// Bad: can keep shaking forever.
camera.position.z += (targetZ - camera.position.z) * 0.05;
```

Use direct positions for scene cuts:

```tsx
const CameraController: React.FC<{ sceneIndex: number }> = ({ sceneIndex }) => {
  const { camera } = useThree();
  const positions: Record<number, [number, number, number]> = {
    0: [0, 0, 4],
    1: [0, 0, 3],
    2: [-0.5, 0, 3.5],
    3: [0, 0, 5],
  };
  const target = positions[sceneIndex] ?? positions[0];
  camera.position.set(...target);
  camera.lookAt(0, 0, 0);
  return null;
};
```

For animated moves, derive the position from `spring()` or `interpolate()` and
clamp the value.

## Image Grid Coordinates

Map image coordinates correctly:

```tsx
for (let row = 0; row < size; row++) {
  for (let col = 0; col < size; col++) {
    const x = (col - size / 2 + 0.5) * cellSize;
    const y = (size - 1 - row - size / 2 + 0.5) * cellSize;
    // col maps to x, row maps to y, row is flipped.
  }
}
```

If `row` maps to x and `col` maps to y, images rotate by 90 degrees.

## 2D In 3D

Use orthographic projection for flat explanatory diagrams:

```tsx
import { OrthographicCamera } from "@react-three/drei";

<OrthographicCamera makeDefault position={[0, 0, 10]} zoom={100} />;
```

Use `planeGeometry` and `meshBasicMaterial` for flat cells, labels, and diagrams.

## GLTF Models

```tsx
import { useGLTF } from "@react-three/drei";
import { interpolate, useCurrentFrame } from "remotion";

const Model = () => {
  const frame = useCurrentFrame();
  const { scene } = useGLTF("/models/product.glb");
  const rotation = interpolate(frame, [0, 150], [0, Math.PI * 2]);

  return <primitive object={scene} rotation={[0, rotation, 0]} scale={0.5} />;
};
```

Put model files in `public/models/`.

## Video Texture

Use frame-accurate texture loading during render:

```tsx
import { ThreeCanvas, useOffthreadVideoTexture } from "@remotion/three";
import { staticFile } from "remotion";

const VideoPlane = () => {
  const texture = useOffthreadVideoTexture({
    src: staticFile("video/source.mp4"),
  });

  return (
    <mesh>
      <planeGeometry args={[4, 3]} />
      {texture ? <meshBasicMaterial map={texture} /> : null}
    </mesh>
  );
};
```

## 3D Performance

- Mount only one heavy `ThreeCanvas` at a time.
- Conditionally render expensive scene branches by scene index.
- Keep geometry counts low for final render unless the shot needs complexity.
- Prefer generated primitive geometry for tutorials and bespoke models for
  product shots.
- Verify still frames before full video renders.

