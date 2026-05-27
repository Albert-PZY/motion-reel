export interface SceneConfig {
  id: string;
  title: string;
  durationInFrames: number;
  audioFile: string;
}

export const SCENES: SceneConfig[] = [
  {
    id: "01-intro",
    title: "Opening",
    durationInFrames: 300,
    audioFile: "01-intro.mp3",
  },
  {
    id: "02-concept",
    title: "Core concept",
    durationInFrames: 450,
    audioFile: "02-concept.mp3",
  },
  {
    id: "03-demo",
    title: "Demonstration",
    durationInFrames: 600,
    audioFile: "03-demo.mp3",
  },
];

export function getSceneStart(sceneIndex: number): number {
  return SCENES.slice(0, sceneIndex).reduce(
    (sum, scene) => sum + scene.durationInFrames,
    0,
  );
}

export const FPS = 30;

export const TOTAL_FRAMES =
  SCENES.reduce((sum, scene) => sum + scene.durationInFrames, 0) + 60;

